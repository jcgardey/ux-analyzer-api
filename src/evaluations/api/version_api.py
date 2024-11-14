from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from evaluations.models import Evaluation, Version, Widget
from evaluations.serializers import VersionSerializer, WidgetSerializer, ExportVersionSerializer

from evaluations.micro_measures_grabbers import TextInputGrabber, SelectInputGrabber, RadiosetGrabber, AnchorGrabber, DatepickerGrabber

import random
import string
from datetime import timedelta, datetime

class CreateVersionAPI(APIView):
    permission_classes = [IsAuthenticated]

    def generate_version_token(self):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))

    def post(self, request, evaluation_id):
        version = Evaluation.objects.get(pk=evaluation_id).versions.create(version_name=request.data['name'], 
        token=self.generate_version_token(),
        urls=','.join(request.data['urls']) )
        return Response(VersionSerializer(version).data, status=status.HTTP_201_CREATED)

class ListVersionsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, evaluation_id):
        return Response(VersionSerializer(Version.objects.filter(evaluation=evaluation_id), many=True).data)

class GetVersionAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        return Response(VersionSerializer(Version.objects.get(pk=id)).data)

class GetVersionWidgetsAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        widgets = Version.objects.get(pk=id).get_widgets()
        return Response(WidgetSerializer(widgets, many=True).data)

class DeleteVersionAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id):
        return Response(Version.objects.get(pk=id).delete())
    

class UpdateWidgetsSettingsAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, id):
        version = Version.objects.get(pk=id)
        print(request.data)
        for widget_data in request.data['widgets']:
            target_widget = version.widgets.get(pk=widget_data['id'])
            target_widget.weight = float(widget_data['weight'])
            target_widget.label = widget_data['label']
            target_widget.save()
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)

class RefreshUserInteractionEffortAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        version = Version.objects.get(pk=id)
        version.calculate_user_interaction_effort()
        return Response(VersionSerializer(version).data)     


class ExportVersionAPI(APIView):

    def get(self, request, id):
        version = Version.objects.get(pk=id)
        return Response(ExportVersionSerializer(version).data)    


class ImportVersionAPI(APIView):

    grabbers = {
        'TextInput': TextInputGrabber(),
        'SelectInput': SelectInputGrabber(),
        'RadioSet': RadiosetGrabber(),
        'Anchor': AnchorGrabber(),
        'Datepicker': DatepickerGrabber(),
        'DateSelect': SelectInputGrabber()
    }

    def post(self, request, evaluation_id):
        version = Evaluation.objects.get(pk=evaluation_id).versions.create(version_name=request.data['version_name'])
        for session_data in request.data['user_sessions']:
            hours, minutes, seconds = map(float, session_data['time'].split(':'))
            t_delta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
            user_session = version.user_sessions.create(session_id=session_data['session_id'], 
                                                        time=t_delta,
                                                        date=datetime.strptime(session_data['date'], '%Y-%m-%dT%H:%M:%S.%fZ'))
            valid_widget_logs = [ widget_log for widget_log in session_data['widget_logs'] if self.grabbers[widget_log['widget']['widget_type']].is_log_valid(widget_log['micro_measures']) ]
            for widget_log in valid_widget_logs:
                target_widget = version.get_widget(widget_log['widget']['url'], widget_log['widget']['xpath'], widget_log['widget']['widget_type'], widget_log['widget']['label'])
                user_session.widget_logs.create(
                    widget=target_widget,
                    micro_measures= widget_log['micro_measures']
                )
        return Response({'result': 'ok'}, status=status.HTTP_201_CREATED)
    

class JoinWidgetsAPI(APIView):

    def post(self, request, version_id):
        version = Version.objects.get(pk=version_id)
        if (request.data.get('widgetIds', None) is None or len(request.data['widgetIds']) == 0):
            return Response({'result': 'invalid widgets'}, status=status.HTTP_401_BAD_REQUEST)
            
        first_widget = Widget.objects.get(pk=request.data['widgetIds'][0])
        new_widget = version.widgets.create(label=first_widget.label, xpath=first_widget.xpath, url=first_widget.url, widget_type=first_widget.widget_type)
        for widget_id in request.data['widgetIds']:
            target = Widget.objects.get(pk=widget_id)
            new_widget.logs.add(*target.logs.all())
            target.delete()
        new_widget.save()
        return Response({'result': 'ok'}, status=status.HTTP_200_OK)

