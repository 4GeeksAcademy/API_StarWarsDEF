from __future__ import annotations
from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorites: Mapped[list['FavoritesCharacters']] = relationship(
        back_populates='user')           
    favorites_planets: Mapped[list['FavoritesPlanets']
                              ] = relationship(back_populates='user')

    def __repr__(self):
        return f'<Usuario {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "is_active": self.is_active,
        }


class Characters(db.Model):
    _tablename__ = 'characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    height: Mapped[int] = mapped_column(Integer)
    weight: Mapped[int] = mapped_column(Integer)
    favorites_by: Mapped[list['FavoritesCharacters']
                         ] = relationship(back_populates='character')

    def __repr__(self):
        return f'<Personaje {self.name}>'


class FavoritesCharacters(db.Model):
    __tablename__ = 'favorites_characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

   
    user: Mapped['User'] = relationship(
        back_populates='favorites')     

    character_id: Mapped[int] = mapped_column(ForeignKey('characters.id'))
    character: Mapped['Characters'] = relationship(
        back_populates='favorites_by')

    def __repr__(self):
        return f'Al usuario {self.user.id} le gusta el personaje {self.character.name}'


class Planets(db.Model):
    __tablename__ = 'planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    diameter: Mapped[int] = mapped_column(Integer)
    population: Mapped[int] = mapped_column(Integer)
    favorites_by: Mapped[list['FavoritesPlanets']
                         ] = relationship(back_populates='planet')

    def __repr__(self):
        return f'<Planet {self.name}>'


class FavoritesPlanets(db.Model):
    __tablename__ = 'favorites_planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    # antes: users = relationship(back_populates='favorites_planets')
    user: Mapped['User'] = relationship(
        back_populates='favorites_planets')   # <- singular

    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'))
    planet: Mapped['Planets'] = relationship(back_populates='favorites_by')

    def __repr__(self):
        return f'Al usuario {self.user.id} le gusta el planeta {self.planet.name}'

