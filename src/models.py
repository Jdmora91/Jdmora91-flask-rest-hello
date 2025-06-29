from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False) 
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    subscription_date: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")

class Character(db.Model):
    __tablename__ = 'characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    height: Mapped[float] = mapped_column(nullable=False)
    weight: Mapped[float] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)

    favorites = relationship("Favorite", back_populates="character")

class Planet(db.Model):
    __tablename__ = 'planets'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    diameter: Mapped[float] = mapped_column(nullable=False)
    weather: Mapped[str] = mapped_column(String(120), nullable=False)
    population: Mapped[int] = mapped_column(nullable=False)

    favorites = relationship("Favorite", back_populates="planet")

class Starship(db.Model):
    __tablename__ = 'starships'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    model: Mapped[str] = mapped_column(String(120), nullable=False)
    max_speed: Mapped[int] = mapped_column(nullable=False)
    passengers: Mapped[int] = mapped_column(nullable=False)

    favorites = relationship("Favorite", back_populates="starship")

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    starship_id: Mapped[int] = mapped_column(ForeignKey('starships.id'), nullable=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'), nullable=True)
    character_id: Mapped[int] = mapped_column(ForeignKey('characters.id'), nullable=True)
   
    # Relationships
    user = relationship("User", back_populates="favorites")
    character = relationship("Character", back_populates="favorites")
    planet = relationship("Planet", back_populates="favorites")
    starship = relationship("Starship", back_populates="favorites")

    # Restrict user to have only one favorite of each type
    __table_args__ = (
        CheckConstraint(
            'CASE WHEN character_id IS NOT NULL THEN 1 ELSE 0 END + '
            'CASE WHEN planet_id IS NOT NULL THEN 1 ELSE 0 END + '
            'CASE WHEN starship_id IS NOT NULL THEN 1 ELSE 0 END = 1',
            name='single_favorite_check'
        ),
        db.UniqueConstraint('user_id', 'character_id', name='unique_character_favorite'),
        db.UniqueConstraint('user_id', 'planet_id', name='unique_planet_favorite'),
        db.UniqueConstraint('user_id', 'starship_id', name='unique_starship_favorite')
    )

    