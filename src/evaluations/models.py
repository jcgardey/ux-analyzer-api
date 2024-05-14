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
        return np.mean( np.array([session.get_user_interaction_effort() for session in self.user_sessions.all()]) ) if self.get_user_sessions_count() > 0 else None
    
    def get_user_sessions_count(self):
        return self.user_sessions.all().count()
    
    def get_widget(self, url, xpath, widgetType, label):
        try:
            return self.widgets.get(url=url, xpath= xpath, widget_type=widgetType)
        except ObjectDoesNotExist:
            return self.widgets.create(url=url, xpath= xpath, widget_type=widgetType, label=label)
    
    def get_widgets(self):
        return self.widgets
    
class UserSession(models.Model):

    version = models.ForeignKey(Version, on_delete=models.CASCADE, related_name='user_sessions')
    date = models.DateTimeField(auto_now=True)
    time = models.DurationField(null=True)
    session_id = models.CharField(max_length=50)
    
    def get_user_interaction_effort(self):
        if self.widget_logs.count() == 0:
            return None
        predictions = np.array([ widget_log.get_user_interaction_effort() for widget_log in self.widget_logs.all() ])
        widget_weights = list(map(lambda widget_log: widget_log.widget.weight, self.widget_logs.all()))
        return np.average(predictions.reshape(-1), weights=widget_weights)
    
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

    def get_user_interaction_effort(self):
        if self.logs.count() == 0:
            return None
        predictions = np.array([ widget_log.get_user_interaction_effort() for widget_log in self.logs.all() ])
        return np.mean(predictions)

class WidgetLog(models.Model):
    
    user_session = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name='widget_logs')
    micro_measures = models.JSONField()
    widget = models.ForeignKey(Widget, on_delete=models.CASCADE, related_name='logs', null=True)

    def get_user_interaction_effort(self):
        prediction_model = prediction_models.get_widget_model(self.widget.widget_type)
        micro_measures_normalized = prediction_model.scaler.transform(  np.array(grabbers[self.widget.widget_type].get_measures_for_prediction(self.micro_measures)).reshape(1,-1) )
        return prediction_model.predict( micro_measures_normalized )




