from app.models import Product, User, user_pydanticOut, product_pydantic, UserPushToken
from typing import List, Optional
import requests
import json


async def get_users(skip: int = 0, limit: int = 100):
    users = await User.all().limit(limit=limit).offset(skip)
    return users


async def get_products(skip: int = 0, limit: int = 100):
    products = await Product.all().limit(limit).offset(skip)
    return products

async def get_user_push_token(id):
    push_obj = await UserPushToken.get_or_none(user_id=id)
    return push_obj.push_token

async def send_push_notification(to: List, title, message, data: Optional[dict] = None):
    if data:

        data = {
                "to": to,
                "title": title,
                "body": message,
                "data": json.dumps(data)
        }
    else:

        data = {
                "to": to,
                "title": title,
                "body": message
             
            }
    print(to)
    r = requests.post("https://exp.host/--/api/v2/push/send", data=data)
    print(r.json())
