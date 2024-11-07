from datetime import datetime

from aiogram import types
import asyncpg
from aiogram.types import InputMediaPhoto

from config import DB_URL, default_img
from buttons import get_quantity_buttons, get_catr_buttons, get_menu_buttons
from payments import YookassaGateway


async def get_cart(user_id) -> dict:
    """ Получаем все товары в корзине пользователя, включая информацию о продукте """
    conn = await asyncpg.connect(DB_URL)
    try:
        cart_items = await conn.fetch("""
                SELECT ci.product_id, ci.quantity, p.name, p.description, p.price
                FROM store_cartitem ci
                JOIN store_product p ON ci.product_id = p.id
                WHERE ci.user_id = $1
            """, user_id)
    finally:
        await conn.close()
    return cart_items


async def add_telegram_user(user_id: int) -> None:
    query_check_user = """
    SELECT user_id FROM store_telegramuser WHERE user_id = $1;
    """
    query_insert_user = """
    INSERT INTO store_telegramuser (user_id) 
    VALUES ($1);
    """

    conn = await asyncpg.connect(DB_URL)
    try:
        # Проверяем, существует ли уже пользователь в базе данных
        result = await conn.fetch(query_check_user, user_id)

        if not result:  # Если пользователя нет в базе
            await conn.execute(query_insert_user, user_id)
            print(f"User {user_id} added to the database.")
        else:
            print(f"User {user_id} already exists in the database.")
    finally:
        await conn.close()


async def view_cart(callback_query):
    user_id = callback_query.from_user.id
    await add_telegram_user(user_id)
    cart_items = await get_cart(user_id)

    if cart_items:
        buttons = get_catr_buttons(cart_items)
        text = f"Ваша корзина:"
    else:
        buttons = get_menu_buttons()
        text = "Ваша корзина пуста."

    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=default_img,
            caption=text,
        ),
        reply_markup=buttons
    )


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
            caption=f"Укажите количество товаров:",
        )

        await callback_query.message.edit_media(
            media=media,
            reply_markup=get_quantity_buttons(quantity, product_id)
        )
        await callback_query.answer()
    except:
        return


async def add_to_cart(callback_query):
    quantity = int(callback_query.data.split(":")[1])
    product_id = int(callback_query.data.split(":")[2])
    user_id = callback_query.from_user.id

    conn = await asyncpg.connect(DB_URL)
    try:
        await conn.execute("""
            INSERT INTO store_cartitem (user_id, product_id, quantity)
            VALUES ($1, $2, $3)
        """, user_id, product_id, quantity)
    finally:
        await conn.close()

    buttons = get_menu_buttons()
    text = f"Вы добавили ({quantity}) товаров в корзину."
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=default_img,
            caption=text,
        ),
        reply_markup=buttons
    )


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
    """ Удаляем все товары из корзины пользователя """
    conn = await asyncpg.connect(DB_URL)

    try:
        await conn.execute("""
            DELETE FROM store_cartitem
            WHERE user_id = $1
        """, user_id)
    finally:
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
    try:
        await conn.execute("""
            INSERT INTO store_order (user_id, user_data, created_at, total_price, status)
            VALUES ($1, $2, $3, $4, $5)
        """, user_id, user_data, created_at, total_price, status)
    finally:
        await conn.close()

    await clear_cart(user_id)


async def get_cart_item(id_cartitem: int):
    """ Получение позиции из корзины """
    # TODO делать джоин с продуктом
    conn = await asyncpg.connect(DB_URL)
    try:
        query = "SELECT * FROM store_cartitem WHERE id = $1;"
        result = await conn.fetch(query, id_cartitem)
    finally:
        await conn.close()

    return result


async def change_cart_item(callback_query, id_cartitem: int):
    """ Изменения кол-ва и удаление продукта из корзины """
    cartitem = await get_cart_item(id_cartitem)

    buttons = get_menu_buttons()
    text = f"Ваш товар"
    img = ''
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=img,
            caption=text,
        ),
        reply_markup=buttons
    )
    # Выводим инфо о позиции и клаву
    # Клава: изменить кол-во (подхватывает текущее кол-во), сохранить, удалить позицию, В меню


async def update_cart_item_quantity(cartitem_id: int, quantity: int) -> None:
    """ Обновляем количество для указанного товара в корзине пользователя """
    conn = await asyncpg.connect(DB_URL)
    try:
        await conn.execute("""
            UPDATE store_cartitem
            SET quantity = $1
            WHERE id = $2
        """, quantity, cartitem_id)
    finally:
        await conn.close()






