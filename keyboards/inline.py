from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🍹 Заказать коктейль", callback_data="order_recipe")],
        [InlineKeyboardButton(text="🥃 Из моего бара", callback_data="from_my_bar")],
        [InlineKeyboardButton(text="✨ Секретный ингредиент", callback_data="secret_ingredient")],
        [InlineKeyboardButton(text="🎉 Конструктор вечеринок", callback_data="party_builder")],
        [InlineKeyboardButton(text="📋 Моё избранное", callback_data="my_favorites")],
        [InlineKeyboardButton(text="🏪 Городской блог", callback_data="city_blog")],
        [InlineKeyboardButton(text="🎁 Пригласить друга", callback_data="referral_info")],
        [InlineKeyboardButton(text="⭐️ Премиум", callback_data="premium_info")],
        [InlineKeyboardButton(text="💳 Поддержать (ЮMoney)", callback_data="donate_info")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def back_to_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 В главное меню", callback_data="back_to_menu")]
    ])
