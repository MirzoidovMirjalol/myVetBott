"""
Locale loader and text retrieval functions
"""

from typing import Dict, Optional
from . import ru, en, uz


# Available locales
LOCALES: Dict[str, Dict] = {
    "ru": ru.TEXTS,
    "en": en.TEXTS,
    "uz": uz.TEXTS,
}

# Feeding info per locale
FEEDING_LOCALES: Dict[str, Dict] = {
    "ru": ru.FEEDING_INFO,
    "en": en.FEEDING_INFO,
    "uz": uz.FEEDING_INFO,
}

# Default language
DEFAULT_LANGUAGE = "ru"


def get_text(user_id: int, text_key: str, language: Optional[str] = None, **kwargs) -> str:
    """
    Get text for the given key in the user's language
    
    Args:
        user_id: User ID (for future database lookup)
        text_key: Key for the text
        language: Language code (ru/en/uz), if None uses default
        **kwargs: Format arguments for the text
    
    Returns:
        Formatted text string
    """
    if language is None:
        language = DEFAULT_LANGUAGE
    
    # Get text from locale
    text_dict = LOCALES.get(language, LOCALES[DEFAULT_LANGUAGE])
    text = text_dict.get(text_key, text_key)
    
    # Format if kwargs provided
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass  # Return unformatted if key missing
    
    return text


def get_feeding_info(animal_type: str, language: str = "ru") -> str:
    """
    Get feeding information for the given animal type
    
    Args:
        animal_type: Type of animal (dog, cat, bird, etc.)
        language: Language code (ru/en/uz)
    
    Returns:
        Feeding information text
    """
    feeding_dict = FEEDING_LOCALES.get(language, FEEDING_LOCALES[DEFAULT_LANGUAGE])
    return feeding_dict.get(animal_type, "Информация обновляется...")


def get_user_language(user_id: int) -> str:
    """
    Get user's preferred language from database
    
    Args:
        user_id: User ID
    
    Returns:
        Language code (ru/en/uz)
    
    Note:
        Currently returns default. Will be implemented with database integration.
    """
    # TODO: Implement database lookup
    # from app.database import crud
    # user = await crud.get_user(user_id)
    # return user.language if user else DEFAULT_LANGUAGE
    return DEFAULT_LANGUAGE


def set_user_language(user_id: int, language: str) -> None:
    """
    Set user's preferred language in database
    
    Args:
        user_id: User ID
        language: Language code (ru/en/uz)
    
    Note:
        Currently does nothing. Will be implemented with database integration.
    """
    # TODO: Implement database update
    # from app.database import crud
    # await crud.update_user_language(user_id, language)
    pass
