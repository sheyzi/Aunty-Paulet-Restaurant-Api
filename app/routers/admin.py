from fastapi import APIRouter, Depends, UploadFile, HTTPException, File
from starlette import status
from app.dependencies import get_admin_user
from app.repositories.user_repo import get_users
from app.repositories.product_repo import get_products, get_categories
from typing import List
from app.models import (Category,
                        user_pydanticOut,
                        product_pydantic,
                        product_pydanticIn,
                        Product,
                        category_pydantic,
                        category_pydanticIn,
                        category_pydanticUpdate,
                        product_pydanticUpdate,
                        UserPushToken, User)
from app.utilities import save_file
import json
import requests

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get('/users', response_model=List[user_pydanticOut])
async def get_all_users(skip: int = 0, limit: int = 100, current_user: user_pydanticOut = Depends(get_admin_user)):
    users = await get_users(skip=skip, limit=limit)
    return users


@router.get('/categories', response_model=List[category_pydantic])
async def get_all_categories(skip: int = 0, limit: int = 100, current_user: user_pydanticOut = Depends(get_admin_user)):
    return await get_categories(skip, limit)


@router.get('/products', response_model=List[product_pydantic])
async def get_all_products(skip: int = 0, limit: int = 100, current_user: user_pydanticOut = Depends(get_admin_user)):
    products = await get_products(skip, limit)
    return products


@router.post('/categories/add', response_model=category_pydantic)
async def add_category(request: category_pydanticIn, current_user: user_pydanticOut = Depends(get_admin_user)):
    category_info = request.dict()
    category = await Category.filter(slug=category_info["slug"]).first()
    if category:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail=f"Category with slug '{request.slug}' already exists!")
    category_obj = await Category.create(**category_info)
    return await category_pydantic.from_queryset_single(Category.get(id=category_obj.id))


@router.post('/categories/{id}/image', response_model=category_pydantic)
async def add_category_image(id: int, file: UploadFile = File(...), current_user: user_pydanticOut = Depends(get_admin_user)):
    category = await Category.get_or_none(id=id)
    if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Category with id '{id}' doesn't exist")
    url = await save_file(file)
    category_info = await category_pydanticIn.from_queryset_single(
        Category.get(id=id))
    category_info.image_url = url
    await Category.filter(id=id).update(**category_info.dict(exclude_unset=True))
    return await category_pydantic.from_queryset_single(Category.get(id=id))


@router.put('/categories/{id}/update', response_model=category_pydantic)
async def update_category(id: int, request: category_pydanticUpdate, current_user: user_pydanticOut = Depends(get_admin_user)):
    category = await Category.get_or_none(id=id)
    if not category:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Category with id {id} doesn't exists")
    if not request.slug == category.slug:
        category = await Category.filter(slug=request.slug).first()
        if category:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail=f"Slug '{category.slug}' cannot be used twice")
    await Category.filter(id=id).update(**request.dict(exclude_unset=True))
    return await category_pydantic.from_queryset_single(Category.get(id=id))


@router.post('/products/add', response_model=product_pydantic)
async def add_products(category_id: int, request: product_pydanticIn, current_user: product_pydantic = Depends(get_admin_user)):
    product_info = request.dict()
    product = await Product.filter(slug=product_info['slug']).first()
    category = await Category.get_or_none(id=category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Category with id {category_id} doesn't exists")
    if product:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail=f"Product with slug '{product_info['slug']}' already exists ")
    product_info.update({'category_id': category_id})
    product_obj = await Product.create(**product_info)
    await product_obj.save()
    push_tokens = await UserPushToken.all()
    generated_push_tokens= []
    for push_token in push_tokens:
        generated_push_tokens.append(push_token.push_token)
    data = {
    "to": generated_push_tokens,
    "title": "New Menu Item!!",
    "body": f"Checkout {product_obj.name}!! It was added to the stores menu recently!!",
    "data": json.dumps({"screen": "ProductDetails", "screen_params": {"name": f"{product_obj.name}", "slug": f"{product_obj.slug}"}})
    }
    r = requests.post("https://exp.host/--/api/v2/push/send", data=data)
    
    return await product_pydantic.from_queryset_single(Product.get(id=product_obj.id))


@router.post('/products/{id}/image', response_model=product_pydantic)
async def add_product_image(id: int, file: UploadFile = File(...), current_user: user_pydanticOut = Depends(get_admin_user)):
    product = await Product.get_or_none(id=id)
    if not product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Product with id '{id}' doesn't exist")
    url = await save_file(file)
    product_info = await product_pydanticIn.from_queryset_single(
        Product.get(id=id))
    product_info.image_url = url
    await Product.filter(id=id).update(**product_info.dict(exclude_unset=True))
    return await product_pydantic.from_queryset_single(Product.get(id=id))


@router.put('/products/{id}/update', response_model=product_pydantic)
async def update_product(id: int, request: product_pydanticUpdate, current_user: user_pydanticOut = Depends(get_admin_user)):
    product = await Product.get_or_none(id=id)
    if not product:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Product with id {id} doesn't exists")
    if not request.slug == product.slug:
        product = await Product.filter(slug=request.slug).first()
        if product:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail=f"Slug '{product.slug}' cannot be used twice")
    await Product.filter(id=id).update(**request.dict(exclude_unset=True))
    return await product_pydantic.from_queryset_single(Product.get(id=id))

