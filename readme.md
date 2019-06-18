# Order Process


- Create order from basket of current user `/flashdeal/api/order/`
- When the user make the full payment, POST that info to payment API (please put the payment response in the `meta` key)`/flashdeal/api/payment/`
- The Order will show up in admin dashboard for the team to check and process. `/admin/flashdeal/order/`
- The Admin will fill in the delivery info and packaging to pass to the delivery service. `/admin/flashdeal/order/`
- If succeed, the order status is as delivery service define 

All APIs as above is available on Postman collection shared with the team

# Authentication token process

- If the user is a normal user. Use phone registration API `/flashdeal/api/user/register/`. 
If return 200, the OTP will be send to the phone. User is created but not verified
- Check the OTP is valid with `/flashdeal/api/token/`. If valid, the response will return with a token to authenticate other API calls
- If the user is not register by phone. You can get the token by call `/flashdeal/api/token/create/`
- You can refresh the token by user API `/flashdeal/api/token/refresh/` (should call every day or just create a new one). With params:
```json
{
	"token": "the-token",
	"orig_iat": "1560879171" // the time stamp of the time you create the token.
}
```
