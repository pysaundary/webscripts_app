from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *


class CreateUserView(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

class LoginUserView(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = LoginUserSerializer

class ForgetPasswordView(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = ForgetPasswordSerializer

class ConfirmPasswordView(ModelViewSet):
    serializer_class = ValidateAndChangePassword

