"""
Other handlers (news, facts, feeding, language, history, etc.)
"""

import random
from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode

from app.locales import get_text, get_feeding_info
from app.keyboards.inline import (
    create_feeding_keyboard,
    create_domestic_animals_keyboard,
    create_language_keyboard
)
from app.utils.helpers import safe_edit_message

router = Router()


# Animal facts
ANIMAL_FACTS = [
    "🐕 Собаки понимают до 250 слов и жестов, считают до пяти и могут решать простейшие математические задачи.",
    "🐱 Кошки спят около 70% своей жизни.",
    "🐰 Кролики могут видеть позади себя, не поворачивая головы.",
    "🐦 Попугаи могут жить более 80 лет.",
    "🐠 Золотые рыбки имеют память около 3 месяцев.",
    "🦜 Некоторые виды попугаев могут имитировать человеческую речь почти идеально.",
    "🐹 Хомяки могут пробежать до 8 км за ночь в своем колесе.",
    "🐢 Черепахи могут жить более 100 лет.",
    "🦎 Некоторые ящерицы могут отбрасывать хвост при опасности.",
    "🐭 Мыши могут смеяться, когда их щекочут."
]


# ==================== NEWS ====================

@router.callback_query(F.data == "menu_news")
async def news_menu(callback: types.CallbackQuery, language: str = "ru"):
    """Show news"""
    user_id = callback.from_user.id
    
    # Sample news
    news_list = [
        "📰 <b>Новость 1:</b> В Ташкенте открылся новый приют для бездомных животных",
        "📰 <b>Новость 2:</b> Бесплатная вакцинация собак от бешенства в Самарканде",
        "📰 <b>Новость 3:</b> Конкурс на лучший зоомагазин Узбекистана 2024",
        "📰 <b>Новость 4:</b> Новый закон о защите животных в Узбекистане"
    ]
    
    text = get_text(user_id, "news_section", language) + "\n\n" + "\n\n".join(news_list)
    
    await safe_edit_message(
        callback.message,
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Обновить новости", callback_data="menu_news")],
            [InlineKeyboardButton(text=get_text(user_id, "back_to_menu", language), callback_data="back_to_menu")]
        ])
    )
    await callback.answer()


# ==================== FACTS ====================

@router.callback_query(F.data == "menu_facts")
async def facts_menu(callback: types.CallbackQuery, language: str = "ru"):
    """Show random fact"""
    user_id = callback.from_user.id
    
    random_fact = random.choice(ANIMAL_FACTS)
    
    text = get_text(user_id, "facts_section", language) + f"\n\n🎲 <b>Случайный факт:</b>\n\n{random_fact}"
    
    await safe_edit_message(
        callback.message,
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎲 Еще факт", callback_data="menu_facts")],
            [InlineKeyboardButton(text=get_text(user_id, "back_to_menu", language), callback_data="back_to_menu")]
        ])
    )
    await callback.answer()


# ==================== FEEDING ====================

@router.callback_query(F.data == "menu_feeding")
async def feeding_menu(callback: types.CallbackQuery, language: str = "ru"):
    """Show feeding menu"""
    user_id = callback.from_user.id
    
    await safe_edit_message(
        callback.message,
        get_text(user_id, "feeding_section", language),
        reply_markup=create_feeding_keyboard(language)
    )
    await callback.answer()


@router.callback_query(F.data == "feeding_domestic")
async def domestic_feeding(callback: types.CallbackQuery, language: str = "ru"):
    """Show domestic animals feeding menu"""
    await safe_edit_message(
        callback.message,
        "🏠 <b>Кормление домашних животных</b>\n\nВыберите тип животного:",
        reply_markup=create_domestic_animals_keyboard(language)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("feed_"))
async def show_feeding_info(callback: types.CallbackQuery, language: str = "ru"):
    """Show feeding information for selected animal"""
    animal_type = callback.data.replace("feed_", "")
    
    info = get_feeding_info(animal_type, language)
    
    await safe_edit_message(
        callback.message,
        info,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="feeding_domestic")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")]
        ])
    )
    await callback.answer()


