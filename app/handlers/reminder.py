"""
Reminder handlers
"""

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode

from app.locales import get_text
from app.keyboards.inline import get_reminders_menu, create_reminder_keyboard
from app.utils.helpers import safe_edit_message

router = Router()


class ReminderStates(StatesGroup):
    waiting_for_reminder_type = State()
    waiting_for_reminder_text = State()
    waiting_for_reminder_date = State()
    waiting_for_reminder_time = State()
    waiting_for_reminder_days = State()


@router.callback_query(F.data == "menu_reminders")
async def reminders_menu(callback: types.CallbackQuery, language: str = "ru"):
    """Show reminders menu"""
    user_id = callback.from_user.id
    
    await safe_edit_message(
        callback.message,
        get_text(user_id, "reminders_section", language),
        reply_markup=get_reminders_menu(user_id, language)
    )
    await callback.answer()


@router.callback_query(F.data == "reminder_add")
async def add_reminder(callback: types.CallbackQuery, state: FSMContext, language: str = "ru"):
    """Start adding a reminder"""
    user_id = callback.from_user.id
    await state.set_state(ReminderStates.waiting_for_reminder_type)
    
    await safe_edit_message(
        callback.message,
        get_text(user_id, "reminder_types", language),
        reply_markup=create_reminder_keyboard(language)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("reminder_"))
async def process_reminder_type(callback: types.CallbackQuery, state: FSMContext):
    """Process reminder type selection"""
    if callback.data == "reminder_add":
        # This is handled by add_reminder
        return
    
    reminder_type = callback.data
    await state.update_data(reminder_type=reminder_type)
    await state.set_state(ReminderStates.waiting_for_reminder_text)
    
    await safe_edit_message(
        callback.message,
        "📝 Введите текст напоминания (например: 'Дать лекарство коту', 'Вакцинация собаки'):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_reminders")]
        ])
    )
    await callback.answer()


@router.message(ReminderStates.waiting_for_reminder_text)
async def process_reminder_text(message: types.Message, state: FSMContext):
    """Process reminder text"""
    data = await state.get_data()
    reminder_type = data.get('reminder_type')
    
    await state.update_data(reminder_text=message.text)
    
    if reminder_type == "reminder_one_time":
        await state.set_state(ReminderStates.waiting_for_reminder_date)
        await message.answer(
            "📅 Введите дату напоминания (в формате ДД.ММ.ГГГГ, например: 25.12.2024):",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_reminders")]
            ])
        )
    elif reminder_type == "reminder_daily":
        await state.set_state(ReminderStates.waiting_for_reminder_time)
        await message.answer(
            "⏰ Введите время напоминания (в формате ЧЧ:ММ, например: 09:00):",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_reminders")]
            ])
        )
    elif reminder_type == "reminder_weekly":
        await state.set_state(ReminderStates.waiting_for_reminder_days)
        await message.answer(
            "📆 Введите дни недели для напоминания (например: ПН,СР,ПТ или понедельник,среда,пятница):",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_reminders")]
            ])
        )
    else:
        await state.set_state(ReminderStates.waiting_for_reminder_date)
        await message.answer(
            "📅 Введите даты напоминаний через запятую (в формате ДД.ММ.ГГГГ):",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_reminders")]
            ])
        )


@router.message(ReminderStates.waiting_for_reminder_date)
async def process_reminder_date(message: types.Message, state: FSMContext, language: str = "ru"):
    """Process reminder date and save"""
    user_id = message.from_user.id
    data = await state.get_data()
    
    # TODO: Save to database
    # from app.database import get_db, crud
    # async with get_db() as session:
    #     reminder = await crud.create_reminder(
    #         session, user_id,
    #         data.get('reminder_text'),
    #         data.get('reminder_type'),
    #         reminder_date=message.text
    #     )
    
    await state.clear()
    
    reminder_type_text = {
        "reminder_one_time": "Один раз",
        "reminder_daily": "Ежедневно",
        "reminder_weekly": "Еженедельно",
        "reminder_custom": "Настроенное"
    }.get(data.get('reminder_type'), "Настроенное")
    
    await message.answer(
        f"✅ <b>Напоминание добавлено!</b>\n\n"
        f"<b>Текст:</b> {data.get('reminder_text')}\n"
        f"<b>Дата:</b> {message.text}\n"
        f"<b>Тип:</b> {reminder_type_text}\n\n"
        f"Я напомню вам в указанное время!",
        parse_mode=ParseMode.HTML,
        reply_markup=get_reminders_menu(user_id, language)
    )


@router.callback_query(F.data == "reminder_list")
async def show_reminders(callback: types.CallbackQuery, language: str = "ru"):
    """Show user's reminders"""
    user_id = callback.from_user.id
    
    # TODO: Get from database
    # For now, show empty list
    text = "📭 <b>У вас нет активных напоминаний</b>"
    
    await safe_edit_message(
        callback.message,
        text,
        reply_markup=get_reminders_menu(user_id, language)
    )
    await callback.answer()
