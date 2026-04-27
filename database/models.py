from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    is_premium = Column(Boolean, default=False)
    premium_expire = Column(DateTime, nullable=True)
    daily_requests_count = Column(Integer, default=0)
    last_request_date = Column(DateTime, default=datetime.utcnow)
    registered_at = Column(DateTime, default=datetime.utcnow)
    referrer_id = Column(BigInteger, nullable=True)
    referral_count = Column(Integer, default=0)
    referral_link = Column(String, nullable=True)

class RecipeLog(Base):
    __tablename__ = "recipe_logs"

    id = Column(Integer, primary_key=True)
    user_telegram_id = Column(BigInteger, nullable=False)
    ingredients_input = Column(String, nullable=True)
    ai_response = Column(String, nullable=True)
    mode = Column(String, default="basic")
    created_at = Column(DateTime, default=datetime.utcnow)

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    user_telegram_id = Column(BigInteger, nullable=False)
    recipe_text = Column(String, nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)

class Partner(Base):
    __tablename__ = "partners"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=True)
    referral_url = Column(String, nullable=False)
    promo_code = Column(String, nullable=True)
    active = Column(Boolean, default=True)
