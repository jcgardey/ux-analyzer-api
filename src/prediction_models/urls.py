from prediction_models.api import TrainModelsAPI
from django.urls import path

urlpatterns = [
    path('prediction_models/train', TrainModelsAPI.as_view())
]