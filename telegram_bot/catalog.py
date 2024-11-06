import os

import asyncpg
from aiogram.types import FSInputFile, BufferedInputFile, URLInputFile

from config import DB_URL
from inline_buttons import get_categories_buttons, get_products_buttons, get_product_buttons


async def get_categories(callback_query):
    # todo: надо сделать пагинацию
    conn = await asyncpg.connect(DB_URL)
    try:
        categories = await conn.fetch("SELECT id, name FROM store_category where parent_category_id is null")
    finally:
        await conn.close()

    if categories:
        category_buttons = get_categories_buttons(categories)
        await callback_query.message.answer(f"Доступные категории:", reply_markup=category_buttons)
    else:
        await callback_query.message.answer(f"Нет категорий")


async def get_categories_or_products(callback_query):
    # todo: надо сделать пагинацию
    conn = await asyncpg.connect(DB_URL)
    categories = None
    products = None
    try:
        # Получаем подкатегории
        category_id = int(callback_query.data.split('_')[1])  # category_{id}
        query = f"SELECT id, name FROM store_category where parent_category_id = $1"
        categories = await conn.fetch(query, category_id)

        if not categories:
            # Получаем продукты
            query = "SELECT * FROM store_product where category_id = $1"
            products = await conn.fetch(query, category_id)
            print(products)
    finally:
        await conn.close()

    if categories:
        category_buttons = get_categories_buttons(categories)
        await callback_query.message.answer(f"Доступные подкатегории:", reply_markup=category_buttons)
    elif products:
        products_buttons = get_products_buttons(products)
        await callback_query.message.answer(f"Доступные товары:", reply_markup=products_buttons)
    else:
        await callback_query.message.answer(f"Ничего не найдено :С")


async def get_product(callback_query):
    conn = await asyncpg.connect(DB_URL)
    try:
        query = "SELECT * FROM store_product where id = $1"
        product_id = int(callback_query.data.split('_')[1])  # product_{id}
        product = await conn.fetch(query, product_id)
    finally:
        await conn.close()

    if product:
        product = product[0]
        product_buttons = get_product_buttons(product)
        if product['image'] and os.path.isfile(f'/code/media/{product["image"]}'):
            photo = FSInputFile(f'/code/media/{product['image']}')
        else:
            photo = URLInputFile('https://серебро.рф/img/placeholder.png')
        await callback_query.message.answer_photo(
            photo=photo,
            caption=f"{product['name']}\n{product['description']}\n{product['price']}",
            reply_markup=product_buttons
        )
    else:
        await callback_query.message.answer(f"Случилась ошибка")









