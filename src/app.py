"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from api.utils import APIException, generate_sitemap
from api.models import db, User
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash



# from models import Person

ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '../public/')
app = Flask(__name__)
app.url_map.strict_slashes = False

# database condiguration
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv("FLASK_APP_KEY", "super-secret") 
MIGRATE = Migrate(app, db, compare_type=True)
db.init_app(app)

# Configurar JWT
jwt = JWTManager(app)

# add the admin
setup_admin(app)

# add the admin
setup_commands(app)

# Add all endpoints form the API with a "api" prefix
app.register_blueprint(api, url_prefix='/api')

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, 'index.html')

# any other endpoint will try to serve it like a static file


@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0  # avoid cache memory
    return response


def Signup(data):
    print("valores recibidos de data",data)
    new_user = User()
    new_user.email = data.get("email")
    new_user.password = data.get("password")
    new_user.is_active = bool(data.get("is_active"))
    if new_user.email == "" or new_user.password == "" :
        response_body = {"message": "email and password are required"}
        return response_body
    else:
        user_result = db.session.execute(db.select(User).filter_by(email=new_user.email)).one_or_none()
        if user_result != None and user_result[0].email == new_user.email:
            response_body = {"message": "Usuario ya existe"}
            return response_body
        else:
            db.session.add(new_user)
            db.session.commit()
            response_body = {"message": "Usuario creado con Exito"}
            return response_body


def Login(data):
    new_user = User()
    print("Newuser dentro de Login",new_user.email)
    new_user.email = data.get("email")
    new_user.password = data.get("password")

    if new_user.email == "" or new_user.password == "" :
        response_body = {"message": "email and password are required"}
        return response_body
    else:
        user_result = db.session.execute(db.select(User).filter_by(email=data.get("email"))).one_or_none()
        user_result = user_result[0]
        passwd_is_ok = user_result.password == new_user.password
        if not passwd_is_ok:
            response_body = {"message": "Password incorrecto"}
            return response_body
        token = create_access_token(identity=user_result.id)
        response_body = {"token": token}
        return response_body

def private():
    current_user_id = get_jwt_identity()  
    user = User.query.get(current_user_id) 

    if user:
        return {
            "message": f"Welcome {user.email}, you are authenticated!",
            "email": user.email,
            "is_active": user.is_active
        }
    else:
        return {"message": "User not found"}, 404



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)
