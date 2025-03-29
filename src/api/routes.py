"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from api.models import db, Users, User, Character, Planet, Favorite
from sqlalchemy.orm import Session

api = Blueprint('api', __name__)
CORS(api) # Allow CORS requests to this API


@api.route('/hello', methods=['GET'])
def handle_hello():
    response_body = {}
    response_body['message'] = "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    return response_body, 200


# [GET] /people - Get a list of all the people in the database
@api.route('/people', methods=['GET'])
def get_people():
    people = Session.query(Character).all()
    return jsonify([person.to_dict() for person in people])


# [GET] /people/<int:people_id> - Get one single person's information
@api.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = Session.query(Character).get(people_id)
    if person:
        return jsonify(person.to_dict())
    return jsonify({"error": "Person not found"}), 404


# [GET] /planets - Get a list of all the planets in the database
@api.route('/planets', methods=['GET'])
def get_planets():
    planets = Session.query(Planet).all()
    return jsonify([planet.to_dict() for planet in planets])


# [GET] /planets/<int:planet_id> - Get one single planet's information
@api.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Session.query(Planet).get(planet_id)
    if planet:
        return jsonify(planet.to_dict())
    return jsonify({"error": "Planet not found"}), 404


# [GET] /users - Get a list of all the blog post users
@api.route('/users', methods=['GET'])
def get_users():
    users = Session.query(User).all()
    return jsonify([user.to_dict() for user in users])


# [GET] /users/favorites - Get all the favorites that belong to the current user
@api.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id')  # Assuming user_id is passed as a query parameter
    favorites = Session.query(Favorite).filter_by(user_id=user_id).all()
    return jsonify([favorite.to_dict() for favorite in favorites])


# [POST] /favorite/planet/<int:planet_id> - Add a new favorite planet
@api.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.json.get('user_id')  # Assuming user_id is passed in the request body
    new_favorite = Favorite(user_id=user_id, planet_id=planet_id)
    Session.add(new_favorite)
    Session.commit()
    return jsonify(new_favorite.to_dict()), 201


# [POST] /favorite/people/<int:people_id> - Add new favorite people
@api.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    user_id = request.json.get('user_id')  # Assuming user_id is passed in the request body
    new_favorite = Favorite(user_id=user_id, character_id=people_id)
    Session.add(new_favorite)
    Session.commit()
    return jsonify(new_favorite.to_dict()), 201


# [DELETE] /favorite/planet/<int:planet_id> - Delete a favorite planet
@api.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.json.get('user_id')  # Assuming user_id is passed in the request body
    favorite = Session.query(Favorite).filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite:
        Session.delete(favorite)
        Session.commit()
        return jsonify({"message": "Favorite planet deleted"}), 200
    return jsonify({"error": "Favorite planet not found"}), 404


# [DELETE] /favorite/people/<int:people_id> - Delete a favorite person
@api.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_person(people_id):
    user_id = request.json.get('user_id')  # Assuming user_id is passed in the request body
    favorite = Session.query(Favorite).filter_by(user_id=user_id, character_id=people_id).first()
    if favorite:
        Session.delete(favorite)
        Session.commit()
        return jsonify({"message": "Favorite person deleted"}), 200
    return jsonify({"error": "Favorite person not found"}), 404
