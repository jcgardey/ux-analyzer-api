from django.db import models
from .micro_measures_grabbers import grabbers
from users.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist

from prediction_models.prediction_models import prediction_models
import numpy as np

class Evaluation(models.Model):
    evaluation_name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='evaluations')

class Version(models.Model):

    version_name = models.CharField(max_length=255)
    token = models.CharField(max_length=16)
    urls = models.CharField(max_length=500)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, null=True, related_name='versions')

    def get_user_interaction_effort(self):
        valid_sessions = list(filter(lambda s: s.get_user_interaction_effort() is not None, self.user_sessions.all()))
        if len(valid_sessions) == 0:
            return None
        return np.mean( np.array([session.get_user_interaction_effort() for session in valid_sessions]) ) 
    
    def get_user_sessions_count(self):
        return self.user_sessions.all().count()
    
    def get_widget(self, url, xpath, widgetType, label):
        try:
            return self.widgets.get(url=url, xpath= xpath, widget_type=widgetType)
        except ObjectDoesNotExist:
            return self.widgets.create(url=url, xpath= xpath, widget_type=widgetType, label=label)
    
    def calculate_user_interaction_effort(self):
        for user_session in self.user_sessions.all():
            user_session.calculate_user_interaction_effort()
    
    def get_widgets(self):
        return self.widgets
    
class UserSession(models.Model):

    version = models.ForeignKey(Version, on_delete=models.CASCADE, related_name='user_sessions')
    date = models.DateTimeField(auto_now=True)
    time = models.DurationField(null=True)
    session_id = models.CharField(max_length=50)
    
    def get_user_interaction_effort(self):
        valid_logs = list(filter(lambda log: not log.widget.disabled and log.has_user_interaction_effort(), self.widget_logs.all()))
        if len(valid_logs) == 0:
            return None
        predictions = np.array([ widget_log.get_user_interaction_effort() for widget_log in valid_logs ])
        widget_weights = list(map(lambda widget_log: widget_log.widget.weight, valid_logs))
        return np.average(predictions.reshape(-1), weights=widget_weights)

    def calculate_user_interaction_effort(self):
        for widget_log in filter(lambda w: w.is_valid(), self.widget_logs.all()):
            widget_log.calculate_user_interaction_effort()
            widget_log.save()
    
class Widget(models.Model):
    WIDGET_TYPES = [
        ('TextInput', 'TextInput'), 
        ('SelectInput', 'SelectInput'),
        ('Anchor', 'Anchor'), 
        ('Datepicker', 'Datepicker'), 
        ('DateSelect', 'DateSelect'), 
        ('RadioSet', 'RadioSet'), 
    ]
    version = models.ForeignKey(Version, on_delete=models.CASCADE, related_name='widgets')
    label = models.CharField(max_length=255)
    xpath = models.CharField(max_length=255)
    widget_type = models.CharField(max_length=255, choices=WIDGET_TYPES)
    url = models.URLField(max_length=255)
    weight = models.FloatField(default=1)
    disabled = models.BooleanField(default=False)

    def get_user_interaction_effort(self):
        valid_logs = list(filter(lambda w: w.has_user_interaction_effort(), self.logs.all()))
        if len(valid_logs) == 0:
            return None
        predictions = np.array([ widget_log.get_user_interaction_effort() for widget_log in valid_logs])
        return np.mean(predictions)

class WidgetLog(models.Model):
    
    user_session = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name='widget_logs')
    micro_measures = models.JSONField()
    widget = models.ForeignKey(Widget, on_delete=models.CASCADE, related_name='logs', null=True)
    interaction_effort = models.FloatField(null=True)

    def is_valid(self):
        for value in grabbers[self.widget.widget_type].get_measures_for_prediction(self.micro_measures):
            if value is None or value == 'NaN':
                return False
        return True
    
    def has_user_interaction_effort(self):
        return self.interaction_effort is not None


    def calculate_user_interaction_effort(self):
        if (self.is_valid()):
            prediction_model = prediction_models.get_widget_model(self.widget.widget_type)
            micro_measures_normalized = prediction_model.scaler.transform(  np.array(grabbers[self.widget.widget_type].get_measures_for_prediction(self.micro_measures)).reshape(1,-1) )
            self.interaction_effort = prediction_model.predict( micro_measures_normalized )[0]
    
    def get_user_interaction_effort(self):
        return self.interaction_effort




