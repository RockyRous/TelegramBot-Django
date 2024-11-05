import asyncpg
from config import DB_URL


async def view_cart(callback_query):
    user_id = callback_query.from_user.id
    conn = await asyncpg.connect(DB_URL)

    # Получаем все товары в корзине пользователя
    cart_items = await conn.fetch("""
        SELECT ci.quantity, p.name 
        FROM store_cartitem ci
        JOIN store_product p ON ci.product_id = p.id
        WHERE ci.user_id = $1
    """, user_id)

    await conn.close()

    if cart_items:
        items = "\n".join([f"{item['name']} (x{item['quantity']})" for item in cart_items])
        await callback_query.message.answer(f"Ваша корзина:\n{items}")
    else:
        await callback_query.message.answer("Ваша корзина пуста.")


async def add_to_cart(user_id, product_id):
    conn = await asyncpg.connect(DB_URL)
    await conn.execute("""
        INSERT INTO store_cartitem (user_id, product_id, quantity)
        VALUES ($1, $2, 1)
        ON CONFLICT (user_id, product_id) DO UPDATE
        SET quantity = cart_items.quantity + 1
    """, user_id, product_id)
    await conn.close()


async def remove_from_cart(user_id, product_id):
    conn = await asyncpg.connect(DB_URL)
    await conn.execute("""
        DELETE FROM store_cartitem
        WHERE user_id = $1 AND product_id = $2
    """, user_id, product_id)
    await conn.close()
