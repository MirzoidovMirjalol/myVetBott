"""
Start command and main menu handlers
"""

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.locales import get_text
from app.keyboards.main_menu import get_main_menu
from app.utils.helpers import safe_edit_message

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message, language: str = "ru"):
    """
    Handle /start command
    
    Args:
        message: Incoming message
        language: User's language from middleware
    """
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    # TODO: Initialize user in database if not exists
    # from app.database import get_db, crud
    # async with get_db() as session:
    #     user = await crud.get_user(session, user_id)
    #     if not user:
    #         await crud.create_user(
    #             session, user_id, message.from_user.username,
    #             user_name, message.from_user.last_name, language
    #         )
    
    welcome_text = get_text(user_id, "welcome", language, name=user_name)
    
    await message.answer(
        text=welcome_text,
        reply_markup=get_main_menu(user_id, language)
    )


@router.callback_query(F.data == "back_to_menu")
async def back_to_main_menu(callback: types.CallbackQuery, state: FSMContext, language: str = "ru"):
    """
    Handle back to main menu button
    
    Args:
        callback: Callback query
        state: FSM context
        language: User's language
    """
    # Clear any active state
    await state.clear()
    
    user_id = callback.from_user.id
    
    await safe_edit_message(
        callback.message,
        get_text(user_id, "main_menu", language),
        reply_markup=get_main_menu(user_id, language)
    )
    await callback.answer()


@router.message(Command("help"))
async def cmd_help(message: types.Message, language: str = "ru"):
    """
    Handle /help command
    
    Args:
        message: Incoming message
        language: User's language
    """
    help_text = (
        "🐾 <b>PetHelper Bot - Помощник по уходу за питомцами</b>\n\n"
        "Доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать это сообщение\n"
        "/menu - Открыть главное меню\n\n"
        "<b>Основные функции:</b>\n"
        "• 👤 Профиль питомца и владельца\n"
        "• 📍 Поиск клиник и аптек\n"
        "• ⏰ Напоминания о процедурах\n"
        "• 🩺 Проверка симптомов\n"
        "• 📢 Объявления\n"
        "• 💬 Чат с ветеринарами\n"
        "• 🍖 Советы по кормлению\n"
        "• И многое другое!\n\n"
        "Выберите функцию в главном меню 👇"
    )
    
    await message.answer(
        text=help_text,
        reply_markup=get_main_menu(message.from_user.id, language)
    )


@router.message(Command("menu"))
async def cmd_menu(message: types.Message, language: str = "ru"):
    """
    Handle /menu command
    
    Args:
        message: Incoming message
        language: User's language
    """
    await message.answer(
        text=get_text(message.from_user.id, "main_menu", language),
        reply_markup=get_main_menu(message.from_user.id, language)
    )
