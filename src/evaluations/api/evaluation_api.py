from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from evaluations.serializers import EvaluationSerializer, FullEvaluationSerializer

from evaluations.models import Evaluation

class CreateEvaluationAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        evaluation = request.user.profile.evaluations.create(evaluation_name=request.data['evaluation_name'])
        return Response(EvaluationSerializer(evaluation).data, status=status.HTTP_201_CREATED)

class DeleteEvaluationAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id):
        evaluation = Evaluation.objects.get(pk=id)
        if request.user.profile == evaluation.user:
            return Response(evaluation.delete())
        else:
            return Response({'error': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


class ListEvaluationsApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(EvaluationSerializer(request.user.profile.evaluations.all(), many=True).data)

class GetEvaluationAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        evaluation = Evaluation.objects.get(pk=id)
        if request.user.profile == evaluation.user:
            return Response(FullEvaluationSerializer(evaluation).data)
        else:
            return Response({'error': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)