from flask import Blueprint, request

##inicializando ruta
home = Blueprint('home', __name__)

#ruta inical
@home.route('/')
def index():
    return "<h1>Welcome to BovinSotf ApiRest</h1>"