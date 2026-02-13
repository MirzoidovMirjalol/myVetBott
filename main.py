"""
PetHelper Bot - Main entry point
"""

import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.config import settings
from app.database import init_db, close_db
from app.middlewares import LanguageMiddleware
from app.handlers import start, profile, clinic, reminder, ads, symptoms, other


# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/bot.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)


async def on_startup():
    """Actions on bot startup"""
    logger.info("=" * 50)
    logger.info("🐾 VETERINARY BOT PETHELPER STARTING...")
    logger.info(f"✅ Version: 2.0.0 (Professional Edition)")
    logger.info(f"✅ Python: {sys.version}")
    logger.info("✅ Features:")
    logger.info("   • Multilingual interface (RU/EN/UZ)")
    logger.info("   • PostgreSQL database")
    logger.info("   • Redis caching")
    logger.info("   • Modular architecture")
    logger.info("   • Owner and vet profiles")
    logger.info("   • Clinic/pharmacy/shelter search")
    logger.info("   • Reminder system")
    logger.info("   • Advertisements and news")
    logger.info("   • Animal facts")
    logger.info("   • Feeding recommendations")
    logger.info("   • Symptom checker")
    logger.info("   • Action history")
    logger.info("=" * 50)
    
    # Initialize database
    try:
        logger.info("Initializing database...")
        await init_db()
        logger.info("✅ Database initialized successfully!")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise


async def on_shutdown():
    """Actions on bot shutdown"""
    logger.info("Shutting down bot...")
    
    # Close database connections
    try:
        await close_db()
        logger.info("✅ Database connections closed")
    except Exception as e:
        logger.error(f"Error closing database: {e}")
    
    logger.info("👋 Bot stopped successfully")


async def main():
    """Main bot function"""
    
    # Create bot instance
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )
    
    # Create dispatcher
    dp = Dispatcher()
    
    # Register middleware
    dp.message.middleware(LanguageMiddleware())
    dp.callback_query.middleware(LanguageMiddleware())
    
    # Register routers
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(clinic.router)
    dp.include_router(reminder.router)
    dp.include_router(ads.router)
    dp.include_router(symptoms.router)
    dp.include_router(other.router)
    
    # Register startup/shutdown handlers
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Delete webhook and start polling
    try:
        logger.info("Deleting webhook...")
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("✅ Webhook deleted!")
        
        logger.info("Starting bot polling...")
        logger.info("✅ Bot is ready to accept messages!")
        logger.info("👉 Send /start to your bot in Telegram")
        
        await dp.start_polling(
            bot,
            allowed_updates=settings.ALLOWED_UPDATES,
            skip_updates=True
        )
    except Exception as e:
        logger.error(f"❌ Bot startup error: {e}")
        raise
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (Ctrl+C)")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
