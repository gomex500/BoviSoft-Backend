from flask import Blueprint, request, jsonify
from controllers.jwt import validar_token
from configs.conecction import collections
from controllers.user import (
    obtener_usuarios,
    obtener_usuario,
    obtener_email,
    eliminar_usuario,
    actualizar_usuario,
    actualizar_rol
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


#ruta eliminar usuario
@user_routes.route('/user/<id>', methods=['DELETE'])
def eliminar_usuario_ruta(id):
    return eliminar_usuario(collections('usuarios'), id)

#ruta actualizar usuario
@user_routes.route('/user/<id>', methods=['PUT'])
def actualizar_usuario_ruta(id):
    return actualizar_usuario(collections('usuarios'), id)

#ruta actualizar rol de usuario
@user_routes.route('/rol/<id>', methods=['PUT'])
def actualizar_rol_ruta(id):
    return actualizar_rol(collections('usuarios'), id)