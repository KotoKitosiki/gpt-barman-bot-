from aiogram import Router, types
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database.core import AsyncSessionLocal
from database.models import Favorite, Partner
from sqlalchemy import select
from config import settings

router = Router()

@router.callback_query(lambda c: c.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    from keyboards.inline import main_menu_keyboard
    await callback.message.edit_text(
        "🍸 *Главное меню*\nВыбирай, что душе угодно!",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "order_recipe")
async def order_recipe(callback: CallbackQuery):
    await callback.message.edit_text(
        "🍹 *Заказ коктейля*\n\nНапиши мне своё настроение или пожелание, и я сочиню рецепт!\nНапример: *«Хочу чего-то летнего, с ананасом»* или *«Бодрящий, чтобы проснуться»*.\n\nПросто ответь на это сообщение текстом 👇",
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "from_my_bar")
async def from_my_bar(callback: CallbackQuery):
    await callback.message.edit_text(
        "🥃 *Что у тебя есть?*\n\nНапиши, какие напитки и ингредиенты нашлись дома.\nЯ подберу коктейль, который можно смешать прямо сейчас!\n\nПример: *«Виски, лимон, сахарный сироп, лёд»*",
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "secret_ingredient")
async def secret_ingredient(callback: CallbackQuery):
    await callback.message.edit_text(
        "✨ *Секретный ингредиент*\n\nНазови любой необычный продукт (авокадо, свёкла, халапеньо...),\nи я придумаю коктейль, который ты точно не пробовал!\n\nНапиши свой ингредиент 👇",
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "party_builder")
async def party_builder(callback: CallbackQuery):
    await callback.message.edit_text(
        "🎉 *Конструктор вечеринок*\n\nРасскажи, что за вечеринка планируется:\n- Тема (например, Техас, день рождения)\n- Сколько гостей\n- Есть ли те, кто не пьёт алкоголь\n- Бюджет на напитки\n\nЯ подготовлю меню коктейлей, список закусок и даже плейлист!\nПиши в одном сообщении 👇",
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "my_favorites")
async def my_favorites(callback: CallbackQuery):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Favorite).where(Favorite.user_telegram_id == callback.from_user.id)
        )
        favorites = result.scalars().all()
        if not favorites:
            await callback.message.edit_text(
                "📋 *Избранное пусто*\n\nСохраняй понравившиеся рецепты — просто напиши «сохрани» в ответ на рецепт, и я добавлю его сюда!\n\nА пока — закажем что-нибудь новенькое? 😉",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🔙 В меню", callback_data="back_to_menu")]
                ])
            )
        else:
            fav_list = "\n\n".join([f"🍸 {f.recipe_text[:200]}..." for f in favorites[:5]])
            await callback.message.edit_text(
                f"📋 *Твоё избранное (последние 5):*\n\n{fav_list}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🔙 В меню", callback_data="back_to_menu")]
                ])
            )
    await callback.answer()

@router.callback_query(lambda c: c.data == "city_blog")
async def city_blog(callback: CallbackQuery):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Partner).where(Partner.active == True))
        partners = result.scalars().all()
        if not partners:
            text = "🏪 *Городской блог*\n\nПока партнёров нет, но скоро здесь появятся лучшие магазины города!\nХочешь разместиться? Пиши: @kitanish"
        else:
            text = "🏪 *Городские скидки и магазины*\n\n"
            for p in partners[:5]:
                text += f"**{p.name}**\n{p.description}\n👉 [Перейти]({p.referral_url})\nПромокод: `{p.promo_code or 'нет'}`\n\n"
    await callback.message.edit_text(
        text,
        parse_mode="Markdown",
        disable_web_page_preview=False,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 В меню", callback_data="back_to_menu")]
        ])
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "referral_info")
async def referral_info(callback: CallbackQuery):
    from database.models import User
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == callback.from_user.id))
        user = result.scalar_one_or_none()
        ref_link = user.referral_link if user else "Сначала напиши /start"
        await callback.message.edit_text(
            "🎁 *Приведи друга — получи бонус!*\n\n"
            f"Твоя ссылка: `{ref_link}`\n\n"
            f"Друзей приведено: *{user.referral_count if user else 0}*\n"
            "За каждого друга — +2 дня премиума 🌟\n\n"
            "Отправь ссылку друзьям, и когда они запустят бота, ты получишь
