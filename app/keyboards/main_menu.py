"""
Main menu keyboards
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.locales import get_text


def get_main_menu(user_id: int, language: str = "ru") -> InlineKeyboardMarkup:
    """
    Create main menu keyboard with all bot options
    
    Args:
        user_id: User ID
        language: Language code (ru/en/uz)
    
    Returns:
        InlineKeyboardMarkup with main menu buttons
    """
    # Large profile button (full width)
    menu_buttons = [
        [InlineKeyboardButton(
            text=get_text(user_id, "profile_big", language),
            callback_data="menu_profile"
        )],
        [
            InlineKeyboardButton(
                text=get_text(user_id, "ads", language),
                callback_data="menu_ads"
            ),
            InlineKeyboardButton(
                text=get_text(user_id, "news", language),
                callback_data="menu_news"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text(user_id, "pet_shop", language),
                callback_data="menu_pet_shop"
            ),
            InlineKeyboardButton(
                text=get_text(user_id, "pet_facts", language),
                callback_data="menu_facts"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text(user_id, "feeding_guide", language),
                callback_data="menu_feeding"
            ),
            InlineKeyboardButton(
                text=get_text(user_id, "symptoms", language),
                callback_data="menu_symptoms"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text(user_id, "clinics", language),
                callback_data="menu_clinics"
            ),
            InlineKeyboardButton(
                text=get_text(user_id, "pharmacies", language),
                callback_data="menu_pharmacies"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text(user_id, "reminders", language),
                callback_data="menu_reminders"
            ),
            InlineKeyboardButton(
                text=get_text(user_id, "shelters", language),
                callback_data="menu_shelters"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text(user_id, "vet_chat", language),
                callback_data="menu_vet_chat"
            ),
            InlineKeyboardButton(
                text=get_text(user_id, "appointment", language),
                callback_data="menu_appointment"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text(user_id, "history", language),
                callback_data="menu_history"
            ),
            InlineKeyboardButton(
                text=get_text(user_id, "language", language),
                callback_data="menu_language"
            )
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=menu_buttons)


def get_back_to_menu_button(user_id: int, language: str = "ru") -> InlineKeyboardMarkup:
    """
    Create a simple back to menu button
    
    Args:
        user_id: User ID
        language: Language code (ru/en/uz)
    
    Returns:
        InlineKeyboardMarkup with back button
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=get_text(user_id, "back_to_menu", language),
            callback_data="back_to_menu"
        )]
    ])
