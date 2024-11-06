from aiogram import types
import asyncpg
from aiogram.types import InputMediaPhoto

from config import DB_URL
from buttons import get_quantity_buttons, get_catr_buttons


async def view_cart(callback_query):
    user_id = callback_query.from_user.id
    conn = await asyncpg.connect(DB_URL)

    # Получаем все товары в корзине пользователя
    cart_items = await conn.fetch("""
        SELECT product_id, quantity
        FROM store_cartitem
        WHERE user_id = $1
    """, user_id)

    await conn.close()

    if cart_items:
        await callback_query.message.answer(f"Ваша корзина:", reply_markup=get_catr_buttons(cart_items))
    else:
        await callback_query.message.answer("Ваша корзина пуста.")


async def set_count(callback_query: types.CallbackQuery):
    MIN_ITEMS = 1
    MAX_ITEMS = 100
    quantity = int(callback_query.data.split(":")[1])
    product_id = int(callback_query.data.split(":")[2])

    if quantity < MIN_ITEMS:
        quantity = MIN_ITEMS
    elif quantity > MAX_ITEMS:
        quantity = MAX_ITEMS

    try:
        media = InputMediaPhoto(
            media=callback_query.message.photo[-1].file_id,
            caption=f"Укажите количество товаров:",  # todo: Должна передаваться инфа о товаре
        )

        await callback_query.message.edit_media(
            media=media,
            reply_markup=get_quantity_buttons(quantity, product_id)
        )
        await callback_query.answer()  # Закрываем уведомление, чтобы кнопка не зависала
    except:
        return


async def add_to_cart(callback_query):
    quantity = int(callback_query.data.split(":")[1])
    product_id = int(callback_query.data.split(":")[2])
    user_id = callback_query.from_user.id

    conn = await asyncpg.connect(DB_URL)
    await conn.execute("""
        INSERT INTO store_cartitem (user_id, product_id, quantity)
        VALUES ($1, $2, $3)
    """, user_id, product_id, quantity)
    await conn.close()

    await callback_query.message.answer(f"Вы добавили {quantity} товаров {product_id} в корзину. Вы {user_id}")
    # await callback_query.answer()  # Закрываем уведомление, чтобы кнопка не зависала


async def remove_from_cart(product_id):
    pass
    # user_id = callback_query.from_user.id

    # conn = await asyncpg.connect(DB_URL)
    # await conn.execute("""
    #     DELETE FROM store_cartitem
    #     WHERE user_id = $1 AND product_id = $2
    # """, user_id, product_id)
    # await conn.close()
