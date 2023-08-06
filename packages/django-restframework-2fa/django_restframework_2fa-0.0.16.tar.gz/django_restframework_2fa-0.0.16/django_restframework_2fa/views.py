from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django_restframework_2fa.serializers import RequestLoginSerializer
from twilio.base.exceptions import TwilioRestException


User = get_user_model()


class Login2FARequestOTPView(APIView):

    '''
    This view is used to request an OTP on the user's mobile number for verification.
    It uses basic authentication instead of JWTAuthentication.
    '''

    def post(self, request, format=None):

        serialized_data = RequestLoginSerializer(data=request.data)

        serialized_data.is_valid(raise_exception=True)

        try:
            
            user_instance = User.objects.get(email=serialized_data.validated_data['email']) 

        except User.DoesNotExist:
            
            return Response({'message':'Account with the provided credentials does not exist.'}, status.HTTP_400_BAD_REQUEST)

        if not user_instance.check_password(serialized_data.validated_data['password']):
    
            return Response({'message':'Invalid credentials.'}, status.HTTP_401_UNAUTHORIZED)
        
        try:

            response = serialized_data.get_response(user_instance)
        
        except ValueError as e:

            return Response({"message": str(e)}, status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            
            return Response({"message": str(e)}, status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(response, status=status.HTTP_200_OK )