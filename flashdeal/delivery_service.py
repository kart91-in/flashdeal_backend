import requests
from django.conf import settings

url = 'http://saruman.staging.shadowfax.in/api/v1/clients/requests'
reverse_url = 'http://reverse.shadowfax.in/api'
token = '51b4c7633d583a9474b147187fb1e1498d22e6ad'

if not settings.DEBUG:
  url = 'http://saruman.shadowfax.in/api'
  reverse_url = 'http://reverse.shadowfax.in/api'
  token = settings.SHADOWFAX_TOKEN
x = {
  "client_order_number": "0121001",
  "warehouse_name": "Client Warehouse",
  "warehouse_address": "Client Warehouse Address",
  "destination_pincode": 500001,
  "total_amount": 430,
  "price": 412,
  "eway_bill": 123456789012,
  "pickup_type": "regular",
  "address_attributes": {
    "address_line": "ho no-68,bhati mkt,main dadri road,surajpur",
    "city": "Noida",
    "country": "India",
    "pincode": 201301,
    "name": "Saurabh Shukla",
    "phone_number": "9540914499",
    "alternate_contact": "9090909090",
    "sms_contact": "9540914499"
  },
  "skus_attributes": [
    {
      "name": "Puma-Men-Black-Wirko-Xc-Casual-Shoes (Size: 8)",
      "client_sku_id": "SC45634",
      "price": 100,
      "brand": "Puma",
      "category": "Shoes",
      "return_reason": "Size Mismatch",
      "qc_required": "false",
      "qc_rules": [
        {
          "question": "Is product colour as per description ?",
          "is_mandatory": 1,
          "value": "Red"
        }
      ],
      "seller_details": {
        "regd_name": "Seller Name",
        "regd_address": "GST Regd address",
        "state": "Karnataka",
        "gstin": "36AAVCS6697K1Z4"
      },
      "taxes": {
        "cgst_amount": 0,
        "sgst_amount": 0,
        "igst_amount": 18,
        "total_tax_amount": 18
      },
      "hsn_code": "83294089",
      "invoice_id": "ADSf",
      "additional_details": {
        "color": "black",
        "size": 8,
        "sku_images": [
          "http://sku_image_url/1/",
          "http://sku_image_url/1/"
        ],
        "quantity": 3
      }
    }
  ]
}

def send_forward_request(data):
  return requests.post(url, json=data, headers={'Authorization': f'Token {token}'}).json()


def send_reverse_request(data):
  return requests.post(reverse_url, json=data, headers={'Authorization': f'Token {token}'}).json()
