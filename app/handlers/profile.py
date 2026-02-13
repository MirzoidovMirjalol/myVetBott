"""
Profile handlers for pet owners and veterinarians
"""

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.locales import get_text
from app.keyboards.inline import get_profile_menu
from app.utils.helpers import safe_edit_message

router = Router()


# FSM States for profile creation
class ProfileStates(StatesGroup):
    waiting_for_owner_name = State()
    waiting_for_owner_phone = State()
    waiting_for_city = State()
    waiting_for_pet_name = State()
    waiting_for_pet_type = State()


class VetProfileStates(StatesGroup):
    waiting_for_vet_name = State()
    waiting_for_vet_phone = State()
    waiting_for_vet_city = State()
    waiting_for_vet_specialization = State()
    waiting_for_vet_experience = State()
    waiting_for_vet_education = State()
    waiting_for_vet_telegram = State()
    waiting_for_vet_consultation_price = State()
    waiting_for_vet_info = State()


@router.callback_query(F.data == "menu_profile")
async def profile_menu(callback: types.CallbackQuery, language: str = "ru"):
    """Show profile menu"""
    user_id = callback.from_user.id
    
    await safe_edit_message(
        callback.message,
        get_text(user_id, "profile_section", language),
        reply_markup=get_profile_menu(user_id, language)
    )
    await callback.answer()


# ==================== OWNER PROFILE ====================

@router.callback_query(F.data == "create_profile")
async def start_create_profile(callback: types.CallbackQuery, state: FSMContext, language: str = "ru"):
    """Start creating owner profile"""
    user_id = callback.from_user.id
    await state.set_state(ProfileStates.waiting_for_owner_name)
    
    await safe_edit_message(
        callback.message,
        "👤 <b>Создание профиля владельца</b>\n\n" + get_text(user_id, "enter_owner_name", language),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )
    await callback.answer()


@router.message(ProfileStates.waiting_for_owner_name)
async def process_owner_name(message: types.Message, state: FSMContext, language: str = "ru"):
    """Process owner name"""
    user_id = message.from_user.id
    await state.update_data(owner_name=message.text)
    await state.set_state(ProfileStates.waiting_for_owner_phone)
    
    await message.answer(
        get_text(user_id, "enter_owner_phone", language),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )


@router.message(ProfileStates.waiting_for_owner_phone)
async def process_owner_phone(message: types.Message, state: FSMContext, language: str = "ru"):
    """Process owner phone"""
    user_id = message.from_user.id
    await state.update_data(owner_phone=message.text)
    await state.set_state(ProfileStates.waiting_for_city)
    
    await message.answer(
        get_text(user_id, "enter_city", language),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )


@router.message(ProfileStates.waiting_for_city)
async def process_city(message: types.Message, state: FSMContext, language: str = "ru"):
    """Process city"""
    user_id = message.from_user.id
    await state.update_data(city=message.text)
    await state.set_state(ProfileStates.waiting_for_pet_name)
    
    await message.answer(
        get_text(user_id, "enter_pet_name", language),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )


@router.message(ProfileStates.waiting_for_pet_name)
async def process_pet_name(message: types.Message, state: FSMContext, language: str = "ru"):
    """Process pet name"""
    user_id = message.from_user.id
    await state.update_data(pet_name=message.text)
    await state.set_state(ProfileStates.waiting_for_pet_type)
    
    await message.answer(
        get_text(user_id, "enter_pet_type", language),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )


@router.message(ProfileStates.waiting_for_pet_type)
async def process_pet_type(message: types.Message, state: FSMContext, language: str = "ru"):
    """Process pet type and save profile"""
    user_id = message.from_user.id
    data = await state.get_data()
    
    # TODO: Save to database
    # from app.database import get_db, crud
    # async with get_db() as session:
    #     user = await crud.update_user_profile(
    #         session, user_id,
    #         data.get('owner_name'),
    #         data.get('owner_phone'),
    #         data.get('city')
    #     )
    #     pet = await crud.create_pet(
    #         session, user.id,
    #         data.get('pet_name'),
    #         message.text
    #     )
    
    await state.clear()
    
    profile_text = (
        "✅ <b>Профиль успешно создан!</b>\n\n"
        f"👤 <b>Владелец:</b> {data.get('owner_name')}\n"
        f"📞 <b>Телефон:</b> {data.get('owner_phone')}\n"
        f"🌍 <b>Город:</b> {data.get('city')}\n"
        f"🐾 <b>Питомец:</b> {data.get('pet_name')}\n"
        f"📋 <b>Вид:</b> {message.text}"
    )
    
    await message.answer(
        profile_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_profile_menu(user_id, language)
    )


@router.callback_query(F.data == "profile_view")
async def view_profile(callback: types.CallbackQuery, language: str = "ru"):
    """View owner profile"""
    user_id = callback.from_user.id
    
    # TODO: Get from database
    # For now, show empty profile
    text = get_text(user_id, "profile_empty", language)
    
    await safe_edit_message(
        callback.message,
        text,
        reply_markup=get_profile_menu(user_id, language)
    )
    await callback.answer()


# ==================== VET PROFILE ====================

