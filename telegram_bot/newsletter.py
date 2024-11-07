import asyncpg
import asyncio
from aiogram.enums import ParseMode

from config import DB_URL


async def get_users(conn):
    """Получаем всех пользователей"""
    query = "SELECT user_id FROM store_telegramuser"
    return await conn.fetch(query)


async def get_unsent_newsletters(conn):
    """Получаем все неотправленные рассылки."""
    query = "SELECT id, title, content FROM store_newsletter WHERE is_sent = FALSE"
    return await conn.fetch(query)


async def send_newsletter(bot):
    """Отправка рассылки всем пользователям."""
    conn = await asyncpg.connect(DB_URL)

    try:
        # Получаем неотправленные рассылки
        newsletters = await get_unsent_newsletters(conn)

        if newsletters:
            # Получаем всех пользователей
            users = await get_users(conn)

            for newsletter in newsletters:
                # Отправляем рассылку каждому пользователю
                for user in users:
                    try:
                        await bot.send_message(
                            user['user_id'],
                            f"<b>{newsletter['title']}</b>\n\n{newsletter['content']}",
                            parse_mode=ParseMode.HTML
                        )
                        print(f"Рассылка '{newsletter['title']}' отправлена пользователю {user['user_id']}")
                    except Exception as e:
                        print(f"Не удалось отправить сообщение пользователю {user['user_id']}: {e}")

                # После отправки рассылки помечаем ее как отправленную
                update_query = "UPDATE store_newsletter SET is_sent = TRUE WHERE id = $1"
                await conn.execute(update_query, newsletter['id'])
                print(f"Рассылка '{newsletter['title']}' отправлена всем юзерам")

    finally:
        await conn.close()


async def scheduled_newsletter(bot):
    """ Задача, которая будет запускать рассылку """
    print('Процесс рассылки запущен')
    while True:
        await send_newsletter(bot)
        await asyncio.sleep(60 * 10)  # Пауза 10 минут


