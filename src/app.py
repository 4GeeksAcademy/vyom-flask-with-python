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
from models import db, User, Character, Planet, Starship, Favorite
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

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# PIDE LOS DATOS DE TODOS LOS USUARIOS CREADOS
@app.route('/users')
def get_users():
    try:
        users = User.query.all()

        if not users:
            return jsonify({'error': 'No se encuentra resultados'}), 404
        
        list_users = []

        for user in users:
            list_users.append(user.serialize())
        return jsonify(list_users), 200
    
    except Exception as e:
        return jsonify({'error': 'falla en el servidor'}), 500


# PIDE LOS DATOS DE TODOS LOS PERSONAJES CREADOS
@app.route('/people')
def get_people():
    try:
        characters = Character.query.all()

        if not characters:
            return jsonify({
                'Error': "No se encuentran personajes"
            }), 400
        
        list_people = []
        for character in characters:
            list_people.append(character.serialize())
        
        return jsonify(list_people), 200
    except Exception as e:
        return jsonify({'error', 'Falla en el servidor'}), 500

# PIDE LOS DATOS DE UN PERSONAJE CON SU ID
@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id(people_id):
    try:
        character = Character.query.get(people_id)
        
        if character:
            return jsonify(character.serialize()), 200
        else:
            return jsonify({'Error': 'Personaje no econtrado'}), 404
        
    except Exception as e:
        return jsonify({'Error', 'Falla en el servidor'}), 500

# PIDE LOS DATOS DE TODOS LOS PLANETAS CREADOS
@app.route('/planets', methods=['GET'])
def get_planets():
    try:
        planets = Planet.query.all()
        if not planets:
            return jsonify({'error': 'No se encontro planetas'}), 404
        
        list_planets = []
        for planet in planets:
            list_planets.append(planet.serialize())
        
        return jsonify(list_planets), 200
    
    except Exception as e:
        return jsonify({'error', 'Falla en el servidor'}), 500

# PIDE LOS DATOS DE UN PLANETA CON SU ID
@app.route('/planets/<int:planet_id>', methods=["GET"])
def get_planet(planet_id):
    try:
        planet = Planet.query.get(planet_id)

        if planet:
            return jsonify(planet.serialize()), 200
        else:
            return jsonify({'error': 'No se encuentra este planeta'}), 404
        
    except Exception as e:
        return jsonify({'error': 'Falla en el servidor'}), 500

#PEDIMOS TODAS LAS NAVES DISPONIBLES
@app.route('/starships', methods=['GET'])
def get_starships():
    try:
        starships = Starship.query.all()
        if not starships:
            return jsonify({'error': 'No se encontraron naves'}), 404

        list_starships = [starship.serialize() for starship in starships]
        return jsonify(list_starships), 200

    except Exception as e:
        return jsonify({'error': 'Falla en el servidor'}), 500

# PEDIMOS INFO DE UNA NAVE POR ID
@app.route('/starships/<int:starship_id>')
def get_starship_id(starship_id):
    try:
        startship =  Starship.query.get(starship_id)

        if startship:
            return jsonify(startship.serialize()), 200
        else:
            return jsonify({'error': 'No se encuentra esta nave'}), 404
        
    except Exception as e:
        return jsonify({'error': 'Falla en el servidor'}), 500

# PEDIMOS LA LISTA DE FAVORITOS DE USUARIO CURRENT_USER_ID
@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    current_user_id = 5
    try:

        
        favorites =  Favorite.query.filter_by(user_id=current_user_id).all()

        if not favorites:
            return jsonify({'error': 'Este usuario no tiene favoritos'}), 400
        
        list_favorites = [favorite.serialize() for favorite in favorites]

        return jsonify(list_favorites), 200
        
    except Exception as e:
        return jsonify({'error': 'Falla en el servidor'}), 500

# ANADIR PLANETA A LISTA DE FAVORITOS DE USUARIO CURRENT_USER_ID
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    current_user_id = 5

    try:
        planet = Planet.query.get(planet_id)
        if not planet:
            return jsonify({'error': 'Planeta no encontrado'}), 404
        
        existing_favorite = Favorite.query.filter_by(
            user_id=current_user_id,
            planet_id=planet_id
        ).first()
        
        if existing_favorite:
            return jsonify({'error': 'Este planeta ya está en los favoritos del usuario'}), 400
        
        new_favorite = Favorite(
            user_id=current_user_id,
            planet_id=planet_id
        )
        
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify(new_favorite.serialize()), 201
    
    except Exception as e:
        return jsonify({'error': "falla en el servidor"}), 500

