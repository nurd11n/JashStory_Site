from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import (
    RegisterSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ForgotPasswordCompleteSerializer,
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import status, generics
from drf_yasg.utils import swagger_auto_schema
from .tasks import send_password_celery
from .permissions import IsAuthorPermission


User = get_user_model()


class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer())
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Successfully registered', status=201)


class ActivationView(APIView):
    def get(self, request, email, activation_code):
        user = User.objects.filter(email=email, activation_code=activation_code).first()
        if not user:
            return Response('User does not exist', status=400)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Successfully activated', status=200)
    

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Вы успешно вышли из системы."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        # logger.error('Ошибка ChangePasswordV')
        return Response(
            'Пароль успешно обнавлен', status=200
        )


class ForgotPasswordView(generics.CreateAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_data = serializer.validated_data
        email = user_data['email']

        user = User.objects.get(email=email)
        user.create_forgot_password_code()
        user.save()

        send_password_celery.delay(user.email, user.forgot_password_code)
        return Response({'Код восстановления отправлен на ваш email.'}, status=status.HTTP_200_OK)


class ForgotPasswordCompleteView(APIView):

    @swagger_auto_schema(request_body=ForgotPasswordCompleteSerializer)
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        # logger.error('Ошибка ChangePasswordV')
        return Response(
            'Пароль успешно обнавлен', status=200
        )
