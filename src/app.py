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
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
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

@app.route('/user', methods=['GET'])
def handle_hello():
    users = User.query.all() #SELECT * FROM 'user'
    print(users) #[Usuario]
    print(type(users[0])) #<class 'models.User'>
    user1 = users[0].serialize()
    users_serialized = []
    for user in users:
       users_serialized.append(user.serialize())
    print(user1) #esto si es un diccionario
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "users": users_serialized
    }

    return jsonify(response_body), 200

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

@app.route('/user_favorites/<int:user_id>', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    print(user)
    if user is None:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    favorites = user.favorites
    return jsonify({"msg": "Favoritos del usuario", "favorites": [f.serialize() for f in favorites]}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