# ANADIR PERSONAJE FAVORITO A LISTA DE USUARIO SELECCIONADO EN CURRENT_USER_ID
@app.route('/favorite/people/<int:people_id>', methods=["POST"])
def add_people_favorite(people_id):
    current_user_id = 5

    try:
        character = Character.query.get(people_id)
        if not character:
            return jsonify({'error': 'Personaje no encontrado en la lista'}), 404
    
        existing_favorite = Favorite.query.filter_by(
            user_id = current_user_id,
            character_id = people_id
        ).first()

        if existing_favorite:
            return jsonify({'error': f'Este personaje ya esta en los favoritos del usuario: {current_user_id}'}), 400

        new_favorite = Favorite(
            user_id =  current_user_id,
            character_id = people_id
        )

        db.session.add(new_favorite)
        db.session.commit()

        return jsonify(new_favorite.serialize()), 201
        
    except Exception as e:
        return jsonify({'error': 'Falla en el servidor'}), 500
    
# ANADIR NAVE FAVORITA A LISTA DE USUARIO SELECCIONADO EN CURRENT_USER_ID
@app.route('/favorite/starship/<int:starship_id>', methods=['POST'])
def add_startship_favorite(starship_id):
    current_user_id = 5
    try:
        starship = Starship.query.get(starship_id)
        if not starship:
            return jsonify({'error': 'Nave no encontrada'}), 404

        existing_favorite = Favorite.query.filter_by(
            user_id = current_user_id,
            starship_id = starship_id
        ).first()

        if existing_favorite:
            return jsonify({'error': f'Esta nave ya esta en los favoritos del usuario: {current_user_id}'})
        
        new_favorite = Favorite(
            user_id = current_user_id,
            starship_id = starship_id
        )

        db.session.add(new_favorite)
        db.session.commit()

        return jsonify(new_favorite.serialize()), 201
        
    except Exception as e:
        return jsonify({'error': 'Falla en el servidor'}), 500


# ELIMINAR PERSONAJE DE LA LISTA DE USUARIO SELECCIONADO EN CURRENT_USER_ID
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_character_user(people_id):
    current_user_id = 5
    try:
        character = Character.query.get(people_id)
        if not character:
            return jsonify({'error': 'Personaje no encontrado'}), 404
        
        existing_favorite = Favorite.query.filter_by(
            user_id = current_user_id,
            character_id = people_id
        ).first()

        if existing_favorite:
            db.session.delete(existing_favorite)
            db.session.commit()
            
            updated_favorites = Favorite.query.filter_by(user_id=current_user_id).all()
            favorites_list = [favorite.serialize() for favorite in updated_favorites]

            return jsonify({
                'message': 'Personaje eliminado de favoritos',
                'nueva_lista': favorites_list
            }), 202

        return jsonify({'error': f'El persona no esta en los favoritos del usuario con id: {current_user_id}'}), 400

        
    except Exception as e:
        return jsonify({'error': 'Falla en el servidor'}), 500


# ELIMINAR PLANETA DE LA LISTA DE USUARIO SELECCIONADO EN CURRENT_USER_ID
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_user(planet_id):
    current_user_id = 5
    try:
        planet = Planet.query.get(planet_id)
        if not planet:
            return jsonify({'error': 'Planeta no encontrado'}), 404

        existing_favorite = Favorite.query.filter_by(
            user_id = current_user_id,
            planet_id = planet_id
        ).first()

        if existing_favorite:
            db.session.delete(existing_favorite)
            db.session.commit()

            updated_favorites = Favorite.query.filter_by(user_id = current_user_id).all()
            favorites_list = [favorite.serialize() for favorite in updated_favorites]

            return jsonify({
                'message': 'Planeta eliminado de favoritos',
                'Nueva_lista': favorites_list
            }), 202

        return jsonify({'error': f'El planeta no esta en los favoritos del usuario con id: {current_user_id}'}), 400
        
    except Exception as e:
        return jsonify({'error': 'Falla en el servidor'}), 500


# ELIMINAR NAVE DE LA LISTA DE USUARIO SELECCIONADO EN CURRENT_USER_ID
@app.route('/favorite/starship/<int:starship_id>', methods=['DELETE'])
def delete_starship_user(starship_id):
    current_user_id = 5
    try:
        starship = Starship.query.get(starship_id)
        if not starship:
            return jsonify({'error': 'Nave no encontrada'}), 404

        existing_favorite = Favorite.query.filter_by(
            user_id = current_user_id,
            starship_id = starship_id
        ).first()

        if existing_favorite:
            db.session.delete(existing_favorite)
            db.session.commit()

            updated_favorites = Favorite.query.filter_by(user_id = current_user_id). all()
            favorites_list = [favorite.serialize() for favorite in updated_favorites]

            return jsonify({
                'message': 'Nave eliminada de favoritos',
                'nueva_lista': favorites_list
            }), 202

        return jsonify({'error': f'La nave no esta en los favoritos del usuario con id: {current_user_id}'}), 400
    
    except Exception as e:
        return jsonify({'error': 'Falla en el servidor'}), 500

# @app.route('')

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
