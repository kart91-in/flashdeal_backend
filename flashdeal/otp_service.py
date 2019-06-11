import requests
from django.conf import settings

default_params = {
    'sender': 'Kart91',
    'authkey': settings.OTP_SERVICE_KEY,
}

def send_otp_message(to_phone_number):
    return requests.post('https://control.msg91.com/api/sendotp.php', data={
        **default_params,
        'mobile': to_phone_number
    }).json()


def resend_otp_message(to_phone_number):
    return requests.post('https://control.msg91.com/api/retryotp.php', data={
        **default_params,
        'mobile': to_phone_number,
        'retrytype': 'text'
    }).json()

def verify_otp(phone_number, otp):
    return requests.post('https://control.msg91.com/api/verifyRequestOTP.php', data={
        **default_params,
        'mobile': phone_number,
        'otp': otp
    }).json()

