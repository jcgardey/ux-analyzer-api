from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from prediction_models.prediction_models import prediction_models

class TrainModelsAPI(APIView):

    def get(self, request):
        try:
            prediction_models.train_models()
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

