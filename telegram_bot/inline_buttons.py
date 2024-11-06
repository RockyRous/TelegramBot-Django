from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_menu_buttons() -> InlineKeyboardMarkup:
    """ Меню """
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


def get_categories_buttons(categories: dict) -> InlineKeyboardMarkup:
    """ Категории """
    buttons = []
    num = 0
    for category in categories:
        num += 1
        buttons.append([InlineKeyboardButton(
            text=f"{num}: {category['name']}",
            callback_data=f"category_{category['id']}"
        )])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_products_buttons(products: dict) -> InlineKeyboardMarkup:
    """ Товары """
    buttons = []
    num = 0
    for product in products:
        num += 1
        buttons.append([InlineKeyboardButton(
            text=f"{num}: {product['name']}",
            callback_data=f"product_{product['id']}"
        )])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_product_buttons(product: dict) -> InlineKeyboardMarkup:
    """ Кнопки одного товара """
    # todo: Сделать кнопки
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Добавить в корзину", callback_data="asd")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="asd")
        ],
        [
            InlineKeyboardButton(text="В меню", callback_data="asd")
        ]
    ])
    return keyboard

