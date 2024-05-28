from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from knox.models import AuthToken
from rest_framework import status
from rest_framework.response import Response
from .serializers import LoginUserSerializer, SignUpUserSerializer
from rest_framework.permissions import IsAuthenticated
from users.models import User, UserProfile

class LoginAPI(APIView):
    
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        user = authenticate(email=request.data['email'], password=request.data['password'])
        if user is None:
            return Response({'credentials': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        login(request, user)
        _, token = AuthToken.objects.create(user=user)
        return Response({ 'token': token, 'name': user.name })

class GetLoggedUserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'name': request.user.name})


class SignUpUserAPI(APIView):

    def post(self, request):
        serializer = SignUpUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        user = User.objects.create_user(**serializer.validated_data)
        user.profile = UserProfile()
        user.profile.save()
        return Response(LoginUserSerializer(user).data, status=status.HTTP_200_OK)
        
        