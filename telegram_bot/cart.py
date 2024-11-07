from datetime import datetime

from aiogram import types
import asyncpg
from aiogram.types import InputMediaPhoto

from config import DB_URL
from buttons import get_quantity_buttons, get_catr_buttons
from payments import YookassaGateway

# todo позаворачивать всё в трай

async def get_cart(user_id) -> dict:
    conn = await asyncpg.connect(DB_URL)
    # Получаем все товары в корзине пользователя, включая информацию о продукте
    cart_items = await conn.fetch("""
            SELECT ci.product_id, ci.quantity, p.name, p.description, p.price
            FROM store_cartitem ci
            JOIN store_product p ON ci.product_id = p.id
            WHERE ci.user_id = $1
        """, user_id)
    await conn.close()
    return cart_items


async def view_cart(callback_query):
    user_id = callback_query.from_user.id
    cart_items = await get_cart(user_id)

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


async def remove_from_cart(user_id: int, product_id: int) -> None:
    """ Удаляем указанный товар из корзины пользователя """
    conn = await asyncpg.connect(DB_URL)
    await conn.execute("""
        DELETE FROM store_cartitem
        WHERE user_id = $1 AND product_id = $2
    """, user_id, product_id)
    await conn.close()


async def update_cart_item_quantity(user_id: int, product_id: int, quantity: int) -> None:
    """ Обновляем количество для указанного товара в корзине пользователя """
    conn = await asyncpg.connect(DB_URL)
    await conn.execute("""
        UPDATE store_cartitem
        SET quantity = $1
        WHERE user_id = $2 AND product_id = $3
    """, quantity, user_id, product_id)
    await conn.close()


async def create_payment(callback_query) -> tuple:
    """ пробуем оплатить """
    # Получаем корзину юзера
    user_id = callback_query.from_user.id
    cart_items = await get_cart(user_id)

    description = ''
    total_price = 0
    # Делаем список покупок и составляем прайс
    num = 0
    for item in cart_items:
        num += 1
        price = item['quantity'] * item['price']
        total_price += price
        description += f"{num}. {item['name']} | Кол-во: {item['quantity']} | {price}\n"
    description += f"Итоговая сумма: {total_price} RUB"

    gateway = YookassaGateway(amount=float(total_price), description=description)
    # Создаем платеж
    payment_url, payment_id = await gateway.create_payment()
    print(f"Ссылка на оплату: {payment_url} | Используйте карту 5555555555554477 и любые цифры для оплаты (дату больше текущей)")  # todo: delete
    return payment_url, payment_id, description


async def clear_cart(user_id: int) -> None:
    conn = await asyncpg.connect(DB_URL)

    # Удаляем все товары из корзины пользователя
    await conn.execute("""
        DELETE FROM store_cartitem
        WHERE user_id = $1
    """, user_id)

    await conn.close()


async def create_order(callback_query, data):
    """ Создание заказа """
    # Собираем данные
    user_id = callback_query.from_user.id
    items = await get_cart(user_id)
    total_price = 0
    for item in items:
        price = item['quantity'] * item['price']
        total_price += price
    user_data = f'{data.get("name")}__{data.get("phone")}__{data.get("city")}__{data.get("address")}'
    status = 'pending'
    created_at = datetime.now()  # Получаем текущее время

    # Записываем данные заказа в базу
    conn = await asyncpg.connect(DB_URL)
    await conn.execute("""
        INSERT INTO store_order (user_id, user_data, created_at, total_price, status)
        VALUES ($1, $2, $3, $4, $5)
    """, user_id, user_data, created_at, total_price, status)
    await conn.close()

    await clear_cart(user_id)









