"""
Clinic, pharmacy, and shelter handlers
"""

from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.locales import get_text
from app.keyboards.inline import create_cities_keyboard
from app.utils.helpers import safe_edit_message

router = Router()


# Sample data (in production, this should come from database)
CLINICS_DATA = {
    "tashkent": [
        "🏥 <b>Vet Clinic 'Pet Care'</b>\n📍 Mirzo Ulug'bek tumani\n📞 +998 71 123 45 67\n🕒 24/7",
        "🏥 <b>Animal Hospital Tashkent</b>\n📍 Yunusobod tumani\n📞 +998 71 234 56 78\n🕒 08:00-22:00",
        "🏥 <b>Doctor Vet Center</b>\n📍 Shayxontohur tumani\n📞 +998 71 345 67 89\n🕒 09:00-20:00"
    ],
    "samarkand": [
        "🏥 <b>Samarkand Vet Clinic</b>\n📍 Registon ko'chasi\n📞 +998 66 123 45 67\n🕒 09:00-19:00",
        "🏥 <b>Animal Care Samarqand</b>\n📍 Amir Temur ko'chasi\n📞 +998 66 234 56 78\n🕒 08:00-21:00"
    ]
}

PHARMACIES_DATA = {
    "tashkent": [
        "💊 <b>Vet Pharmacy #1</b>\n📍 Chilonzor tumani\n📞 +998 71 111 22 33\n🕒 08:00-23:00",
        "💊 <b>Animal Drugs Center</b>\n📍 Yakkasaroy tumani\n📞 +998 71 222 33 44\n🕒 24/7",
        "💊 <b>Pet Med Tashkent</b>\n📍 Mirabad tumani\n📞 +998 71 333 44 55\n🕒 09:00-22:00"
    ]
}

SHELTERS_DATA = {
    "tashkent": [
        "🏠 <b>Tashkent Animal Shelter</b>\n📍 Qibray tumani\n📞 +998 71 444 55 66\n🐕 50+ animals",
        "🏠 <b>Hope for Pets Shelter</b>\n📍 Olmazor tumani\n📞 +998 71 555 66 77\n🐱 30+ animals"
    ]
}


@router.callback_query(F.data == "menu_clinics")
async def clinics_menu(callback: types.CallbackQuery, language: str = "ru"):
    """Show clinics menu"""
    user_id = callback.from_user.id
    
    await safe_edit_message(
        callback.message,
        get_text(user_id, "clinics_section", language),
        reply_markup=create_cities_keyboard(language)
    )
    await callback.answer()


@router.callback_query(F.data == "menu_pharmacies")
async def pharmacies_menu(callback: types.CallbackQuery, language: str = "ru"):
    """Show pharmacies menu"""
    user_id = callback.from_user.id
    
    await safe_edit_message(
        callback.message,
        get_text(user_id, "pharmacies_section", language),
        reply_markup=create_cities_keyboard(language)
    )
    await callback.answer()


@router.callback_query(F.data == "menu_shelters")
async def shelters_menu(callback: types.CallbackQuery, language: str = "ru"):
    """Show shelters menu"""
    user_id = callback.from_user.id
    
    await safe_edit_message(
        callback.message,
        get_text(user_id, "shelters_section", language),
        reply_markup=create_cities_keyboard(language)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("city_"))
async def show_city_info(callback: types.CallbackQuery, language: str = "ru"):
    """Show information for selected city"""
    user_id = callback.from_user.id
    city_key = callback.data.replace("city_", "")
    city_name = get_text(user_id, city_key, language)
    
    # Determine type based on original message
    message_text = callback.message.text.lower()
    
    if "клиник" in message_text or "clinic" in message_text or "klinika" in message_text:
        # TODO: Get from database
        data = CLINICS_DATA.get(city_key, [f"🏥 В городе {city_name} информация о клиниках обновляется"])
        title = f"🏥 <b>Ветеринарные клиники в {city_name}:</b>\n\n"
    elif "аптек" in message_text or "pharmacy" in message_text or "dorixona" in message_text:
        data = PHARMACIES_DATA.get(city_key, [f"💊 В городе {city_name} информация об аптеках обновляется"])
        title = f"💊 <b>Ветеринарные аптеки в {city_name}:</b>\n\n"
    else:
        data = SHELTERS_DATA.get(city_key, [f"🏠 В городе {city_name} информация о приютах обновляется"])
        title = f"🏠 <b>Приюты для животных в {city_name}:</b>\n\n"
    
    text = title + "\n\n".join(data)
    
    await safe_edit_message(
        callback.message,
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="📍 Показать на карте",
                callback_data=f"show_on_map_{city_key}"
            )],
            [InlineKeyboardButton(
                text="🔙 Назад",
                callback_data="back_to_menu"
            )]
        ])
    )
    await callback.answer()


@router.callback_query(F.data.startswith("show_on_map_"))
async def show_on_map(callback: types.CallbackQuery, language: str = "ru"):
    """Show location on map"""
    user_id = callback.from_user.id
    city_key = callback.data.replace("show_on_map_", "")
    city_name = get_text(user_id, city_key, language)
    
    # Create Google Maps search link
    maps_url = f"https://www.google.com/maps/search/ветеринарные+клиники+{city_name}"
    
    await callback.message.answer(
        f"📍 <b>{city_name} на карте</b>\n\n"
        f"Нажмите на ссылку ниже, чтобы открыть карту:\n"
        f"{maps_url}"
    )
    await callback.answer()


@router.callback_query(F.data == "menu_pet_shop")
async def pet_shop_menu(callback: types.CallbackQuery, language: str = "ru"):
    """Show pet shops menu"""
    user_id = callback.from_user.id
    
    await safe_edit_message(
        callback.message,
        get_text(user_id, "pet_shop_section", language),
        reply_markup=create_cities_keyboard(language)
    )
    await callback.answer()


@router.callback_query(F.data == "find_by_location")
async def find_by_location(callback: types.CallbackQuery):
    """Request user location"""
    await callback.answer(
        "📍 Функция геолокации в разработке. Пожалуйста, выберите город из списка.",
        show_alert=True
    )
