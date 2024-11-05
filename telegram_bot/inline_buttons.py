from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Каталог", callback_data="catalog")
        ],
        [
            InlineKeyboardButton(text="Корзина", callback_data="cart")
        ],
        [
            InlineKeyboardButton(text="FAQ", callback_data="faq")
        ]
    ])
    return keyboard
