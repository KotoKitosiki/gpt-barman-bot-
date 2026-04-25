import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import os
from config import settings
from database.core import init_db

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Переменные окружения для вебхука
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL", "")

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустить бармена 🍸"),
        BotCommand(command="menu", description="Главное меню 📋"),
        BotCommand(command="premium", description="Премиум подписка ⭐️"),
        BotCommand(command="donate", description="Поддержать бармена 💰"),
        BotCommand(command="referral", description="Реферальная программа 🎁"),
    ]
    await bot.set_my_commands(commands)

async def on_startup(bot: Bot):
    await init_db()
    logger.info("Database initialized")
    await set_commands(bot)
    # Устанавливаем вебхук
    if RENDER_EXTERNAL_URL:
        webhook_url = f"{RENDER_EXTERNAL_URL}/webhook"
        await bot.set_webhook(webhook_url)
        logger.info(f"Webhook set to {webhook_url}")
    logger.info("Bot started")

async def on_shutdown(bot: Bot):
    await bot.delete_webhook()
    logger.info("Bot stopped")

async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    # Импорт и регистрация роутеров (добавим ниже по мере готовности)
    from handlers.start import router as start_router
    dp.include_router(start_router)

    from handlers.menu import router as menu_router
    dp.include_router(menu_router)

    # Запуск через вебхук на Render или polling локально
    if RENDER_EXTERNAL_URL:
        app = web.Application()
        webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
        webhook_requests_handler.register(app, path="/webhook")
        setup_application(app, dp, bot=bot)
        await app.run_app(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
    else:
        logger.info("No RENDER_EXTERNAL_URL, using polling")
        await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
