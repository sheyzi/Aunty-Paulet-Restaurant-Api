from app.models import Product, User, user_pydanticOut, product_pydantic, UserPushToken


async def get_users(skip: int = 0, limit: int = 100):
    users = await User.all().limit(limit=limit).offset(skip)
    return users


async def get_products(skip: int = 0, limit: int = 100):
    products = await Product.all().limit(limit).offset(skip)
    return products

async def get_user_push_token(id):
    push_obj = await UserPushToken.get_or_none(user_id=id)
    return push_obj.push_token
