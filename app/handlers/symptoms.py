"""
Symptom checking handlers
"""

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode

from app.locales import get_text
from app.keyboards.inline import create_animal_type_keyboard
from app.services.symptom_checker import analyze_symptoms, is_emergency
from app.utils.helpers import safe_edit_message

router = Router()


class SymptomsStates(StatesGroup):
    waiting_for_pet_type = State()
    waiting_for_symptoms = State()


@router.callback_query(F.data == "menu_symptoms")
async def symptoms_menu(callback: types.CallbackQuery, language: str = "ru"):
    """Show symptoms checker menu"""
    user_id = callback.from_user.id
    
    await safe_edit_message(
        callback.message,
        get_text(user_id, "symptoms_section", language),
        reply_markup=create_animal_type_keyboard(language)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("animal_"))
async def process_animal_type(callback: types.CallbackQuery, state: FSMContext):
    """Process animal type selection"""
    animal_type = callback.data.replace("animal_", "")
    
    await state.update_data(pet_type=animal_type)
    await state.set_state(SymptomsStates.waiting_for_symptoms)
    
    animal_names = {
        "dog": "собаки",
        "cat": "кошки",
        "rodent": "грызуна",
        "bird": "птицы",
        "fish": "рыбок"
    }
    
    animal_name = animal_names.get(animal_type, "животного")
    
    await safe_edit_message(
        callback.message,
        f"🩺 <b>Проверка симптомов у {animal_name}</b>\n\n"
        f"Опишите симптомы вашего питомца (что вас беспокоит, как давно, дополнительные детали):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_symptoms")]
        ])
    )
    await callback.answer()


@router.message(SymptomsStates.waiting_for_symptoms)
async def process_symptoms(message: types.Message, state: FSMContext):
    """Process symptoms and provide recommendations"""
    user_id = message.from_user.id
    data = await state.get_data()
    
    symptoms_text = message.text
    pet_type = data.get('pet_type', 'unknown')
    
    # TODO: Save to database
    # from app.database import get_db, crud
    # async with get_db() as session:
    #     await crud.create_symptom_record(
    #         session, user_id, pet_type, symptoms_text
    #     )
    
    # Check if emergency
    if is_emergency(symptoms_text):
        emergency_text = (
            "🚨 <b>ЭКСТРЕННАЯ СИТУАЦИЯ!</b>\n\n"
            "Обнаружены симптомы, требующие немедленной медицинской помощи!\n\n"
            "⚠️ <b>СРОЧНО обратитесь к ветеринару или в ближайшую клинику!</b>\n\n"
        )
        response = emergency_text + analyze_symptoms(symptoms_text, pet_type)
    else:
        response = analyze_symptoms(symptoms_text, pet_type)
    
    await state.clear()
    
    await message.answer(
        response,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📍 Найти клинику", callback_data="menu_clinics")],
            [InlineKeyboardButton(text="💬 Чат с ветер.", callback_data="menu_vet_chat")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")]
        ])
    )
