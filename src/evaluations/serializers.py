from rest_framework import serializers
from .models import Evaluation, WidgetLog, UserSession, Version, Widget

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ('id', 'evaluation_name', 'creation_date')

class WidgetSerializer(serializers.ModelSerializer):
    user_interaction_effort = serializers.SerializerMethodField()
    class Meta:
        model = Widget
        fields = ('id','widget_type', 'url', 'label', 'xpath', 'weight', 'user_interaction_effort')
    
    def get_user_interaction_effort(self, widget):
        return round(widget.get_user_interaction_effort(), 1)

class WidgetLogSerializer(serializers.ModelSerializer):
    widget = WidgetSerializer()
    class Meta:
        model = WidgetLog
        fields = ('micro_measures', 'widget')

class UserSessionSerializer(serializers.ModelSerializer):
    widget_logs = WidgetLogSerializer(many=True)
    user_interaction_effort = serializers.SerializerMethodField()

    class Meta:
        model = UserSession
        fields = ('user_interaction_effort','widget_logs', 'session_id', 'time', 'date')
    
    def get_user_interaction_effort(self, user_session):
        return round(user_session.get_user_interaction_effort(), 1)


class VersionSerializer(serializers.ModelSerializer):
    user_interaction_effort = serializers.SerializerMethodField()
    user_sessions_count = serializers.SerializerMethodField()
    widgets_count = serializers.SerializerMethodField()
    urls = serializers.SerializerMethodField()
    class Meta:
        model = Version
        fields = ('id', 'version_name', 'urls', 'token' , 'user_interaction_effort', 'user_sessions_count', 'widgets_count')
    
    def get_user_interaction_effort(self, version):
        return round(version.get_user_interaction_effort(),1) if version.get_user_interaction_effort() else None
    
    def get_user_sessions_count(self, version):
        return version.get_user_sessions_count()
    
    def get_widgets_count(self, version):
        return version.get_widgets().count()
    
    def get_urls(self, version):
        return version.urls.split(',')


class FullEvaluationSerializer(serializers.ModelSerializer):
    versions = VersionSerializer(many=True)

    class Meta:
        model = Evaluation
        fields = ('id', 'evaluation_name', 'versions')