import os

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()

class RequestLoginOTPTests(APITestCase):

    def setUp(self):
        
        data = {"email": "jeet@steinnlabs.com", "mobile_number": "+91 9765136777"}
        user = User(**data)
        user.set_password("Jeet@123")
        user.save()
        
    def test_request_login_otp(self):

        """
        Ensure we can get the login otp and the API response is as expected.
        """

        url = '/api/auth/request-login-otp/'
        
        data = {"email": "jeet@steinnlabs.com", "password":"Jeet@123"}
        
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data, {
            'id': 1,
            'message': 'An OTP has been sent to your registered mobile number.',
            'mobile_number' : '***-******-' + '6777'
        })

    def test_with_invalid_email(self):

        """
        To validate the response object and the status code if the provided email does not exist in the db. 
        """

        url = '/api/auth/request-login-otp/'
        
        data = {"email": "jeet@steinnlabs.in", "password":"Jeet@123"}
        
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response.data, {'message':'Account with the provided credentials does not exist.'})
    
    def test_with_invalid_pass(self):

        """
        To validate the response object and the status code if the provided password is incorrect. 
        """

        url = '/api/auth/request-login-otp/'
        
        data = {"email": "jeet@steinnlabs.com", "password":"Jeet@"}
        
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(response.data, {'message':'Invalid credentials.'})
    
    def test_with_invalid_mobile_num(self):

        """
        To validate the response object and the status code if the mobile number associated with the account is incorrect. 
        """

        url = '/api/auth/request-login-otp/'
        
        data = {"email": "jeet@steinnlabs.com", "password":"Jeet@123"}

        user_instance = User.objects.get(email=data['email'])

        user_instance.mobile_number = '987987'

        user_instance.save()
        
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response.data, {'message':'Invalid mobile number.'})
    
    def test_with_invalid_twilio_sid(self):

        """
        To make this test successful twilio account SID must be incorrect.
        This test case is specifically designed generate exception from `_get_twilio_client`.
        """

        os.environ.setdefault('TWILIO_SID', 'qwerty')

        url = '/api/auth/request-login-otp/'

        data = {"email": "jeet@steinnlabs.com", "password":"Jeet@123"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
    
    def test_with_invalid_twilio_service_id(self):

        """
        To make this test successful twilio account's TWILIO_SERVICE_ID must be incorrect.
        This test case is specifically designed to generate the exception from `send_otp`.
        """
        os.environ.setdefault('TWILIO_SERVICE_ID', 'qwerty')

        url = '/api/auth/request-login-otp/'

        data = {"email": "jeet@steinnlabs.com", "password":"Jeet@123"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)