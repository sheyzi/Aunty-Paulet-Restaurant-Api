from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.models import *
from app.routers import admin, users, products, orders

import cloudinary

app = FastAPI(title="Aunty Paulet Restaurant", version="1.0.0")

cloudinary.config(
    cloud_name="sheyzisilver",
    api_key="312279126699163",
    api_secret="T0RRpS0xn428dtqoEP3YWW8vv7Q",
    secure=True
)

app.include_router(
    users.router
)



app.include_router(
    orders.router
)

app.include_router(
    products.router
)

app.include_router(
    admin.router
)

register_tortoise(
    app,
    db_url="sqlite://data.db",
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True
)


TORTOISE_ORM = {
        "connections": {
            "default": "sqlite://data.db"
            },
        "apps": {
            "models": {
                "models": ["app.models", "aerich.models"],
                "default_connection": "default",
            },
        }
    }
