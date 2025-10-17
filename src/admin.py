import os
from flask_admin import Admin
from models import db, User, Characters, FavoritesCharacters, Planets, FavoritesPlanets, Starships, FavoritesStarships
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import relationship

# Vistas para el panel de administración


# UsersModelView sirve para administrar los usuarios
class UsersModelView(ModelView):
    column_auto_selected = True
    column_list = ['id', 'email', 'is_active',
                   'favorites', 'favorites_planets']


# CharactersModelView sirve para administrar los personajes
class CharactersModelView(ModelView):
    column_auto_selected = True
    column_list = ['id', 'name', 'height', 'weight', 'favorites_by']


# FavoritesCharactersModelView sirve para administrar los favoritos de personajes
class FavoritesCharactersModelView(ModelView):
    column_auto_selected = True
    column_list = ['id', 'user_id', 'users', 'character_id', 'character']


# PlanetsModelView sirve para administrar los planetas en el panel de administración
class PlanetsModelView(ModelView):
    column_auto_selected = True
    column_list = ['id', 'name', 'diameter', 'population', 'favorites_by']


# FavoritesPlanetsModelView sirve para administrar los favoritos de planetas en el panel de administración
class FavoritesPlanetsModelView(ModelView):
    column_auto_selected = True
    column_list = ['id', 'user_id', 'users', 'planet_id', 'planet']


# StarshipsModelView sirve para administrar las naves espaciales en el panel de administración
class StarshipsModelView(ModelView):
    column_auto_selected = True
    column_list = ['id', 'name', 'model', 'favorites_by']


# FavoritesStarshipsModelView sirve para administrar los favoritos de naves espaciales en el panel de administración
class FavoritesStarshipsModelView(ModelView):
    column_auto_selected = True
    column_list = ['id', 'user_id', 'users', 'starship_id', 'starship']


# Función para configurar el admin
def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Aqui estan los modelos que deben ir en el admin
    admin.add_view(UsersModelView(User, db.session))
    admin.add_view(CharactersModelView(Characters, db.session))
    admin.add_view(FavoritesCharactersModelView(
        FavoritesCharacters, db.session))
    admin.add_view(PlanetsModelView(Planets, db.session))
    admin.add_view(FavoritesPlanetsModelView(FavoritesPlanets, db.session))
    admin.add_view(StarshipsModelView(Starships, db.session))
    admin.add_view(FavoritesStarshipsModelView(FavoritesStarships, db.session))
    print("El panel de administración ha sido configurado.")
