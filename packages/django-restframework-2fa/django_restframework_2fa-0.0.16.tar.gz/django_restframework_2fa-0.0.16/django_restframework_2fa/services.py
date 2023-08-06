import phonenumbers

from django.contrib.auth import get_user_model
from django.conf import settings

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client as TwilioClient

from rest_framework import status


class TwilioConfiguration():

    def __init__(self, twilio_sid=settings.TWILIO_SID, twilio_auth_token=settings.TWILIO_AUTH_TOKEN, twilio_service_id=settings.TWILIO_SERVICE_ID):

        self.twilio_sid = twilio_sid
        self.twilio_auth_token = twilio_auth_token
        self.twilio_service_id = twilio_service_id
    
    def _is_mobile_number_correct(self, mobile_number : str):

        """
        This method will validate the user's mobile number stored in db. 
        In case of invalid number it will raise and exception.
        """
        
        try:
        
            mobile_number = phonenumbers.parse(mobile_number, None)
        
        except Exception as e:
            
            raise ValueError('Invalid mobile number.')

        if (not phonenumbers.is_possible_number(mobile_number)) or (not phonenumbers.is_valid_number(mobile_number)):

            raise ValueError('Invalid mobile number.')

    def _get_twilio_client(self):

        """
        This method will return the twilio client object.
        """

        try:

            twilio_client = TwilioClient(self.twilio_sid, self.twilio_auth_token)

        except TwilioRestException as e:
            
            #possible reason of this exception could be the invalid twilio_sid or twilio_auth_token.
            raise Exception("You have requested for OTP to many times. Please try after 10 minutes.")
        
        return twilio_client

    def send_otp(self, mobile_number : str):

        """
        This method will validate the provided mobile number and if it is correct the it will try to send an OTP.
        If twilio service has raised an exception then the exception will be printed on to the terminal and an
        exception will be raised for the end user.
        """

        try:
            
            self._is_mobile_number_correct(mobile_number)

        except ValueError as e:

            raise e

        try:

            verification = self._get_twilio_client() \
                .verify.services(self.twilio_service_id) \
                .verifications \
                .create(to=str(mobile_number), channel='sms')
        
        except TwilioRestException as e:

            raise e