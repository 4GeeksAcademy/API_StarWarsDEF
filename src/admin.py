import os
from flask_admin import Admin
from models import db, User, Characters, FavoritesCharacters, Planets, FavoritesPlanets
from flask_admin.contrib.sqla import ModelView


class UsersModelView(ModelView):
    column_auto_selected = True  # Carga las relaciones
    column_list = ['id', 'email', 'is_active', 'favorites', 'favorites_planets']  # Columnas a mostrar
    
class CharactersModelView(ModelView):
    column_auto_selected = True
    column_list = ['id', 'name', 'height', 'weight', 'favorites_by']

class FavoritesCharactersModelView(ModelView):
    column_auto_selected = True
    column_list = ['id', 'user_id', 'users', 'character_id', 'character']

class PlanetsModelView(ModelView):
    column_auto_selected = True
    column_list = ['id', 'name', 'diameter', 'population', 'favorites_by']

class FavoritesPlanetsModelView(ModelView):
    column_auto_selected = True
    column_list = ['id', 'user_id', 'users', 'planet_id', 'planet']


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UsersModelView(User, db.session))
    admin.add_view(CharactersModelView(Characters, db.session))
    admin.add_view(FavoritesCharactersModelView(FavoritesCharacters, db.session))
    admin.add_view(PlanetsModelView(Planets, db.session))
    admin.add_view(FavoritesPlanetsModelView(FavoritesPlanets, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
