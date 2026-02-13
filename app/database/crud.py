"""
CRUD operations for database models
"""

from typing import Optional, List
from datetime import datetime
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import User, Pet, VetProfile, Clinic, Reminder, Ad, History, Symptom


# ==================== USER OPERATIONS ====================

async def get_user(session: AsyncSession, telegram_id: int) -> Optional[User]:
    """Get user by telegram ID"""
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    return result.scalar_one_or_none()


async def create_user(
    session: AsyncSession,
    telegram_id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    language: str = "ru"
) -> User:
    """Create new user"""
    user = User(
        telegram_id=telegram_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        language=language,
    )
    session.add(user)
    await session.flush()
    return user


async def update_user_profile(
    session: AsyncSession,
    telegram_id: int,
    owner_name: Optional[str] = None,
    owner_phone: Optional[str] = None,
    city: Optional[str] = None,
) -> Optional[User]:
    """Update user profile"""
    user = await get_user(session, telegram_id)
    if not user:
        return None
    
    if owner_name is not None:
        user.owner_name = owner_name
    if owner_phone is not None:
        user.owner_phone = owner_phone
    if city is not None:
        user.city = city
    
    user.updated_at = datetime.utcnow()
    await session.flush()
    return user


async def update_user_language(
    session: AsyncSession,
    telegram_id: int,
    language: str
) -> Optional[User]:
    """Update user language preference"""
    user = await get_user(session, telegram_id)
    if not user:
        return None
    
    user.language = language
    user.updated_at = datetime.utcnow()
    await session.flush()
    return user


# ==================== PET OPERATIONS ====================

async def create_pet(
    session: AsyncSession,
    owner_id: int,
    name: str,
    pet_type: str,
    **kwargs
) -> Pet:
    """Create new pet"""
    pet = Pet(
        owner_id=owner_id,
        name=name,
        pet_type=pet_type,
        **kwargs
    )
    session.add(pet)
    await session.flush()
    return pet


async def get_user_pets(session: AsyncSession, user_id: int) -> List[Pet]:
    """Get all pets for a user"""
    result = await session.execute(
        select(Pet).where(Pet.owner_id == user_id)
    )
    return list(result.scalars().all())


# ==================== VET PROFILE OPERATIONS ====================

async def create_vet_profile(
    session: AsyncSession,
    user_id: int,
    vet_name: str,
    vet_phone: str,
    vet_city: str,
    specialization: str,
    experience_years: int,
    education: str,
    telegram_contact: str,
    consultation_price: str,
    additional_info: Optional[str] = None,
) -> VetProfile:
    """Create veterinarian profile"""
    vet_profile = VetProfile(
        user_id=user_id,
        vet_name=vet_name,
        vet_phone=vet_phone,
        vet_city=vet_city,
        specialization=specialization,
        experience_years=experience_years,
        education=education,
        telegram_contact=telegram_contact,
        consultation_price=consultation_price,
        additional_info=additional_info,
    )
    session.add(vet_profile)
    await session.flush()
    return vet_profile


async def get_vet_profile(session: AsyncSession, user_id: int) -> Optional[VetProfile]:
    """Get vet profile by user ID"""
    result = await session.execute(
        select(VetProfile).where(VetProfile.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def get_active_vets(session: AsyncSession, city: Optional[str] = None) -> List[VetProfile]:
    """Get all active veterinarians, optionally filtered by city"""
    query = select(VetProfile).where(VetProfile.is_active == True)
    
    if city:
        query = query.where(VetProfile.vet_city == city)
    
    result = await session.execute(query)
    return list(result.scalars().all())


# ==================== REMINDER OPERATIONS ====================

async def create_reminder(
    session: AsyncSession,
    user_id: int,
    text: str,
    reminder_type: str,
    **kwargs
) -> Reminder:
    """Create new reminder"""
    reminder = Reminder(
        user_id=user_id,
        text=text,
        reminder_type=reminder_type,
        **kwargs
    )
    session.add(reminder)
    await session.flush()
    return reminder


async def get_user_reminders(
    session: AsyncSession,
    user_id: int,
    active_only: bool = True
) -> List[Reminder]:
    """Get all reminders for a user"""
    query = select(Reminder).where(Reminder.user_id == user_id)
    
    if active_only:
        query = query.where(Reminder.is_active == True)
    
    result = await session.execute(query)
    return list(result.scalars().all())


# ==================== AD OPERATIONS ====================

async def create_ad(
    session: AsyncSession,
    user_id: int,
    title: str,
    text: str,
    price: str,
    contact: str,
    category: Optional[str] = None,
) -> Ad:
    """Create new advertisement"""
    ad = Ad(
        user_id=user_id,
        title=title,
        text=text,
        price=price,
        contact=contact,
        category=category,
    )
    session.add(ad)
    await session.flush()
    return ad


async def get_user_ads(
    session: AsyncSession,
    user_id: int,
    active_only: bool = True
) -> List[Ad]:
    """Get all ads for a user"""
    query = select(Ad).where(Ad.user_id == user_id)
    
    if active_only:
        query = query.where(Ad.is_active == True)
    
    result = await session.execute(query)
    return list(result.scalars().all())


async def get_all_ads(
    session: AsyncSession,
    limit: int = 50,
    active_only: bool = True
) -> List[Ad]:
    """Get all advertisements"""
    query = select(Ad)
    
    if active_only:
        query = query.where(Ad.is_active == True)
    
    query = query.order_by(Ad.created_at.desc()).limit(limit)
    
    result = await session.execute(query)
    return list(result.scalars().all())


# ==================== HISTORY OPERATIONS ====================

async def add_history(
    session: AsyncSession,
    user_id: int,
    action: str,
    action_type: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> History:
    """Add history entry"""
    history = History(
        user_id=user_id,
        action=action,
        action_type=action_type,
        metadata=metadata,
    )
    session.add(history)
    await session.flush()
    return history


async def get_user_history(
    session: AsyncSession,
    user_id: int,
    limit: int = 50
) -> List[History]:
    """Get user history"""
    result = await session.execute(
        select(History)
        .where(History.user_id == user_id)
        .order_by(History.created_at.desc())
        .limit(limit)
    )
    return list(result.scalars().all())


# ==================== CLINIC OPERATIONS ====================

async def get_clinics_by_city(
    session: AsyncSession,
    city: str,
    clinic_type: Optional[str] = None
) -> List[Clinic]:
    """Get clinics by city and type"""
    query = select(Clinic).where(
        Clinic.city == city,
        Clinic.is_active == True
    )
    
    if clinic_type:
        query = query.where(Clinic.clinic_type == clinic_type)
    
    result = await session.execute(query)
    return list(result.scalars().all())


# ==================== SYMPTOM OPERATIONS ====================

async def create_symptom_record(
    session: AsyncSession,
    user_id: int,
    pet_type: str,
    symptoms_text: str,
    recommendations: Optional[str] = None,
) -> Symptom:
    """Create symptom check record"""
    symptom = Symptom(
        user_id=user_id,
        pet_type=pet_type,
        symptoms_text=symptoms_text,
        recommendations=recommendations,
    )
    session.add(symptom)
    await session.flush()
    return symptom
