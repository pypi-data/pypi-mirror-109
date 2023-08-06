from django.contrib.auth import get_user_model

from django_restframework_2fa.services import TwilioConfiguration

from rest_framework import serializers

User = get_user_model


class RequestLoginSerializer(serializers.Serializer):

    def __init__(self, **data):

        self.twilio_config = TwilioConfiguration()

        super().__init__(**data)

    email = serializers.EmailField(required=True, allow_null=False, allow_blank=False)
    password = serializers.CharField(required=True, allow_null=False, allow_blank=False)

    def validate_email(self, value : str):

        """
        This method will simple strip all the preceding and following white spaces of email and then it will return the 
        lower case of email.
        """

        value = value.strip()

        return value.lower()

    
    def get_response(self, user_instance = User):

        """
        This method will simply send the OTP and will return the API response object.
        It accept an object which should be the instance of get_user_model().

        The OTP will be sent to the instance provided above i.e user_instance.mobile_number
        
        """

        # this is important or else the OTP won't be sent.
        self.twilio_config.send_otp(str(user_instance.mobile_number))
        
        return {
            'id': user_instance.id,
            'message': 'An OTP has been sent to your registered mobile number.',
            'mobile_number' : '***-******-' + str(user_instance.mobile_number)[9:]
        }
        