@router.callback_query(F.data == "feeding_farm")
async def farm_feeding(callback: types.CallbackQuery):
    """Farm animals feeding (placeholder)"""
    await callback.answer(
        "🐄 Раздел в разработке. Скоро будет доступна информация о кормлении фермерских животных.",
        show_alert=True
    )


@router.callback_query(F.data == "feeding_exotic")
async def exotic_feeding(callback: types.CallbackQuery):
    """Exotic animals feeding (placeholder)"""
    await callback.answer(
        "🦎 Раздел в разработке. Скоро будет доступна информация о кормлении экзотических животных.",
        show_alert=True
    )


# ==================== LANGUAGE ====================

@router.callback_query(F.data == "menu_language")
async def language_menu(callback: types.CallbackQuery, language: str = "ru"):
    """Show language selection menu"""
    user_id = callback.from_user.id
    
    await safe_edit_message(
        callback.message,
        get_text(user_id, "choose_language", language),
        reply_markup=create_language_keyboard(language)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: types.CallbackQuery):
    """Set user language"""
    user_id = callback.from_user.id
    language = callback.data.replace("lang_", "")
    
    # TODO: Save to database
    # from app.database import get_db, crud
    # async with get_db() as session:
    #     await crud.update_user_language(session, user_id, language)
    
    languages = {
        "ru": "🇷🇺 Русский",
        "en": "🇺🇸 English",
        "uz": "🇺🇿 O'zbekcha"
    }
    
    await callback.answer(f"Язык изменен на {languages.get(language, language)}!")
    
    # Return to main menu with new language
    from app.handlers.start import back_to_main_menu
    from aiogram.fsm.context import FSMContext
    # Note: We can't easily get FSMContext here, so we'll just go back to menu
    await callback.message.answer(
        get_text(user_id, "main_menu", language),
        reply_markup=__import__('app.keyboards.main_menu', fromlist=['get_main_menu']).get_main_menu(user_id, language)
    )


# ==================== HISTORY ====================

@router.callback_query(F.data == "menu_history")
async def history_menu(callback: types.CallbackQuery, language: str = "ru"):
    """Show user history"""
    user_id = callback.from_user.id
    
    # TODO: Get from database
    text = "📭 <b>История пуста</b>\n\nЗдесь будут отображаться ваши действия в боте."
    
    await safe_edit_message(
        callback.message,
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🗑️ Очистить историю", callback_data="clear_history")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
        ])
    )
    await callback.answer()


@router.callback_query(F.data == "clear_history")
async def clear_history(callback: types.CallbackQuery):
    """Clear user history"""
    # TODO: Clear from database
    
    await callback.answer("✅ История очищена!")
    await history_menu(callback)


# ==================== VET CHAT & APPOINTMENT ====================

@router.callback_query(F.data == "menu_vet_chat")
async def vet_chat_menu(callback: types.CallbackQuery, language: str = "ru"):
    """Show vet chat menu"""
    user_id = callback.from_user.id
    
    text = (
        "💬 <b>Чат с ветеринаром</b>\n\n"
        "К сожалению, в данный момент нет доступных ветеринаров онлайн.\n"
        "Вы можете:\n"
        "• Найти клинику для очного приема\n"
        "• Создать профиль ветеринара, если вы специалист"
    )
    
    await safe_edit_message(
        callback.message,
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📍 Клиники", callback_data="menu_clinics")],
            [InlineKeyboardButton(text="👨‍⚕️ Стать ветер.", callback_data="create_vet_profile")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
        ])
    )
    await callback.answer()


@router.callback_query(F.data == "menu_appointment")
async def appointment_menu(callback: types.CallbackQuery, language: str = "ru"):
    """Show appointment menu"""
    user_id = callback.from_user.id
    
    text = get_text(user_id, "appointment_section", language)
    
    await safe_edit_message(
        callback.message,
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📅 Записаться онлайн", callback_data="book_appointment")],
            [InlineKeyboardButton(text="📍 Найти клинику", callback_data="menu_clinics")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
        ])
    )
    await callback.answer()


@router.callback_query(F.data == "book_appointment")
async def book_appointment(callback: types.CallbackQuery):
    """Book appointment (placeholder)"""
    await callback.answer(
        "📅 Функция онлайн-записи в разработке. Пожалуйста, свяжитесь с клиникой напрямую.",
        show_alert=True
    )
