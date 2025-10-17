from __future__ import annotations
from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey

db = SQLAlchemy()

# Modelo User, que representa a los usuarios de la aplicación


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
    favorites_starships: Mapped[list['FavoritesStarships']
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

# Modelo Characters, que representa a los personajes de Star Wars


class Characters(db.Model):
    __tablename__ = 'characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    height: Mapped[int] = mapped_column(Integer)
    weight: Mapped[int] = mapped_column(Integer)
    favorites_by: Mapped[list['FavoritesCharacters']
                         ] = relationship(back_populates='character')

    def __repr__(self):
        return f'<Personaje {self.name}>'

# Modelo FavoritesCharacters, que representa los personajes favoritos de los usuarios


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

# Modelo Planets, que representa a los planetas de Star Wars


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

# Modelo FavoritesPlanets, que representa los planetas favoritos de los usuarios


class FavoritesPlanets(db.Model):
    __tablename__ = 'favorites_planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    user: Mapped['User'] = relationship(
        back_populates='favorites_planets')

    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'))
    planet: Mapped['Planets'] = relationship(back_populates='favorites_by')

    def __repr__(self):
        return f'Al usuario {self.user.id} le gusta el planeta {self.planet.name}'

# Modelo Starships, que representa a las naves espaciales de Star Wars


class Starships(db.Model):
    __tablename__ = 'starships'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    favorites_by: Mapped[list['FavoritesStarships']
                         ] = relationship(back_populates='starship')

    def __repr__(self):
        return f'<Starship {self.name}>'

# Modelo FavoritesStarships, que representa las naves espaciales favoritas de los usuarios


class FavoritesStarships(db.Model):
    __tablename__ = 'favorites_starships'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    user: Mapped['User'] = relationship(
        back_populates='favorites_starships')

    starship_id: Mapped[int] = mapped_column(ForeignKey('starships.id'))
    starship: Mapped['Starships'] = relationship(back_populates='favorites_by')

    def __repr__(self):
        return f'Al usuario {self.user.id} le gusta la nave {self.starship.name}'
