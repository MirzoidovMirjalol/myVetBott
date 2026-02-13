"""
Helper utility functions
"""

from typing import Optional
from datetime import datetime
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup


async def safe_edit_message(
    message: Message,
    text: str,
    reply_markup: Optional[InlineKeyboardMarkup] = None,
    parse_mode: ParseMode = ParseMode.HTML
) -> bool:
    """
    Safely edit message text, falls back to sending new message if edit fails
    
    Args:
        message: Message to edit
        text: New text
        reply_markup: Optional keyboard markup
        parse_mode: Parse mode for text
    
    Returns:
        True if edited successfully, False if sent new message
    """
    try:
        await message.edit_text(
            text=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup
        )
        return True
    except Exception:
        try:
            await message.answer(
                text=text,
                parse_mode=parse_mode,
                reply_markup=reply_markup
            )
            return False
        except Exception:
            return False


def format_timestamp(dt: datetime, format_str: str = "%d.%m.%Y %H:%M") -> str:
    """
    Format datetime to string
    
    Args:
        dt: Datetime object
        format_str: Format string
    
    Returns:
        Formatted datetime string
    """
    return dt.strftime(format_str)


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
