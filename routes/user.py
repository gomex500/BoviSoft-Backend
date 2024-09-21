from flask import Blueprint, request, jsonify
from controllers.jwt import validar_token
from configs.conecction import collections
from controllers.user import (
    obtener_usuarios
)

#inicalizando ruta
user_routes = Blueprint('user_routes', __name__)

##validando token
@user_routes.before_request
def verificar_token():
    try:
        token = request.headers['Authorization'].split(" ")[1]
        validar_token(token, output=False)
    except:
        return jsonify({"Mensaje":"Error de autenticacion, no estas autorizado"})

#ruta mostrar usuarios
@user_routes.route('/users', methods=['GET'])
def obtener_usuarios_ruta():
    return obtener_usuarios(collections('usuarios'))