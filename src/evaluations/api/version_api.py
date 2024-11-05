from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from evaluations.models import Evaluation, Version
from evaluations.serializers import VersionSerializer, WidgetSerializer

import random
import string

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
    #permission_classes = [IsAuthenticated]

    def post(self, request, id):
        version = Version.objects.get(pk=id)
        version.calculate_user_interaction_effort()
        return Response(VersionSerializer(version).data)     