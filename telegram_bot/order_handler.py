from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import re

from buttons import get_menu_buttons, confirm_order_buttons
from cart import create_payment, create_order
from payments import YookassaGateway

router = Router()


# Состояния
class OrderForm(StatesGroup):
    name = State()
    phone = State()
    city = State()
    address = State()


@router.callback_query(F.data == 'start_order')
async def start_order(callback_query: types.CallbackQuery, state: FSMContext):
    """ Запуск заполнения данных """
    await callback_query.message.answer("Введите ваше имя и фамилию:")
    await state.set_state(OrderForm.name)


@router.message(OrderForm.name)
async def enter_name(message: types.Message, state: FSMContext):
    """ Ввод имени и проверка на валидность """
    name = message.text.strip()
    if not re.match(r"^[a-zA-Zа-яА-ЯёЁ\s]{2,50}$", name):
        await message.answer(
            "Имя и фамилия должны содержать только буквы, быть длиной от 2 до 50 символов. Попробуйте снова.")
        return
    await state.update_data(name=name)

    # Кнопка для отправки номера телефона
    contact_button = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Отправить номер телефона", request_contact=True)]],
        resize_keyboard=True, one_time_keyboard=True
    )
    await message.answer("Введите ваш номер телефона или нажмите кнопку для отправки контакта:",
                         reply_markup=contact_button)
    await state.set_state(OrderForm.phone)


@router.message(OrderForm.phone)
async def enter_phone(message: types.Message, state: FSMContext):
    """ Ввод номера телефона """
    # Проверка, был ли отправлен контакт
    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text.strip()

    # Проверка номера телефона
    phone = re.sub(r"\D", "", phone)  # Удаляем все нечисловые символы
    if phone.startswith("8"):
        phone = "7" + phone[1:]
    elif not phone.startswith("7"):
        await message.answer("Номер телефона должен начинаться с 7 или 8. Попробуйте снова.")
        return
    if len(phone) != 11:
        await message.answer("Неверный формат номера телефона. Убедитесь, что введено 11 цифр после 7.")
        return

    await state.update_data(phone=phone)
    await message.answer("Введите ваш город:")
    await state.set_state(OrderForm.city)


@router.message(OrderForm.city)
async def enter_city(message: types.Message, state: FSMContext):
    """ Ввод города """
    city = message.text.strip()
    if not re.match(r"^[a-zA-Zа-яА-ЯёЁ\s-]{2,50}$", city):
        await message.answer("Название города должно содержать только буквы и быть длиной от 2 до 50 символов.")
        return
    await state.update_data(city=city)
    await message.answer("Введите ваш адрес, включая почтовый индекс:")
    await state.set_state(OrderForm.address)


@router.message(OrderForm.address)
async def enter_address(message: types.Message, state: FSMContext):
    """ Ввод адреса и почтового индекса """
    address = message.text.strip()
    if len(address) < 5:
        await message.answer("Адрес должен быть длиной не менее 5 символов.")
        return

    await state.update_data(address=address)
    data = await state.get_data()

    # Подтверждение данных перед отправкой
    await message.answer(
        f"Проверьте ваши данные для доставки:\n\n"
        f"Имя и фамилия: {data['name']}\n"
        f"Телефон: {data['phone']}\n"
        f"Город: {data['city']}\n"
        f"Адрес: {data['address']}\n\n"
        "Подтвердите данные или отмените ввод.",
        reply_markup=confirm_order_buttons()
    )


@router.callback_query(F.data == "confirm_order")
async def confirm_order(callback_query: types.CallbackQuery, state: FSMContext):
    """ Обработка подтверждения заказа """
    data = await state.get_data()

    # Пробуем оплатить - выводим ссылку на оплату
    payment_url, payment_id, description = await create_payment(callback_query)
    await callback_query.message.answer(f"Ссылка для оплаты заказа:\n{description}\n{payment_url}")

    status = await YookassaGateway.check_payment_status(payment_id)
    if status == 'succeeded':
        print(f"Платёж {payment_id} прошёл удачно!")
        await create_order(callback_query, data)
        await callback_query.message.answer("Ваш заказ подтвержден и принят в обработку!",
                                            reply_markup=get_menu_buttons())
    elif status == 'canceled':
        print("Платёж был отменён.")
    else:
        print("Тайм-аут проверки статуса платежа.")

    # При неудаче предлагаем пробовать снова или отмена

    """
    Кажется тут ругается 
    TelegramBadRequest: Telegram server says - Bad Request: query is too old and response timeout expired or query ID is invalid
    Или там где идет оплата (врятли тк проходит всё до удаления корзины и выводит сообщение)
    Но мейби отваливается посередине
    """
    await state.clear()
    await callback_query.answer()


@router.callback_query(F.data == "cancel_order")
async def cancel_order(callback_query: types.CallbackQuery, state: FSMContext):
    """ Обработка отмены заказа """
    await state.clear()
    await callback_query.message.answer("Вы отменили заказ.", reply_markup=get_menu_buttons())
    await callback_query.answer()
