from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import CustomUserSerializer, LoginSerializer, EmailSerializer, ResetPasswordSerializer
# allow login
from rest_framework.permissions import AllowAny
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.views.decorators.csrf import csrf_exempt

from .send_email import send

class AuthViewSet(viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'login':
            return LoginSerializer
        return CustomUserSerializer
    
    def get_permissions(self):
        if self.action == 'login':
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        
        if not user:
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        })

    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if user exists
        if CustomUser.objects.filter(email=serializer.validated_data['email']).exists():
            return Response(
                {'error': 'User with this email already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # If is_employer is True, is_applicant should be False, create employer profile
        # if serializer.validated_data['is_employer']:
        #     # serializer.validated_data['is_applicant'] = False
        #     # create employer profile
        #     EmployerProfile.objects.create(user=serializer.save())


        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put', 'patch'])
    def update_profile(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()
        
        return Response({
            'user_id': updated_user.id,
            'username': updated_user.username,
            'email': updated_user.email
        })
    
    # logout
    @action(detail=False, methods=['post'])
    def logout(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Logged out successfully'})
    

    @action(detail=False, methods=['post'])
    def forgot_password(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user = CustomUser.objects.filter(email=email).first()
        
        if user:
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            
            # Generate password reset link using the action URL pattern
            reset_link = f"https://stockmanagementappweb.netlify.app/reset/?uidb64={uidb64}&token={token}"
            
            # Send email
            send("Password Reset", reset_link, [email])
            
            return Response({'message': 'Password reset email sent'}, status=status.HTTP_200_OK)
        return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def reset_password(self, request):
        # Get uidb64 and token from query parameters
        uidb64 = request.query_params.get('uidb64')
        token = request.query_params.get('token')
        
        if not uidb64 or not token:
            return Response(
                {'error': 'Invalid password reset link'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Decode the user ID and get the user
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
            
            # Verify the token
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {'error': 'Invalid or expired token'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validate and set the new password
            serializer = ResetPasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            user.set_password(serializer.validated_data['password'])
            user.save()
            
            return Response(
                {'message': 'Password reset successfully'}, 
                status=status.HTTP_200_OK
            )
            
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response(
                {'error': 'Invalid reset link'}, 
                status=status.HTTP_400_BAD_REQUEST
            )