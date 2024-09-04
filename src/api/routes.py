"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity
import app 


api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/signup', methods=['POST'])
def Signup():
     data = request.json
     respuesta = app.Signup(data)

     print("respuesta desde app", respuesta)
     return jsonify(respuesta),200


@api.route('/login', methods=['POST'])
def Login1():
     data = request.json
     print("Data dentro de Login1",data)
     respuesta = app.Login(data)
     print(respuesta)
     return jsonify(respuesta),201


@api.route('/private', methods=['GET'])
@jwt_required()
def private():
    response = app.private()
    return jsonify(response), 200