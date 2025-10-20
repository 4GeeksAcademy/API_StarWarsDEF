"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Ruta GET/users que devuelve todos los usuarios (Funciona)
@app.route('/users', methods=['GET'])
def handle_hello():
    users = User.query.all()  # SELECT * FROM 'user'
    print(users)  # [Usuario]
    print(type(users[0]))  # <class 'models.User'>
    user1 = users[0].serialize()
    users_serialized = []
    for user in users:
        users_serialized.append(user.serialize())
    print(user1)  # esto si es un diccionario
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "users": users_serialized
    }

    return jsonify(response_body), 200


#GET characters que devuelve todos los personajes (Funciona)
@app.route('/characters', methods=['GET'])
def get_characters():
    from models import Characters
    characters = Characters.query.all()
    characters_serialized = [char.serialize() for char in characters]
    return jsonify({"msg": "Lista de personajes", "characters": characters_serialized}), 200

#GET/characters/<int:character_id> que devuelve un personaje por su ID (Funciona)   
@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character_by_id(character_id):
    from models import Characters
    character = Characters.query.get(character_id)
    if character is None:
        return jsonify({"msg": "Personaje no encontrado"}), 404
    return jsonify({"msg": "Personaje encontrado", "character": character.serialize()}), 200



#GET/planets que devuelve todos los planetas (Funciona)    
@app.route('/planets', methods=['GET'])
def get_planets():
    from models import Planets
    planets = Planets.query.all()
    planets_serialized = [planet.serialize() for planet in planets]
    return jsonify({"msg": "Lista de planetas", "planets": planets_serialized}), 200

#GET/planets/<int:planet_id> que devuelve un planeta por su ID (Funciona)
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    from models import Planets
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({"msg": "Planeta no encontrado"}), 404
    return jsonify({"msg": "Planeta encontrado", "planet": planet.serialize()}), 200


# Ruta GET/user/favorites/<int:user_id> Lista todos los favoritos que pertenecen al usuario actual.
@app.route('/user/favorites/<int:user_id>', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    print(user)
    if user is None:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    favorites_characters = user.favorites
    favorites_planets = user.favorites_planets

    return jsonify({
        "msg": "Favoritos del usuario",
        "favorites_characters": [f.serialize() for f in favorites_characters],
        "favorites_planets": [f.serialize() for f in favorites_planets]
    }), 200

# GET/user/fav_characters/<int:user_id> que devuelve los personajes favoritos de un usuario (Funciona)
@app.route('/user/fav_characters/<int:user_id>', methods=['GET'])
def get_user_characters(user_id):
    user = User.query.get(user_id)
    print(user)
    if user is None:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    favorites_characters = user.favorites
    return jsonify({"msg": "Personajes favoritos del usuario", "favorites_characters": [f.serialize() for f in favorites_characters]}), 200


# Ruta GET/user/fav_planets/<int:user_id> que devuelve los favoritos de un usuario de planetas (Funciona)
@app.route('/user/fav_planets/<int:user_id>', methods=['GET'])
def get_user_favorites_planets(user_id):
    user = User.query.get(user_id)
    print(user)
    if user is None:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    favorites_planets = user.favorites_planets
    return jsonify({"msg": "Planetas favoritos del usuario", "favorites_planets": [f.serialize() for f in favorites_planets]}), 200

# Ruta POST/user que crea un nuevo usuario (Funciona)
@app.route('/user', methods=['POST'])
def add_user():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "La petición del body es null"}), 400

    if 'email' not in body:
        return jsonify({"msg": "El email es obligatorio"}), 400
    if 'password' not in body:
        return jsonify({"msg": "La contraseña es obligatoria"}), 400

    print(body)
    new_user = User()
    new_user.email = body['email']
    new_user.password = body['password']
    new_user.is_active = True
    print(new_user)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "Usuario creado exitosamente", "user": new_user.serialize()}), 201

#POST /user/favorites/character que añade un personaje a los favoritos de un usuario (Funciona)
@app.route('/user/favorites/character', methods=['POST'])
def add_favorite_character():       
    from models import FavoritesCharacters
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "La petición del body es null"}), 400

    if 'user_id' not in body:
        return jsonify({"msg": "El user_id es obligatorio"}), 400
    if 'character_id' not in body:
        return jsonify({"msg": "El character_id es obligatorio"}), 400

    new_favorite = FavoritesCharacters()
    new_favorite.user_id = body['user_id']
    new_favorite.character_id = body['character_id']
    print(new_favorite)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"msg": "Personaje añadido a favoritos exitosamente", "favorite_character": new_favorite.serialize()}), 201


#POST /user/favorites/planet que añade un planeta a los favoritos de un usuario (Funciona)
@app.route('/user/favorites/planet', methods=['POST'])
def add_favorite_planet():  
    from models import FavoritesPlanets
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "La petición del body es null"}), 400

    if 'user_id' not in body:
        return jsonify({"msg": "El user_id es obligatorio"}), 400
    if 'planet_id' not in body:
        return jsonify({"msg": "El planet_id es obligatorio"}), 400

    new_favorite = FavoritesPlanets()
    new_favorite.user_id = body['user_id']
    new_favorite.planet_id = body['planet_id']
    print(new_favorite)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"msg": "Planeta añadido a favoritos exitosamente", "favorite_planet": new_favorite.serialize()}), 201


#DELETE /user/favorites/character/<int:favorite_id> que elimina un personaje de los favoritos de un usuario 
@app.route('/user/favorites/character/<int:favorite_id>', methods=['DELETE'])
def delete_favorite_character(favorite_id):
    from models import FavoritesCharacters
    favorite = FavoritesCharacters.query.get(favorite_id)
    if favorite is None:
        return jsonify({"msg": "Favorito no encontrado"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Personaje favorito eliminado exitosamente"}), 200

#DELETE /user/favorites/planet/<int:favorite_id> que elimina un planeta de los favoritos de un usuario
@app.route('/user/favorites/planet/<int:favorite_id>', methods=['DELETE'])
def delete_favorite_planet(favorite_id):
    from models import FavoritesPlanets
    favorite = FavoritesPlanets.query.get(favorite_id)
    if favorite is None:
        return jsonify({"msg": "Favorito no encontrado"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Planeta favorito eliminado exitosamente"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
