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
    db_url="postgres://zwehbhhckpamxf:74a818468b29c9806d05b39f23fe5c2734033fa44aefd4854c559713482c63ad@ec2-54-159-35-35.compute-1.amazonaws.com:5432/dc42ggsmv5fpha",
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True
)


TORTOISE_ORM = {
        "connections": {
            "default": "postgres://zwehbhhckpamxf:74a818468b29c9806d05b39f23fe5c2734033fa44aefd4854c559713482c63ad@ec2-54-159-35-35.compute-1.amazonaws.com:5432/dc42ggsmv5fpha"
            },
        "apps": {
            "models": {
                "models": ["app.models", "aerich.models"],
                "default_connection": "default",
            },
        }
    }
