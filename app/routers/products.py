from app.dependencies import get_current_active_user
from fastapi import APIRouter, status, HTTPException, Depends
from app.models import product_pydantic, category_pydantic, user_pydanticOut, StoreSettings, store_settings_pydantic
from typing import List
from app.repositories.product_repo import get_categories, get_featured_products, get_products, get_category, get_product, get_product_with_query, get_products_with_category


router = APIRouter(tags=['Products'])


@router.get('/products', response_model=List[product_pydantic])
async def get_all_products(skip: int = 0, limit: int = 100):
    products = await get_products(skip, limit)
    return products



@router.get('/products/featured', response_model=List[product_pydantic])
async def get_all_featured_products(skip: int = 0, limit: int = 8):
    products = await get_featured_products(skip, limit)
    return products


@router.get('/categories', response_model=List[category_pydantic])
async def get_all_categories(skip: int = 0, limit: int = 100):
    return await get_categories(skip, limit)


@router.get('/categories/{slug}', response_model=category_pydantic)
async def get_category_by_slug(slug: str):
    category = await get_category(slug)
    if not category:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Category with slug '{slug}' doesn't exists")
    return category


@router.get('/categories/{slug}/products', response_model=List[product_pydantic])
async def get_category_products(slug: str):
    category = await get_category(slug)
    if not category:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Category with slug '{slug}' doesn't exists")
    products = await get_products_with_category(slug)
    return products


@router.get('/products/search', response_model=List[product_pydantic])
async def search_products(q: str):
    return await get_product_with_query(query=q)


@router.get('/products/{slug}', response_model=product_pydantic)
async def get_product_by_slug(slug: str):
    product = await get_product(slug)
    if not product:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Product with slug '{slug}' doesn't exists")
    return product

@router.get('/encryption-key')
async def get_encryption_key(current_user: user_pydanticOut = Depends(get_current_active_user)):
    settings = await StoreSettings.first()
    return settings

