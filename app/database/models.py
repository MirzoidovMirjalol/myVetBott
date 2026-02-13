"""
SQLAlchemy database models
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all models"""
    pass


class User(Base):
    """User model - pet owners and veterinarians"""
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    language: Mapped[str] = mapped_column(String(2), default="ru")
    
    # Owner profile fields
    owner_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    owner_phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    pets: Mapped[list["Pet"]] = relationship("Pet", back_populates="owner", cascade="all, delete-orphan")
    vet_profile: Mapped[Optional["VetProfile"]] = relationship("VetProfile", back_populates="user", uselist=False)
    reminders: Mapped[list["Reminder"]] = relationship("Reminder", back_populates="user", cascade="all, delete-orphan")
    ads: Mapped[list["Ad"]] = relationship("Ad", back_populates="user", cascade="all, delete-orphan")
    history: Mapped[list["History"]] = relationship("History", back_populates="user", cascade="all, delete-orphan")


class Pet(Base):
    """Pet model"""
    __tablename__ = "pets"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    
    name: Mapped[str] = mapped_column(String(255))
    pet_type: Mapped[str] = mapped_column(String(100))  # dog, cat, bird, etc.
    breed: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    weight: Mapped[Optional[float]] = mapped_column(nullable=True)
    color: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Medical information
    allergies: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    diseases: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    vaccinations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="pets")


class VetProfile(Base):
    """Veterinarian profile model"""
    __tablename__ = "vet_profiles"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    
    vet_name: Mapped[str] = mapped_column(String(255))
    vet_phone: Mapped[str] = mapped_column(String(50))
    vet_city: Mapped[str] = mapped_column(String(100))
    specialization: Mapped[str] = mapped_column(String(255))
    experience_years: Mapped[int] = mapped_column(Integer)
    education: Mapped[str] = mapped_column(Text)
    telegram_contact: Mapped[str] = mapped_column(String(255))
    consultation_price: Mapped[str] = mapped_column(String(100))
    additional_info: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="vet_profile")


class Clinic(Base):
    """Veterinary clinic model"""
    __tablename__ = "clinics"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    name: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(100), index=True)
    address: Mapped[str] = mapped_column(String(500))
    phone: Mapped[str] = mapped_column(String(50))
    working_hours: Mapped[str] = mapped_column(String(255))
    clinic_type: Mapped[str] = mapped_column(String(50))  # clinic, pharmacy, shelter
    
    # Location
    latitude: Mapped[Optional[float]] = mapped_column(nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(nullable=True)
    
    # Additional info
    services: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Reminder(Base):
    """Reminder model"""
    __tablename__ = "reminders"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    
    text: Mapped[str] = mapped_column(String(500))
    reminder_type: Mapped[str] = mapped_column(String(50))  # one_time, daily, weekly, custom
    reminder_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    reminder_time: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    reminder_days: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # JSON array of days
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_sent: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="reminders")


class Ad(Base):
    """Advertisement model"""
    __tablename__ = "ads"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    
    title: Mapped[str] = mapped_column(String(255))
    text: Mapped[str] = mapped_column(Text)
    price: Mapped[str] = mapped_column(String(100))
    contact: Mapped[str] = mapped_column(String(255))
    
    # Category
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # sale, adoption, service, etc.
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="ads")


class History(Base):
    """User action history model"""
    __tablename__ = "history"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    
    action: Mapped[str] = mapped_column(String(500))
    action_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # profile, reminder, ad, etc.
    metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="history")


class Symptom(Base):
    """Symptom check history model"""
    __tablename__ = "symptoms"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    
    pet_type: Mapped[str] = mapped_column(String(100))
    symptoms_text: Mapped[str] = mapped_column(Text)
    recommendations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