@router.callback_query(F.data == "create_vet_profile")
async def start_create_vet_profile(callback: types.CallbackQuery, state: FSMContext, language: str = "ru"):
    """Start creating vet profile"""
    user_id = callback.from_user.id
    await state.set_state(VetProfileStates.waiting_for_vet_name)
    
    await safe_edit_message(
        callback.message,
        "👨‍⚕️ <b>Создание профиля ветеринара</b>\n\nВведите ваше полное имя:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )
    await callback.answer()


@router.message(VetProfileStates.waiting_for_vet_name)
async def process_vet_name(message: types.Message, state: FSMContext):
    """Process vet name"""
    await state.update_data(vet_name=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_phone)
    
    await message.answer(
        "📞 Введите ваш контактный телефон:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )


@router.message(VetProfileStates.waiting_for_vet_phone)
async def process_vet_phone(message: types.Message, state: FSMContext):
    """Process vet phone"""
    await state.update_data(vet_phone=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_city)
    
    await message.answer(
        "🏙️ Введите город, где вы работаете:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )


@router.message(VetProfileStates.waiting_for_vet_city)
async def process_vet_city(message: types.Message, state: FSMContext):
    """Process vet city"""
    await state.update_data(vet_city=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_specialization)
    
    await message.answer(
        "🎯 Введите вашу специализацию (например: хирург, терапевт, дерматолог):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )


@router.message(VetProfileStates.waiting_for_vet_specialization)
async def process_vet_specialization(message: types.Message, state: FSMContext):
    """Process vet specialization"""
    await state.update_data(vet_specialization=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_experience)
    
    await message.answer(
        "⏳ Введите ваш опыт работы (лет):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )


@router.message(VetProfileStates.waiting_for_vet_experience)
async def process_vet_experience(message: types.Message, state: FSMContext):
    """Process vet experience"""
    await state.update_data(vet_experience=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_education)
    
    await message.answer(
        "🎓 Введите ваше образование:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )


@router.message(VetProfileStates.waiting_for_vet_education)
async def process_vet_education(message: types.Message, state: FSMContext):
    """Process vet education"""
    await state.update_data(vet_education=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_telegram)
    
    await message.answer(
        "💬 Введите ссылку на ваш Telegram аккаунт (например: @username):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )


@router.message(VetProfileStates.waiting_for_vet_telegram)
async def process_vet_telegram(message: types.Message, state: FSMContext):
    """Process vet telegram"""
    await state.update_data(vet_telegram=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_consultation_price)
    
    await message.answer(
        "💰 Введите стоимость консультации (например: 50$ или бесплатно):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )


@router.message(VetProfileStates.waiting_for_vet_consultation_price)
async def process_vet_consultation_price(message: types.Message, state: FSMContext):
    """Process vet consultation price"""
    await state.update_data(vet_consultation_price=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_info)
    
    await message.answer(
        "📝 Напишите дополнительную информацию о себе и ваших услугах:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )


@router.message(VetProfileStates.waiting_for_vet_info)
async def process_vet_info(message: types.Message, state: FSMContext, language: str = "ru"):
    """Process vet info and save vet profile"""
    user_id = message.from_user.id
    data = await state.update_data(vet_info=message.text)
    
    # TODO: Save to database
    # from app.database import get_db, crud
    # async with get_db() as session:
    #     user = await crud.get_user(session, user_id)
    #     vet_profile = await crud.create_vet_profile(
    #         session, user.id, ...
    #     )
    
    await state.clear()
    
    profile_text = (
        "✅ <b>Профиль ветеринара успешно создан!</b>\n\n"
        "👨‍⚕️ <b>ПРОФИЛЬ ВЕТЕРИНАРА</b>\n"
        "═════════════════════════\n"
        f"<b>👨 Имя:</b> {data.get('vet_name')}\n"
        f"<b>📞 Телефон:</b> {data.get('vet_phone')}\n"
        f"<b>🏙️ Город:</b> {data.get('vet_city')}\n"
        f"<b>🎯 Специализация:</b> {data.get('vet_specialization')}\n"
        f"<b>⏳ Опыт работы:</b> {data.get('vet_experience')} лет\n"
        f"<b>🎓 Образование:</b> {data.get('vet_education')}\n"
        f"<b>💬 Telegram:</b> {data.get('vet_telegram')}\n"
        f"<b>💰 Консультация:</b> {data.get('vet_consultation_price')}\n"
        f"<b>📝 О себе:</b>\n{data.get('vet_info')}\n"
        "═════════════════════════"
    )
    
    await message.answer(
        profile_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_profile_menu(user_id, language)
    )


@router.callback_query(F.data == "vet_profile_view")
async def view_vet_profile(callback: types.CallbackQuery, language: str = "ru"):
    """View vet profile"""
    user_id = callback.from_user.id
    
    # TODO: Get from database
    text = get_text(user_id, "vet_profile_empty", language)
    
    await safe_edit_message(
        callback.message,
        text,
        reply_markup=get_profile_menu(user_id, language)
    )
    await callback.answer()


@router.callback_query(F.data == "profile_clear")
async def clear_profile(callback: types.CallbackQuery, language: str = "ru"):
    """Clear profile"""
    user_id = callback.from_user.id
    
    # TODO: Clear from database
    
    await callback.answer("✅ Профиль очищен!")
    
    # Return to main menu
    from app.handlers.start import back_to_main_menu
    await back_to_main_menu(callback, None, language)
