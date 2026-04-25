from aiogram import Router, types
from aiogram.filters import CommandStart
from sqlalchemy import select
from datetime import datetime
from database.core import AsyncSessionLocal
from database.models import User
from keyboards.inline import main_menu_keyboard
from config import settings

router = Router()

# Приветственные фразы с юмором
WELCOME_MESSAGES = [
    "🍸 Приветствую в баре «У Китёныша»! Я твой личный миксолог. Готов смешать настроение, даже если ты трезв как стёклышко.",
    "🎩 Добро пожаловать! Я — бармен-виртуоз. У меня есть рецепты на все случаи жизни, включая «завтра на работу после трёх коктейлей».",
    "🍹 О, свежая кровь! То есть, свежий гость! Присаживайся, сейчас колдовать будем.",
]

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()

        if not user:
            # Новый гость
            referrer_id = None
            # Проверяем, пришёл ли по реферальной ссылке
            if message.text and len(message.text.split()) > 1:
                ref_param = message.text.split()[1]
                if ref_param.startswith("ref") and ref_param[3:].isdigit():
                    referrer_id = int(ref_param[3:])

            new_user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                daily_requests_count=0,
                last_request_date=datetime.utcnow(),
                referrer_id=referrer_id,
                referral_link=f"https://t.me/{(await message.bot.get_me()).username}?start=ref{message.from_user.id}"
            )
            session.add(new_user)
            await session.commit()

            welcome_text = (
                f"{WELCOME_MESSAGES[0]}\n\n"
                f"🎁 *Бесплатно:* {settings.FREE_DAILY_LIMIT} рецепта в день.\n"
                "⭐️ *Премиум:* Безлимит, секретные миксы, конструктор вечеринок.\n\n"
                "Жми кнопку «🍹 Заказать коктейль» и поехали!"
            )
        else:
            # Старый друг
            user.daily_requests_count = 0  # Сбрасываем счётчик при новом заходе (для теста)
            await session.commit()
            welcome_text = (
                f"С возвращением, {user.first_name or 'друг'}!\n"
                f"Как настроение? Давай смешаем что-нибудь грандиозное!"
            )

    await message.answer(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )
