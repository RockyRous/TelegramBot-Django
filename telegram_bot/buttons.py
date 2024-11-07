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


def get_categories_buttons(categories: list, page: int) -> InlineKeyboardMarkup:
    """ Категории """
    buttons = []
    num = 0
    for category in categories:
        num += 1
        buttons.append([InlineKeyboardButton(
            text=f"{num}: {category['name']}",
            callback_data=f"category_{category['id']}"
        )])

    # Кнопки навигации
    nav_buttons = []
    if page > 1:
        nav_buttons.insert(0, InlineKeyboardButton(text="Предыдущая", callback_data=f"prev_{page}"))
    nav_buttons.append(InlineKeyboardButton(text="Следующая", callback_data=f"next_{page}"))
    buttons.append(nav_buttons)

    buttons.append([InlineKeyboardButton(text="В меню", callback_data="menu")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_products_buttons(products: list, page: int) -> InlineKeyboardMarkup:
    """ Товары """
    buttons = []
    num = 0
    for product in products:
        num += 1
        buttons.append([InlineKeyboardButton(
            text=f"{num}: {product['name']}",
            callback_data=f"product_{product['id']}"
        )])

    # Кнопки навигации
    nav_buttons = []
    if page > 1:
        nav_buttons.insert(0, InlineKeyboardButton(text="Предыдущая", callback_data=f"prev_products_{page}"))
    nav_buttons.append(InlineKeyboardButton(text="Следующая", callback_data=f"next_products_{page}"))

    buttons.append(nav_buttons)
    buttons.append([InlineKeyboardButton(text="В меню", callback_data="menu")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_product_buttons(product: dict) -> InlineKeyboardMarkup:
    """ Кнопки одного товара """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Добавить в корзину", callback_data=f"quantity:1:{product['id']}")
        ],
        [
            InlineKeyboardButton(text="В меню", callback_data="menu")
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
        ],
        [
            InlineKeyboardButton(text="В меню", callback_data="menu")
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
                text=f"{num}: {item['name']} | Кол-во: {item['quantity']} | {item['quantity'] * item['price']} | Нажмите чтобы изменить",
                callback_data=f"asd"  # todo Сделать меню редактирования кол-ва и удаления
            )])  # todo: Добавить кнопку с очищением корзины

        buttons.append([InlineKeyboardButton(text=f"Оформление заказа", callback_data=f"start_order")])
        buttons.append([InlineKeyboardButton(text="В меню", callback_data="menu")])

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard


def confirm_order_buttons():
    """ Кнопки подтверждения заказа """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подтвердить", callback_data="confirm_order"),
         InlineKeyboardButton(text="Отменить", callback_data="cancel_order")]
    ])


def get_faq_buttons() -> InlineKeyboardMarkup:
    """ Кнопки FAQ """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="В меню", callback_data="menu")
        ]
    ])
    return keyboard


