from aiogram import Router, types
from database.core import AsyncSessionLocal
from database.models import User, Favorite, RecipeLog
from sqlalchemy import select
from datetime import datetime, date
from config import settings
from services.ai_service import get_cocktail_recipe
from keyboards.inline import main_menu_keyboard, back_to_menu_keyboard

router = Router()
user_modes = {}
user_last_recipe = {}

@router.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    if not text:
        await message.answer("🍸 Я понимаю только текст. Напиши, что хочешь заказать!")
        return

    if text.lower() == "сохрани":
        await save_last_recipe(user_id, message)
        return

    mode = user_modes.get(user_id, "basic")
    can_proceed, limit_message = await check_limits(user_id)
    if not can_proceed:
        await message.answer(limit_message, reply_markup=main_menu_keyboard())
        return

    thinking_msg = await message.answer("🍹 *Бармен смешивает...* думаю над твоим заказом...", parse_mode="Markdown")

    if mode == "party":
        recipe = await get_cocktail_recipe(text, mode="party")
    elif mode == "from_bar":
        recipe = await get_cocktail_recipe(text, mode="from_bar")
    elif mode == "secret":
        recipe = await get_cocktail_recipe(text, mode="secret")
    else:
        recipe = await get_cocktail_recipe(text, mode="basic")

    await thinking_msg.edit_text(recipe, parse_mode="Markdown", reply_markup=back_to_menu_keyboard())
    await log_recipe(user_id, text, recipe, mode)
    user_last_recipe[user_id] = recipe
    user_modes[user_id] = "basic"

async def save_last_recipe(user_id: int, message: types.Message):
    last_recipe = user_last_recipe.get(user_id)
    if not last_recipe:
        await message.answer("🤔 Пока нечего сохранять. Сначала закажи коктейль!")
        return
    async with AsyncSessionLocal() as session:
        new_fav = Favorite(user_telegram_id=user_id, recipe_text=last_recipe[:500])
        session.add(new_fav)
        await session.commit()
    await message.answer("⭐️ Рецепт сохранён в избранное! Найти его можно в меню «📋 Моё избранное».")

async def check_limits(user_id: int) -> tuple:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            return True, ""
        if user.is_premium:
            if user.premium_expire and user.premium_expire < datetime.utcnow():
                user.is_premium = False
                await session.commit()
            else:
                return True, ""
        today = date.today()
        if user.last_request_date.date() != today:
            user.daily_requests_count = 0
            user.last_request_date = datetime.utcnow()
            await session.commit()
            return True, ""
        if user.daily_requests_count >= settings.FREE_DAILY_LIMIT:
            return False, (
                f"😔 На сегодня бесплатные рецепты закончились (лимит: {settings.FREE_DAILY_LIMIT}).\n"
                "Приходи завтра или активируй премиум — там безлимит и ещё куча плюшек! 🌟\n"
                "Или пригласи друга по реферальной ссылке и получи +2 дня премиума! 🎁"
            )
        user.daily_requests_count += 1
        await session.commit()
        return True, ""

async def log_recipe(user_id: int, ingredients: str, response: str, mode: str):
    async with AsyncSessionLocal() as session:
        log = RecipeLog(user_telegram_id=user_id, ingredients_input=ingredients, ai_response=response[:500], mode=mode)
        session.add(log)
        await session.commit()
