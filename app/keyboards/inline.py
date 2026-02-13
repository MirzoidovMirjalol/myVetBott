"""
Inline keyboards for various bot features
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.locales import get_text


# Uzbekistan cities for location selection
UZBEK_CITIES = [
    "tashkent", "samarkand", "bukhara", "khiva", "andijan",
    "namangan", "fergana", "nukus", "urgench", "karshi",
    "jizzakh", "navoi", "termez"
]


def get_profile_menu(user_id: int, language: str = "ru") -> InlineKeyboardMarkup:
    """Profile menu keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=get_text(user_id, "create_profile", language),
            callback_data="create_profile"
        )],
        [InlineKeyboardButton(
            text=get_text(user_id, "create_vet_profile", language),
            callback_data="create_vet_profile"
        )],
        [InlineKeyboardButton(
            text=get_text(user_id, "view_profile", language),
            callback_data="profile_view"
        )],
        [InlineKeyboardButton(
            text=get_text(user_id, "view_vet_profile", language),
            callback_data="vet_profile_view"
        )],
        [InlineKeyboardButton(
            text=get_text(user_id, "edit_profile", language),
            callback_data="edit_profile"
        )],
        [InlineKeyboardButton(
            text=get_text(user_id, "clear_profile", language),
            callback_data="profile_clear"
        )],
        [InlineKeyboardButton(
            text=get_text(user_id, "back_to_menu", language),
            callback_data="back_to_menu"
        )]
    ])


def get_ads_menu(user_id: int, language: str = "ru") -> InlineKeyboardMarkup:
    """Advertisements menu keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=get_text(user_id, "post_ad", language),
            callback_data="post_ad"
        )],
        [InlineKeyboardButton(
            text=get_text(user_id, "view_ads", language),
            callback_data="view_ads"
        )],
        [InlineKeyboardButton(
            text=get_text(user_id, "my_ads", language),
            callback_data="my_ads"
        )],
        [InlineKeyboardButton(
            text=get_text(user_id, "back_to_menu", language),
            callback_data="back_to_menu"
        )]
    ])


def get_reminders_menu(user_id: int, language: str = "ru") -> InlineKeyboardMarkup:
    """Reminders menu keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=get_text(user_id, "add_reminder", language),
            callback_data="reminder_add"
        )],
        [InlineKeyboardButton(
            text=get_text(user_id, "my_reminders", language),
            callback_data="reminder_list"
        )],
        [InlineKeyboardButton(
            text=get_text(user_id, "back_to_menu", language),
            callback_data="back_to_menu"
        )]
    ])


def create_reminder_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    """Reminder type selection keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏰ Один раз", callback_data="reminder_one_time")],
        [InlineKeyboardButton(text="🔄 Ежедневно", callback_data="reminder_daily")],
        [InlineKeyboardButton(text="📆 Еженедельно", callback_data="reminder_weekly")],
        [InlineKeyboardButton(text="⚙️ Настроить дни", callback_data="reminder_custom")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="menu_reminders")]
    ])


def create_cities_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    """Cities selection keyboard for Uzbekistan"""
    buttons = []
    row = []
    
    for city_key in UZBEK_CITIES:
        city_name = get_text(0, city_key, language)
        row.append(InlineKeyboardButton(
            text=city_name,
            callback_data=f"city_{city_key}"
        ))
        
        if len(row) == 2:
            buttons.append(row)
            row = []
    
    if row:
        buttons.append(row)
    
    buttons.append([InlineKeyboardButton(
        text="📍 Найти по геолокации",
        callback_data="find_by_location"
    )])
    buttons.append([InlineKeyboardButton(
        text="🔙 Назад",
        callback_data="back_to_menu"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_animal_type_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    """Animal type selection keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐕 Собака", callback_data="animal_dog")],
        [InlineKeyboardButton(text="🐱 Кошка", callback_data="animal_cat")],
        [InlineKeyboardButton(text="🐹 Грызуны", callback_data="animal_rodent")],
        [InlineKeyboardButton(text="🐦 Птицы", callback_data="animal_bird")],
        [InlineKeyboardButton(text="🐠 Рыбки", callback_data="animal_fish")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="menu_symptoms")]
    ])


def create_feeding_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    """Feeding category selection keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Домашние животные", callback_data="feeding_domestic")],
        [InlineKeyboardButton(text="🐄 Сельскохозяйственные", callback_data="feeding_farm")],
        [InlineKeyboardButton(text="🦎 Экзотические", callback_data="feeding_exotic")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
    ])


def create_domestic_animals_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    """Domestic animals selection keyboard for feeding"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐕 Собаки", callback_data="feed_dog")],
        [InlineKeyboardButton(text="🐱 Кошки", callback_data="feed_cat")],
        [InlineKeyboardButton(text="🐹 Грызуны", callback_data="feed_rodent")],
        [InlineKeyboardButton(text="🐦 Птицы", callback_data="feed_bird")],
        [InlineKeyboardButton(text="🐠 Рыбки", callback_data="feed_fish")],
        [InlineKeyboardButton(text="🐢 Рептилии", callback_data="feed_reptile")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="menu_feeding")]
    ])


def create_language_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    """Language selection keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en")],
        [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
    ])


def create_cancel_button(callback_data: str = "back_to_menu") -> InlineKeyboardMarkup:
    """Create a cancel button"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data=callback_data)]
    ])
