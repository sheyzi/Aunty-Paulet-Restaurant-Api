from app.models import Product, Category


async def get_categories(skip: int = 0, limit: int = 100):
    return (
        await Category.all()
        .limit(limit)
        .offset(skip)
        .order_by("-date_created")
    )


async def get_products(skip: int = 0, limit: int = 100):
    return (
        await Product.all()
        .limit(limit)
        .offset(skip)
        .order_by("-date_created")
    )


async def get_product(slug: str):
    product = await Product.get_or_none(slug=slug)
    return product


async def get_category(slug: str):
    category = await Category.get_or_none(slug=slug)
    return category


async def get_products_with_category(slug: str):
    category = await Category.get(slug=slug)
    products = (
        await Product.filter(category_id=category.id)
        .all()
        .order_by("-date_created")
    )
    return products


async def get_product_with_query(query: str):
    return (
        await Product.filter(name__contains=query)
        .all()
        .order_by("-date_created")
    )


async def get_featured_products(
    skip: int = 0, limit: int = 4
):
    products = (
        await Product.filter(is_featured=True)
        .all()
        .limit(limit)
        .offset(skip)
        .order_by("-date_created")
    )
    return products
