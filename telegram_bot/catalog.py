import asyncpg
from aiogram import types
from aiogram.types import URLInputFile, InputMediaPhoto

from config import DB_URL, default_img_url, default_img
from buttons import get_categories_buttons, get_products_buttons, get_product_buttons, get_menu_buttons

ITEMS_PER_PAGE = 5  # Кол-во для пагинации


async def get_categories(callback_query: types.CallbackQuery) -> None:
    """ Получение списка категорий с пагинацией """
    conn = await asyncpg.connect(DB_URL)
    try:
        # Получаем номер страницы из callback_data
        page = 1  # По умолчанию первая страница
        if callback_query.data.startswith('next_'):
            page = int(callback_query.data.split('_')[1]) + 1
        elif callback_query.data.startswith('prev_'):
            page = int(callback_query.data.split('_')[1]) - 1

        # Рассчитываем смещение для SQL-запроса
        offset = (page - 1) * ITEMS_PER_PAGE

        # Запрос на получение категории для текущей страницы
        categories = await conn.fetch("""
                    SELECT id, name FROM store_category
                    WHERE parent_category_id IS NULL
                    LIMIT $1 OFFSET $2
                """, ITEMS_PER_PAGE, offset)
    finally:
        await conn.close()

    if categories:
        buttons = get_categories_buttons(categories, page)
        text = f"Доступные категории (страница {page}):"
    else:
        buttons = get_menu_buttons()
        text = f"Нет доступных категорий"

    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=default_img,
            caption=text,
        ),
        reply_markup=buttons
    )


async def get_categories_or_products(callback_query: types.CallbackQuery) -> None:
    """ Получение списка подкатегорий или товаров с пагинацией """
    conn = await asyncpg.connect(DB_URL)
    categories = None
    products = None
    try:
        # Получаем ID категории из callback_data
        category_id = int(callback_query.data.split('_')[1])  # category_{id}

        # Пагинация для подкатегорий и товаров
        page = 1  # По умолчанию первая страница
        if callback_query.data.startswith('next_categories_'):
            page = int(callback_query.data.split('_')[2]) + 1
        elif callback_query.data.startswith('prev_categories_'):
            page = int(callback_query.data.split('_')[2]) - 1
        elif callback_query.data.startswith('next_products_'):
            page = int(callback_query.data.split('_')[2]) + 1
        elif callback_query.data.startswith('prev_products_'):
            page = int(callback_query.data.split('_')[2]) - 1

        # Рассчитываем смещение для SQL-запроса
        offset = (page - 1) * ITEMS_PER_PAGE

        # Получаем подкатегории для данной категории с пагинацией
        query = f"SELECT id, name FROM store_category WHERE parent_category_id = $1 LIMIT $2 OFFSET $3"
        categories = await conn.fetch(query, category_id, ITEMS_PER_PAGE, offset)

        if not categories:
            # Если нет подкатегорий, получаем товары для данной категории с пагинацией
            query = f"SELECT id, name FROM store_product WHERE category_id = $1 LIMIT $2 OFFSET $3"
            products = await conn.fetch(query, category_id, ITEMS_PER_PAGE, offset)
    finally:
        await conn.close()

    if categories:
        buttons = get_categories_buttons(categories, page)
        text = f"Доступные подкатегории (страница {page}):"
    elif products:
        buttons = get_products_buttons(products, page)
        text = f"Доступные товары (страница {page}):"
    else:
        buttons = get_menu_buttons()
        text = f"Ничего не найдено :С"

    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=default_img,
            caption=text,
        ),
        reply_markup=buttons
    )


async def get_product(callback_query: types.CallbackQuery) -> None:
    """ Получаем карточку продукта """
    conn = await asyncpg.connect(DB_URL)
    try:
        query = "SELECT * FROM store_product where id = $1"
        product_id = int(callback_query.data.split('_')[1])  # product_{id}
        product = await conn.fetch(query, product_id)
    finally:
        await conn.close()

    if product:
        product = product[0]
        buttons = get_product_buttons(product)
        if product['image_url']:
            try:
                photo = URLInputFile(product['image_url'])
            except:
                photo = URLInputFile(default_img_url)
        else:
            photo = URLInputFile(default_img_url)

        text = f"{product['name']}\n{product['description']}\n{product['price']}"
    else:
        buttons = get_menu_buttons()
        photo = default_img
        text = f"Случилась ошибка"

    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=photo,
            caption=text,
        ),
        reply_markup=buttons
    )









