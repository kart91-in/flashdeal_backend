import requests
from django.conf import settings

url = 'http://saruman.staging.shadowfax.in/api/v1/clients/requests'
reverse_url = 'http://reverse.shadowfax.in/api'
token = '51b4c7633d583a9474b147187fb1e1498d22e6ad'

if not settings.DEBUG:
    url = 'http://saruman.shadowfax.in/api'
    reverse_url = 'http://reverse.shadowfax.in/api'
    token = settings.SHADOWFAX_TOKEN



def send_forward_request(data):
    return requests.post(url, json=data, headers={'Authorization': f'Token {token}'}).json()
