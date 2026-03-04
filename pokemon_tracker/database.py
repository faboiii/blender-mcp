"""SQLite database models and setup for the Pokemon card tracker."""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime, Boolean, create_engine
)
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///./pokemon_cards.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    # Pokemon TCG API data
    api_id = Column(String, unique=True, index=True, nullable=True)
    name = Column(String, nullable=False)
    set_name = Column(String, nullable=True)
    set_id = Column(String, nullable=True)
    number = Column(String, nullable=True)
    rarity = Column(String, nullable=True)
    supertype = Column(String, nullable=True)      # Pokémon, Trainer, Energy
    subtypes = Column(String, nullable=True)       # comma-separated
    hp = Column(Integer, nullable=True)
    types = Column(String, nullable=True)          # comma-separated
    attacks = Column(Text, nullable=True)          # JSON string
    weaknesses = Column(Text, nullable=True)       # JSON string
    resistances = Column(Text, nullable=True)      # JSON string
    retreat_cost = Column(Integer, nullable=True)
    image_url = Column(String, nullable=True)
    image_url_hires = Column(String, nullable=True)
    # Market data
    market_price_low = Column(Float, nullable=True)
    market_price_mid = Column(Float, nullable=True)
    market_price_high = Column(Float, nullable=True)
    market_price_market = Column(Float, nullable=True)
    # User collection data
    condition = Column(String, default="NM")       # PSA condition grade
    quantity = Column(Integer, default=1)
    purchase_price = Column(Float, nullable=True)
    is_foil = Column(Boolean, default=False)
    is_graded = Column(Boolean, default=False)
    grade_score = Column(Float, nullable=True)
    grading_company = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    added_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def create_tables():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
