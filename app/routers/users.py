from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    status,
    BackgroundTasks,
    Depends,
)
from app.models import (
    User,
    user_pydanticIn,
    user_pydantic,
    user_pydanticOut,
    user_pydanticUpdate,
    Transactions,
    Order,
    order_pydantic,
    OrderItem,
    order_pydantic,
    order_item_pydantic,
    product_pydantic,
    Product,
    user_push_token,
    UserPushToken,
    StoreSettings,
)
from app.utilities import (
    generate_password_hash,
    token_generator,
)
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import (
    get_current_user,
    get_current_active_user,
)
from pydantic import BaseModel
from typing import List
from datetime import datetime
import requests
import json


router = APIRouter(tags=["User"], prefix="/users")


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/token", response_model=Token)
async def generate_token(
    request_form: OAuth2PasswordRequestForm = Depends(),
):
    token = await token_generator(
        request_form.username, request_form.password
    )
    return {"access_token": token, "token_type": "bearer"}


@router.post(
    "/registration", response_model=user_pydanticOut
)
async def user_registration(
    user: user_pydanticIn,
    request: Request,
    background_tasks: BackgroundTasks,
):
    user_info = user.dict()
    user = await User.filter(
        email=user_info["email"]
    ).first()

    if user:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Account with this mail already exists",
        )
    user = await User.filter(
        username=user_info["username"]
    ).first()
    if user:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Account with this username already exists",
        )
    user_info["password"] = generate_password_hash(
        user_info["password"]
    )
    users_count = await User.all().count()
    if int(users_count) <= 50:
        user_info.update({"balance": 250})

    user_obj = await User.create(**user_info)
    new_user = await user_pydanticOut.from_tortoise_orm(
        user_obj
    )
    return new_user


@router.get("/me", response_model=user_pydanticOut)
async def user_login(
    current_user: user_pydanticOut = Depends(
        get_current_active_user
    ),
):
    return await user_pydanticOut.from_queryset_single(
        User.get(id=current_user.id)
    )


@router.put("/update", response_model=user_pydanticOut)
async def update_user(
    request: user_pydanticUpdate,
    current_user: user_pydanticOut = Depends(
        get_current_active_user
    ),
):
    former_user = await User.get(id=current_user.id)
    if not request.email == former_user.email:
        user = await User.filter(
            email=request.email
        ).first()
        if user:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail="Email belongs to another account",
            )
    if not request.username == former_user.username:
        user = await User.filter(
            username=request.username
        ).first()
        if user:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail="Username already in use",
            )
    await User.filter(id=current_user.id).update(
        **request.dict(exclude_unset=True)
    )
    return await user_pydanticOut.from_queryset_single(
        User.get(id=current_user.id)
    )


class OrderItemOut(BaseModel):
    id: str
    price: float
    quantity: int
    product: product_pydantic


class OrderOut(BaseModel):
    id: int
    receiver_name: str
    receiver_phone_number: str
    receiver_street_address: str
    receiver_city: str
    receiver_state: str
    amount: float
    payment_ref_id: str
    created_at: datetime
    status: str
    items: List[OrderItemOut]


@router.get("/orders", response_model=List[OrderOut])
async def get_user_orders(
    current_user: user_pydanticOut = Depends(
        get_current_active_user
    ),
):
    orders = (
        await Order.filter(user_id=current_user.id)
        .all()
        .order_by("-created_at")
    )
    new_orders = []
    for order in orders:
        order_details = (
            await order_pydantic.from_queryset_single(
                Order.get(id=order.id)
            )
        )
        order_details = order_details.dict()
        items = await OrderItem.filter(
            order_id=order.id
        ).all()
        new_items = []
        for item in items:
            item_details = await order_item_pydantic.from_queryset_single(
                OrderItem.get(id=item.id)
            )
            item_details = item_details.dict()
            product = await Product.get(id=item.product_id)
            item_details.update({"product": product})
            # print(product)
            new_items.append(item_details)
        order_details.update({"items": new_items})
        new_orders.append(order_details)
    return new_orders


@router.get("/add/push-token")
async def add_user_token(
    token: str,
    current_user: user_pydanticOut = Depends(
        get_current_active_user
    ),
):
    push_obj = await UserPushToken.get_or_none(
        user_id=current_user.id
    )
    if push_obj != None:
        await UserPushToken.filter(id=push_obj.id).update(
            push_token=token
        )
        return {
            "msg": "Token added successfully",
            "token": token,
        }

    push_obj = await UserPushToken.create(
        user_id=current_user.id, push_token=token
    )
    return {
        "msg": "Token added successfully",
        "token": token,
    }


@router.get("/push-token")
async def get_user_token(
    current_user: user_pydanticOut = Depends(
        get_current_active_user
    ),
):
    push_obj = await UserPushToken.get_or_none(
        user_id=current_user.id
    )
    return {"push_token": push_obj.push_token}


@router.get("/push-token")
async def get_user_token(
    current_user: user_pydanticOut = Depends(
        get_current_active_user
    ),
):
    push_obj = await UserPushToken.get_or_none(
        user_id=current_user.id
    )
    return {"push_token": push_obj.push_token}


@router.get("/fund")
async def fund_user(
    t_id: str,
    current_user: user_pydanticOut = Depends(
        get_current_active_user
    ),
):
    store_settings = await StoreSettings.first()
    secret_key = store_settings.secret_key
    transaction = await Transactions.get_or_none(
        transaction_id=t_id
    )
    if transaction:
        raise HTTPException(
            status_code=400,
            detail="Transaction has been recorded before",
        )
    headers = {"Authorization": f"Bearer {secret_key}"}
    r = requests.get(
        f"https://api.flutterwave.com/v3/transactions/{t_id}/verify",
        headers=headers,
    )
    r = r.json()
    transaction_id = t_id
    amount = r["data"]["amount"]
    status = r["status"]
    tx_ref = r["data"]["tx_ref"]
    user_id = current_user.id

    transaction_obj = await Transactions.create(
        transaction_id=transaction_id,
        status=status,
        tx_ref=tx_ref,
        user_id=user_id,
        amount=amount,
    )
    if status == "success":
        print("Successful transaction")
        new_balance = current_user.balance + float(amount)
        await User.filter(id=current_user.id).update(
            balance=new_balance
        )
        push_obj = await UserPushToken.get_or_none(
            user_id=current_user.id
        )
        push_token = push_obj.push_token
        data = {
            "to": push_token,
            "title": "Account funded successfully!!",
            "body": f"Your account has been funded with ₦{amount}!!",
            "data": json.dumps({"screen": "Profile"}),
        }
        r = requests.post(
            "https://exp.host/--/api/v2/push/send",
            data=data,
        )

    return transaction_obj
