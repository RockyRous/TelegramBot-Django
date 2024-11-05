import asyncpg
from config import DB_URL


async def get_categories(callback_query):
    # todo: Делать кнопки, по нажатию, проверять есть ли подкатегории при вызове или вызывать метод показа товаров
    conn = await asyncpg.connect(DB_URL)
    categories = await conn.fetch("SELECT id, name FROM store_category where parent_category_id is null")  # Измените на ваше имя таблицы
    await conn.close()
    if categories:
        category_buttons = "\n".join([f"{category['id']}: {category['name']}" for category in categories])
        await callback_query.message.answer(f"Доступные категории:\n{category_buttons}")
    else:
        await callback_query.message.answer(f"Нет категорий")

# todo: make get_products

