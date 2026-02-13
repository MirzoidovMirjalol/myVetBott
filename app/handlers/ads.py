"""
Advertisement handlers
"""

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode

from app.locales import get_text
from app.keyboards.inline import get_ads_menu
from app.utils.helpers import safe_edit_message

router = Router()


class AdStates(StatesGroup):
    waiting_for_ad_title = State()
    waiting_for_ad_text = State()
    waiting_for_ad_price = State()
    waiting_for_ad_contact = State()


@router.callback_query(F.data == "menu_ads")
async def ads_menu(callback: types.CallbackQuery, language: str = "ru"):
    """Show ads menu"""
    user_id = callback.from_user.id
    
    await safe_edit_message(
        callback.message,
        get_text(user_id, "ads_section", language),
        reply_markup=get_ads_menu(user_id, language)
    )
    await callback.answer()


@router.callback_query(F.data == "post_ad")
async def post_ad(callback: types.CallbackQuery, state: FSMContext):
    """Start posting an ad"""
    await state.set_state(AdStates.waiting_for_ad_title)
    
    await safe_edit_message(
        callback.message,
        "📝 <b>Создание объявления</b>\n\nВведите заголовок объявления:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_ads")]
        ])
    )
    await callback.answer()


@router.message(AdStates.waiting_for_ad_title)
async def process_ad_title(message: types.Message, state: FSMContext):
    """Process ad title"""
    await state.update_data(ad_title=message.text)
    await state.set_state(AdStates.waiting_for_ad_text)
    
    await message.answer(
        "📄 Введите текст объявления:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_ads")]
        ])
    )


@router.message(AdStates.waiting_for_ad_text)
async def process_ad_text(message: types.Message, state: FSMContext):
    """Process ad text"""
    await state.update_data(ad_text=message.text)
    await state.set_state(AdStates.waiting_for_ad_price)
    
    await message.answer(
        "💰 Введите цену (или 'Бесплатно', 'Договорная'):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_ads")]
        ])
    )


@router.message(AdStates.waiting_for_ad_price)
async def process_ad_price(message: types.Message, state: FSMContext):
    """Process ad price"""
    await state.update_data(ad_price=message.text)
    await state.set_state(AdStates.waiting_for_ad_contact)
    
    await message.answer(
        "📞 Введите контактную информацию (телефон или Telegram):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_ads")]
        ])
    )


@router.message(AdStates.waiting_for_ad_contact)
async def process_ad_contact(message: types.Message, state: FSMContext, language: str = "ru"):
    """Process ad contact and save ad"""
    user_id = message.from_user.id
    data = await state.get_data()
    
    # TODO: Save to database
    # from app.database import get_db, crud
    # async with get_db() as session:
    #     ad = await crud.create_ad(
    #         session, user_id,
    #         data.get('ad_title'),
    #         data.get('ad_text'),
    #         data.get('ad_price'),
    #         message.text
    #     )
    
    await state.clear()
    
    ad_text = (
        f"✅ <b>Объявление опубликовано!</b>\n\n"
        f"<b>Заголовок:</b> {data.get('ad_title')}\n"
        f"<b>Описание:</b> {data.get('ad_text')}\n"
        f"<b>Цена:</b> {data.get('ad_price')}\n"
        f"<b>Контакты:</b> {message.text}"
    )
    
    await message.answer(
        ad_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_ads_menu(user_id, language)
    )


@router.callback_query(F.data == "my_ads")
async def show_my_ads(callback: types.CallbackQuery, language: str = "ru"):
    """Show user's ads"""
    user_id = callback.from_user.id
    
    # TODO: Get from database
    text = "📭 <b>У вас нет опубликованных объявлений</b>"
    
    await safe_edit_message(
        callback.message,
        text,
        reply_markup=get_ads_menu(user_id, language)
    )
    await callback.answer()


@router.callback_query(F.data == "view_ads")
async def view_ads(callback: types.CallbackQuery, language: str = "ru"):
    """View all ads"""
    user_id = callback.from_user.id
    
    # TODO: Get from database
    text = "📭 <b>Пока нет объявлений</b>\n\nСтаньте первым, кто опубликует объявление!"
    
    await safe_edit_message(
        callback.message,
        text,
        reply_markup=get_ads_menu(user_id, language)
    )
    await callback.answer()
