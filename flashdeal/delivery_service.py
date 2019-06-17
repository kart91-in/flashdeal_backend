import requests
from django.conf import settings

url = 'http://saruman.staging.shadowfax.in/api/v1/clients/requests'

# sample_request = {
#     "client_order_id": "66967604933444",
#     "awb_number": "SFXE220250035SK",
#
#     "actual_weight": 100,
#     "volumetric_weight": 100,
#     "order_service": "NDD",
#
#     "pincode": 110009,
#     "customer_name": "javed",
#     "customer_phone": "909090990",
#     "alternate_customer_contact": "9090909090",
#     "customer_address": "5811 Jones Street Londonderry, NH 03053",
#     "address_type": "home",
#     "c_city": "Okhla",
#     "c_state": "New Delhi",
#
#     "declared_value": 1000,
#     "total_amount": 900,
#     "cod_amount": 0,
#     "deliver_type": "COD",
#
#     "pickup_address_attributes": {
#         "address": "Khasra No. 93/5 94/1 Phirni Road Vill- Mundka New Delhi Delhi",
#         "pincode": 122001
#     },
#     "rto_attributes": {
#         "name": "Rishav Telecom",
#         "city": "Ludhiana",
#         "state": "Punjab",
#         "contact_no": "9089898789",
#         "address": "sec-24 poc-25 Hno-76 Shiv mandir",
#         "pincode": 110009
#     },
#     "skus_attributes": [
#         {
#             "product_name": "xyz",
#             "client_sku_id": "12321",
#             "price": 100,
#             "product_category": "Footwear",
#             "product_subcategory": "Women's shoe",
#             "brand_name": "Nike",
#             "volumetric_weight": 122,
#             "box_type": "box",
#             "product_sale_value": 234,
#             "additional_details": {
#                 "color": "blue",
#                 "size": 9
#             },
#             "seller_details": {
#                 "seller_name": "Seller Name",
#                 "seller_address": "GST Regd address",
#                 "seller_state": "Karnataka",
#                 "gstin_number": "36AAVCS6697K1Z4"
#             },
#             "taxes": {
#                 "cgst": 0,
#                 "sgst": 0,
#                 "igst": 18,
#                 "total_tax": 18
#             },
#             "hsn_code": "83294089",
#             "invoice_no": "ADSf"
#         },
#         {
#             "product_name": "abc",
#             "client_sku_id": "1234",
#             "price": 120,
#             "product_category": "Clothing",
#             "product_subcategory": "Men's shirt",
#             "brand_name": "Puma",
#             "volumetric_weight": 123,
#             "box_type": "box",
#             "product_sale_value": 12345,
#             "additional_details": {
#                 "color": "blue",
#                 "size": 9
#             },
#             "seller_details": {
#                 "seller_name": "Seller Name",
#                 "seller_address": "GST Regd address",
#                 "seller_state": "Karnataka",
#                 "gstin_number": "36AAVCS6697K1Z4"
#             },
#             "taxes": {
#                 "cgst": 0,
#                 "sgst": 0,
#                 "igst": 18,
#                 "total_tax": 18
#             },
#             "hsn_code": "83294089",
#             "invoice_no": "ADSf"
#         }
#     ]
# }

def send_forward_request(data):
    return requests.post(url, json=data, headers={'Authorization': f'Token 51b4c7633d583a9474b147187fb1e1498d22e6ad'}).json()
