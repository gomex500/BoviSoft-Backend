from flask import Blueprint, request, jsonify
from controllers.jwt import validar_token
from configs.conecction import collections
from controllers.user import (
    obtener_usuarios,
    obtener_usuario,
    obtener_email
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

#ruta mostrar usuario
@user_routes.route('/user/<id>', methods=['GET'])
def obtener_usuario_ruta(id):
    return obtener_usuario(collections('usuarios'), id)

#ruta mostrar usuario por el correo
@user_routes.route('/email/<email>', methods=['GET'])
def obtener_email_ruta(email):
    return obtener_email(collections('usuarios'), email)