from jwt import InvalidTokenError, ExpiredSignatureError
from mail_templated import send_mail
from rest_framework import generics, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from django.contrib.auth import logout
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.api.v1.serializers import RegisterSerializer, UserSerializer, ChangePasswordSerializer, \
    CustomTokenObtainPairSerializer, EmailSerializer
from ..utils import EmailThread

from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate token for verification
        tokens = self.get_tokens_for_user(user)

        # Prepare email context
        context = {
            'name': user.username,
            'email': user.email,
            'verification_token': tokens['access'],
            'site_url': request.build_absolute_uri('/accounts/api/v1')
        }

        # Send verification email
        email_thread = EmailThread(
            subject='Verify Your Email',
            template_name='email/verification.tpl',
            context=context
        )
        email_thread.start()
        return Response({
            "user_username": user.username,
            "email": user.email,
            "message": "User Created Successfully. Please check your email to verify your account.",
        }, status=status.HTTP_201_CREATED)


class LoginView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not user.is_verified:
            return Response({"message": "User account is disabled."}, status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_username': user.username,
            'user_id': user.pk,
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({"message": "User Logged Out Successfully."})


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class SendTestEmail(generics.GenericAPIView):
    serializer_class = EmailSerializer

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
            if user.is_verified:
                return Response({
                    'status': 'error',
                    'message': 'Email already verified'
                }, status=status.HTTP_400_BAD_REQUEST)
            tokens = self.get_tokens_for_user(user)
            context = {
                'name': user.username,
                'email': user.email,
                'verification_token': tokens['access'],
                'site_url': request.build_absolute_uri('/accounts/api/v1')
            }
            email_thread = EmailThread(
                subject='Verify Your Email',
                template_name='email/verification.tpl',
                context=context
            )
            email_thread.start()
            return Response({
                'status': 'success',
                'message': 'Email sent successfully'
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Email does not exist'
            }, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(generics.GenericAPIView):
    def get(self,request, token):
        try:
            token_obj = AccessToken(token)
            user_id = token_obj.payload['user_id']

            # get and verify user
            user = User.objects.get(id=user_id)
            if user.is_verified:
                return Response({
                    'status': 'error',
                    'message': 'Email already verified'
                }, status=status.HTTP_400_BAD_REQUEST)
            user.is_verified = True
            user.save()
            return Response({
                'status': 'success',
                'message': 'Email verified successfully'
            }, status=status.HTTP_200_OK)
        except (InvalidTokenError, ExpiredSignatureError):
            return Response({
                'status': 'error',
                'message': 'Invalid or expired token'
            }, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class ResendVerificationEmail(generics.GenericAPIView):
    serializer_class = EmailSerializer

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
            if user.is_verified:
                return Response({
                    'status': 'error',
                    'message': 'Email already verified'
                }, status=status.HTTP_400_BAD_REQUEST)
            tokens = self.get_tokens_for_user(user)
            context = {
                'name': user.username,
                'email': user.email,
                'verification_token': tokens['access'],
                'site_url': request.build_absolute_uri('/accounts/api/v1')
            }
            email_thread = EmailThread(
                subject='Verify Your Email',
                template_name='email/verification.tpl',
                context=context
            )
            email_thread.start()
            return Response({
                'status': 'success',
                'message': 'Email sent successfully'
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Email does not exist'
            }, status=status.HTTP_400_BAD_REQUEST)
