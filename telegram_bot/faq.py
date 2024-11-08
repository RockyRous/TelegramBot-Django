from aiogram import types
from aiogram.types import InputMediaPhoto

from buttons import get_faq_buttons

faq_img = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQdWZDrTELsCUnHhN9CvT_uWv8hkY8qkn75Rw&s'


async def get_faq(callback_query: types.CallbackQuery) -> None:
    """ Вывод FAQ с кнопками """
    buttons = get_faq_buttons()
    text = f"FAQ:"

    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=faq_img,
            caption=text,
        ),
        reply_markup=buttons
    )