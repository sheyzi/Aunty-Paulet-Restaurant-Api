from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_active_user
from app.models import user_pydanticOut, user_pydanticIn, order_pydanticIn, OrderItemIn, Order, Product, User, order_pydantic, OrderItem, AdminPushToken, admin_push_token
import random
from typing import List
import requests
from app.repositories.user_repo import get_user_push_token
import json   

from app.repositories.user_repo import send_push_notification

router = APIRouter(tags=['Orders'])

@router.post('/order', response_model=order_pydantic)
async def order_product(order_details: order_pydanticIn, order_items: List[OrderItemIn] ,current_user: user_pydanticOut = Depends(get_current_active_user)):
	if order_details.amount > current_user.balance:
		raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Insufficient balance!! Please fund your account to complete your order!!")

	payment_ref_id = random.randint(10292, 1278376376)
	sum = 0
	for item in order_items:
		sum += item.price * item.quantity
	order_details = order_details.dict()
	order_details.update({"payment_ref_id": payment_ref_id})
	order_details.update({"user_id": current_user.id})
	order_details.update({"status":"PAID"})
	order_details['amount'] = sum + 500
	order_obj = await Order.create(**order_details)
	await order_obj.save()

	for item in order_items:
		item_details = item.dict()
		item_details.update({'order_id': order_obj.id})
		item_obj = await OrderItem.create(**item_details)
		await item_obj.save()
	
	user_info = await user_pydanticIn.from_queryset_single(User.get(id=current_user.id))
	user_info.balance = float(user_info.balance) - float(order_details["amount"])
	push_token = await get_user_push_token(current_user.id)
	data = {
	"to": push_token,
  	"title": "Order Successful!!",
  	"body": "Your order of ₦{:.2f} was Successful. You would be contacted shortly".format(order_obj.amount),
  	"data": json.dumps({"screen": "Profile"})
	}
	r = requests.post("https://exp.host/--/api/v2/push/send", data=data)
	r = r.json()
	print(r)

	admin_push_tokens = await 	admin_push_token.from_queryset(AdminPushToken.all())
	print(admin_push_tokens)
	push_tokens = []
	for tokens in admin_push_tokens:
		push_tokens.append(tokens.push_token)
	await send_push_notification(push_tokens, 'New Order', 'There is a new food order in Aunty Paulet Restaurant!!')
	await User.filter(id=current_user.id).update(**user_info.dict(exclude_unset=True))
	return await order_pydantic.from_queryset_single(Order.get(id=order_obj.id))
