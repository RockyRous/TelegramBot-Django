from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


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
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Добавить в корзину", callback_data=f"quantity:1:{product['id']}")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="MakeMe")  # todo: Сделать кнопки
        ],
        [
            InlineKeyboardButton(text="В меню", callback_data="MakeMe")  # todo: Сделать кнопки
        ]
    ])
    return keyboard


def get_quantity_buttons(quantity: int, product: int) -> InlineKeyboardMarkup:
    """ Кнопки кол-ва товара """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➖", callback_data=f"quantity:{quantity - 1}:{product}"),
            InlineKeyboardButton(text=f"{quantity}", callback_data="ignore"),
            InlineKeyboardButton(text="➕", callback_data=f"quantity:{quantity + 1}:{product}")
        ],
        [
            InlineKeyboardButton(text="Добавить в корзину", callback_data=f"add_to_cart:{quantity}:{product}")
        ]
    ])
    return keyboard


def get_catr_buttons(items: dict) -> InlineKeyboardMarkup:
        """ Кнопки корзины """
        buttons = []
        num = 0
        for item in items:
            num += 1
            buttons.append([InlineKeyboardButton(
                text=f"{num}: {item['product_id']} | Кол-во: {item['quantity']} | Нажмите чтобы изменить",
                callback_data=f"asd"  # todo Сделать меню редактирования кол-ва и удаления
            )])

        buttons.append([InlineKeyboardButton(
            text=f"Оформление заказа",
            callback_data=f"start_order"
        )])

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard


def confirm_order_buttons():
    """ Кнопки подтверждения заказа """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подтвердить", callback_data="confirm_order"),
         InlineKeyboardButton(text="Отменить", callback_data="cancel_order")]
    ])



