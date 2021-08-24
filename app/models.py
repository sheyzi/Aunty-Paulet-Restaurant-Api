from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel
from enum import Enum


class User(Model):
    id = fields.IntField(pk=True, index=True)
    username = fields.CharField(
        max_length=200, null=False, unique=True
    )
    email = fields.CharField(
        max_length=200, null=False, unique=True
    )
    password = fields.CharField(max_length=255, null=False)
    is_active = fields.BooleanField(default=True)
    is_admin = fields.BooleanField(default=False)
    join_date = fields.DatetimeField(auto_now_add=True)
    balance = fields.FloatField(default=0.0)

    def __str__(self) -> str:
        return self.username


class Category(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=20, null=False)
    slug = fields.CharField(
        max_length=50, unique=True, null=False
    )
    image_url = fields.CharField(
        max_length=500,
        null=False,
        default="https://res.cloudinary.com/sheyzisilver/image/upload/v1628729409/placeholder_rl2wsr.png",
    )
    date_created = fields.DatetimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class UserPushToken(Model):
    id = fields.IntField(pk=True, index=True)
    user = fields.OneToOneField(
        "models.User",
        related_name="token",
        on_delete=fields.CASCADE,
    )
    push_token = fields.CharField(max_length=255)


class AdminPushToken(Model):
    id = fields.IntField(pk=True, index=True)
    user = fields.OneToOneField(
        "models.User",
        related_name="adminToken",
        on_delete=fields.CASCADE,
    )
    push_token = fields.CharField(max_length=255)


class Product(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=50, null=False)
    category = fields.ForeignKeyField(
        "models.Category",
        related_name="products",
        on_delete=fields.CASCADE,
    )
    slug = fields.CharField(
        max_length=60, unique=True, null=False
    )
    description = fields.TextField(null=False)
    price = fields.FloatField(null=False)
    image_url = fields.CharField(
        max_length=500,
        null=False,
        default="https://res.cloudinary.com/sheyzisilver/image/upload/v1628729409/placeholder_rl2wsr.png",
    )
    is_featured = fields.BooleanField(default=False)
    date_created = fields.DatetimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class StatusChoice(Enum):
    PAID = "PAID"
    PENDING_PAYMENT = "PENDING_PAYMENT"
    DELIVERED = "DELIVERED"


class Order(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(
        "models.User",
        related_name="orders",
        on_delete=fields.RESTRICT,
    )
    receiver_name = fields.CharField(max_length=100)
    receiver_phone_number = fields.CharField(max_length=12)
    receiver_street_address = fields.TextField()
    receiver_city = fields.CharField(
        max_length=20, default="Ikorodu"
    )
    receiver_state = fields.CharField(
        max_length=20, default="Lagos"
    )
    amount = fields.FloatField()
    payment_ref_id = fields.CharField(max_length=150)
    created_at = fields.DatetimeField(auto_now_add=True)
    status = fields.CharField(
        max_length=30, default="PENDING_PAYMENT"
    )

    def __str__(self) -> str:
        return self.receiver_name


class OrderItem(Model):
    id = fields.IntField(pk=True)
    order = fields.ForeignKeyField(
        "models.Order",
        related_name="items",
        on_delete=fields.CASCADE,
    )
    product = fields.ForeignKeyField(
        "models.Product",
        related_name="items",
        on_delete=fields.RESTRICT,
    )
    price = fields.FloatField()
    quantity = fields.IntField()

    def __str__(self) -> str:
        return self.product.name


class StoreSettings(Model):
    id = fields.IntField(pk=True)
    encryption_key = fields.CharField(max_length=500)
    public_key = fields.CharField(
        max_length=500,
        default="FLWPUBK-8d86cd80110eab28ded75457e92d47f4-X",
    )
    secret_key = fields.CharField(
        max_length=500,
        default="FLWSECK-7df341197189906ab0dd5c045b057216-X",
    )
    delivery_fee = fields.IntField(default=500)


class Transactions(Model):
    transaction_id = fields.IntField(pk=True)
    status = fields.CharField(max_length=20)
    amount = fields.CharField(max_length=10)
    tx_ref = fields.CharField(max_length=30)
    user = fields.ForeignKeyField(
        "models.User",
        related_name="transactions",
        on_delete=fields.RESTRICT,
    )


user_pydantic = pydantic_model_creator(User, name="User")
user_pydanticIn = pydantic_model_creator(
    User,
    name="UserIn",
    exclude_readonly=True,
    exclude=("is_active", "is_admin"),
)
user_pydanticUpdate = pydantic_model_creator(
    User,
    name="UserUpdate",
    exclude_readonly=True,
    exclude=(
        "is_active",
        "is_admin",
        "password",
        "balance",
    ),
)
user_pydanticOut = pydantic_model_creator(
    User, name="UserOut", exclude=("password",)
)

category_pydantic = pydantic_model_creator(
    Category, name="Category"
)
category_pydanticIn = pydantic_model_creator(
    Category, name="CategoryIn", exclude_readonly=True
)
category_pydanticUpdate = pydantic_model_creator(
    Category,
    name="CategoryUpdate",
    exclude_readonly=True,
    exclude=("image_url",),
)

product_pydantic = pydantic_model_creator(
    Product, name="Product"
)
product_pydanticIn = pydantic_model_creator(
    Product, name="ProductIn", exclude_readonly=True
)
product_pydanticUpdate = pydantic_model_creator(
    Product,
    name="ProductUpdate",
    exclude_readonly=True,
    exclude=("image_url",),
)

order_pydantic = pydantic_model_creator(Order, name="Order")
order_pydanticIn = pydantic_model_creator(
    Order,
    name="OrderIn",
    exclude_readonly=True,
    exclude=("payment_ref_id",),
)

order_item_pydantic = pydantic_model_creator(
    OrderItem, name="OrderItem"
)
order_item_pydanticIn = pydantic_model_creator(
    OrderItem, name="OrderItemIn", exclude_readonly=True
)

user_push_token = pydantic_model_creator(
    UserPushToken, name="UserPushToken"
)
admin_push_token = pydantic_model_creator(
    AdminPushToken, name="AdminPushToken"
)
store_settings_pydantic = pydantic_model_creator(
    StoreSettings, name="StoreSettings"
)
store_settings_pydanticIn = pydantic_model_creator(
    StoreSettings,
    name="StoreSettingsIn",
    exclude_readonly=True,
)


class OrderItemIn(BaseModel):
    product_id: int
    price: float
    quantity: int
