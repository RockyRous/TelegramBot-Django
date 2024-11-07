import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ChatMember
import asyncio

from config import API_TOKEN, LOGGING_LEVEL, CHANNEL_ID
from buttons import get_menu_buttons
from router import router
from newsletter import scheduled_newsletter

# Настройка логирования
logging.basicConfig(level=LOGGING_LEVEL)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
dp.include_router(router)

# TODO: Хорошо бы сделать удаление старых сообщений


async def check_subscription(user_id: int):
    """ Функция для проверки подписки пользователя на канал """
    try:
        # Получаем информацию о статусе пользователя в чате
        chat_member = await bot.get_chat_member(CHANNEL_ID, user_id)

        # Проверяем статус пользователя
        if chat_member.status in [ChatMember.Status.MEMBER, ChatMember.Status.ADMINISTRATOR, ChatMember.Status.CREATOR]:
            return True
        return False
    except Exception as e:
        print(f"Error while checking subscription: {e}")
        return False


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать! Используйте /menu для доступа к функциям.")


@dp.message(Command("menu"))
async def cmd_menu(message: types.Message):
    # Проверяем подписку пользователя
    user_id = message.from_user.id
    is_subscribed = await check_subscription(user_id)

    if is_subscribed:
        await message.answer("Вы подписаны на канал!")
    else:
        await message.answer("Пожалуйста, подпишитесь на канал, чтобы продолжить!")

    # FROM DEBUG. Перенесите в выполнение if is_subscribed
    await message.answer("Выберите действие:", reply_markup=get_menu_buttons())


async def main():
    asyncio.create_task(scheduled_newsletter(bot))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.info("Starting bot...")
    asyncio.run(main())
