"""Keyboards module"""

from .main_menu import get_main_menu, get_back_to_menu_button
from .inline import (
    get_profile_menu,
    get_ads_menu,
    get_reminders_menu,
    create_cities_keyboard,
    create_animal_type_keyboard,
    create_feeding_keyboard,
    create_language_keyboard,
)

__all__ = [
    "get_main_menu",
    "get_back_to_menu_button",
    "get_profile_menu",
    "get_ads_menu",
    "get_reminders_menu",
    "create_cities_keyboard",
    "create_animal_type_keyboard",
    "create_feeding_keyboard",
    "create_language_keyboard",
]
