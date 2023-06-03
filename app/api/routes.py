from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Wine, wine_schema, wines_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/wines', methods = ['POST'])
@token_required
def create_wine(current_user_token):
    brand = request.json['brand']
    type= request.json['type']
    origin = request.json['origin']
    year = request.json['year']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    wine = Wine(brand, type, origin, year, user_token = user_token )

    db.session.add(wine)
    db.session.commit()

    response = wine_schema.dump(wine)
    return jsonify(response)

@api.route('/wines', methods = ['GET'])
@token_required
def get_wine(current_user_token):
    a_user = current_user_token.token
    wines = Wine.query.filter_by(user_token = a_user).all()
    response = wines_schema.dump(wines)
    return jsonify(response)


@api.route('/wines/<id>', methods = ['GET'])
@token_required
def get_single_wine(current_user_token, id):
    wine = Wine.query.get(id)
    response = wine_schema.dump(wine)
    return jsonify(response)

@api.route('/wines/<id>', methods = ['POST','PUT'])
@token_required
def update_wine(current_user_token,id):
    wine = Wine.query.get(id) 
    wine.brand = request.json['brand']
    wine.type = request.json['type']
    wine.origin = request.json['origin']
    wine.year = request.json['year']
    wine.user_token = current_user_token.token

    db.session.commit()
    response = wine_schema.dump(wine)
    return jsonify(response)

@api.route('/wines/<id>', methods = ['DELETE'])
@token_required
def delete_wine(current_user_token, id):
    wine = Wine.query.get(id)
    db.session.delete(wine)
    db.session.commit()
    response = wine_schema.dump(wine)
    return jsonify(response)