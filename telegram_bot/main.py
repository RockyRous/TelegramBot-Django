import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

from config import API_TOKEN, LOGGING_LEVEL, DB_URL
from inline_buttons import get_menu_buttons
from catalog import get_categories, get_categories_or_products, get_product
from cart import add_to_cart, view_cart, remove_from_cart

# Настройка логирования
logging.basicConfig(level=LOGGING_LEVEL)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать! Используйте /menu для доступа к функциям.")

@dp.message(Command("menu"))
async def cmd_menu(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=get_menu_buttons())


@dp.callback_query(lambda c: c.data == "catalog")
async def catalog_handler(callback_query: types.CallbackQuery):
    return await get_categories(callback_query)


@dp.callback_query(lambda c: c.data.startswith("category_"))
async def catalog_handler(callback_query: types.CallbackQuery):
    return await get_categories_or_products(callback_query)


@dp.callback_query(lambda c: c.data.startswith("product_"))
async def catalog_handler(callback_query: types.CallbackQuery):
    return await get_product(callback_query)


@dp.callback_query(lambda c: c.data == "cart")
async def cart_handler(callback_query: types.CallbackQuery):
    await view_cart(callback_query)


@dp.callback_query(lambda c: c.data == "faq")
async def cart_handler(callback_query: types.CallbackQuery):
    await view_cart(callback_query)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.info("Starting bot...")
    asyncio.run(main())
