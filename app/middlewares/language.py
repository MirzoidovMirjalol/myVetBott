"""
Language middleware for automatic language detection
"""

from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User


class LanguageMiddleware(BaseMiddleware):
    """
    Middleware to set user language in handler data
    """
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """
        Inject user language into handler data
        
        Args:
            handler: Handler function
            event: Telegram event
            data: Handler data
        
        Returns:
            Handler result
        """
        user: User = data.get("event_from_user")
        
        if user:
            # TODO: Get language from database
            # For now, use default or user's telegram language
            language = "ru"  # Default
            
            # You can use user.language_code for initial language
            if hasattr(user, "language_code") and user.language_code:
                lang_code = user.language_code.lower()
                if lang_code in ["ru", "en", "uz"]:
                    language = lang_code
                elif lang_code.startswith("uz"):
                    language = "uz"
                elif lang_code.startswith("en"):
                    language = "en"
            
            data["language"] = language
            data["user_id"] = user.id
        
        return await handler(event, data)
