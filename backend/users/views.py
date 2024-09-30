from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.conf import settings
from django.shortcuts import get_object_or_404
from users.serializers import UserSerializer
from users.models import User, BlacklistedToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from django.db import IntegrityError, transaction
import logging
import jwt

# Set up logger
logger = logging.getLogger(__name__)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            username = request.data.get('username')

            # Check for missing fields
            missing_fields = []
            if not email:
                missing_fields.append('email')
            if not password:
                missing_fields.append('password')
            if not username:
                missing_fields.append('username')
            if missing_fields:
                return Response({'error': 'Missing required fields', 'fields': missing_fields}, status=status.HTTP_400_BAD_REQUEST)

            # Validate email format
            try:
                validate_email(email)
            except DjangoValidationError:
                return Response({'error': 'Invalid email format', 'field': 'email'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if email or username already exists
            if User.objects.filter(email=email).exists():
                return Response({'error': 'Email already exists', 'field': 'email'}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists', 'field': 'username'}, status=status.HTTP_400_BAD_REQUEST)

            # Validate password
            try:
                validate_password(password)
            except DjangoValidationError as e:
                return Response({'error': 'Invalid password', 'details': e.messages, 'field': 'password'}, status=status.HTTP_400_BAD_REQUEST)

            # Create user
            user = User.objects.create_user(username=username, email=email, password=password)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            logger.error(f"Database integrity error during registration: {str(e)}")
            return Response({'error': 'Database integrity error', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Unexpected error during registration: {str(e)}")
            return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            # Check for missing fields
            if not email and not password:
                return Response({'error': 'Both email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
            elif not email:
                return Response({'error': 'Email is required', 'field': 'email'}, status=status.HTTP_400_BAD_REQUEST)
            elif not password:
                return Response({'error': 'Password is required', 'field': 'password'}, status=status.HTTP_400_BAD_REQUEST)

            # Validate email format
            try:
                validate_email(email)
            except DjangoValidationError:
                return Response({'error': 'Invalid email format', 'field': 'email'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if user exists
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'No user found with this email', 'field': 'email'}, status=status.HTTP_404_NOT_FOUND)

            # Check if the account is active
            if not user.is_active:
                return Response({'error': 'This account has been deactivated'}, status=status.HTTP_403_FORBIDDEN)

            # Verify password
            if not user.check_password(password):
                return Response({'error': 'Incorrect password', 'field': 'password'}, status=status.HTTP_400_BAD_REQUEST)

            # Generate tokens
            try:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                response = Response({
                    'access': access_token,
                    'refresh': refresh_token,
                    'user': UserSerializer(user).data
                })
                response.set_cookie(key='jwt', value=refresh_token, httponly=True, secure=True, samesite='Strict')
                return response

            except Exception as e:
                logger.error(f"Error generating tokens: {str(e)}")
                return Response({'error': 'Error during login process'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(f"Unexpected error during login: {str(e)}")
            return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get('jwt')

        if not refresh_token:
            return Response({'error': 'Refresh token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            
            # Check if the refresh token is blacklisted
            if BlacklistedToken.objects.filter(token=refresh_token).exists():
                return Response({'error': 'Refresh token is blacklisted'}, status=status.HTTP_401_UNAUTHORIZED)

            access_token = str(token.access_token)
            return Response({'access': access_token})
        except TokenError as e:
            return Response({'error': 'Invalid refresh token', 'details': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except InvalidToken as e:
            return Response({'error': 'Token is invalid or expired', 'details': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.error(f"Error refreshing token: {str(e)}")
            return Response({'error': 'Error during token refresh process', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error fetching user data: {str(e)}")
            return Response({'error': 'Error fetching user data', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        try:
            user = request.user
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response({'error': 'Invalid data', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            logger.error(f"Database integrity error updating user data: {str(e)}")
            return Response({'error': 'Database integrity error', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Error updating user data: {str(e)}")
            return Response({'error': 'Error updating user data', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('jwt')
            access_token = request.auth.token if hasattr(request, 'auth') and hasattr(request.auth, 'token') else None

            if not refresh_token and not access_token:
                return Response({'error': 'No tokens provided for logout'}, status=status.HTTP_400_BAD_REQUEST)

            if refresh_token:
                try:
                    token = RefreshToken(refresh_token)
                    BlacklistedToken.objects.create(token=str(token), user=request.user)
                except TokenError:
                    logger.warning(f"Invalid refresh token during logout for user {request.user.id}")
                except Exception as e:
                    logger.error(f"Error blacklisting refresh token: {str(e)}")

            if access_token:
                try:
                    BlacklistedToken.objects.create(token=str(access_token), user=request.user)
                except Exception as e:
                    logger.error(f"Error blacklisting access token: {str(e)}")

            response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
            response.delete_cookie('jwt')
            return response

        except Exception as e:
            logger.error(f"Error during logout for user {request.user.id}: {str(e)}")
            return Response({"error": "An error occurred during logout", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)