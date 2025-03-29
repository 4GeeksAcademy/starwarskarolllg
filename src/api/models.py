import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False, unique=False)
    favorites = relationship("Favorite", back_populates="user")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

class Character(Base):
    __tablename__ = 'character'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(500), nullable=False)
    favorites = relationship("Favorite", back_populates="character")

def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

class Planet(Base):
    __tablename__ = 'planet'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    planet_name = Column(String(150), unique=True, nullable=False)
    description = Column(String(500), nullable=False)
    favorites = relationship("Favorite", back_populates="planet")

def to_dict(self):
        return {
            "id": self.id,
            "planet_name": self.planet_name,
            "description": self.description
        }

class Favorite(Base):
    __tablename__ = 'favorites'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    character_id = Column(Integer, ForeignKey('character.id'))
    planet_id = Column(Integer, ForeignKey('planet.id'))
    user = relationship("User", back_populates="favorites")
    character = relationship("Character", back_populates="favorites")
    planet = relationship("Planet", back_populates="favorites")

def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "user": self.user.name if self.user else None,  # Incluye el nombre del usuario si existe
            "character": self.character.name if self.character else None,  # Incluye el nombre del personaje si existe
            "planet": self.planet.planet_name if self.planet else None  # Incluye el nombre del planeta si existe
        }

## Draw from SQLAlchemy base
render_er(Base, 'diagramastarwrs.png')