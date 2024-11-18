from flask import Blueprint, request, jsonify
from controllers.jwt import validar_token
from configs.conecction import collections
from controllers.foro_controller import (
    insertar_foro,
    obtener_foros,
    obtener_foro,
    actualizar_foro,
    eliminar_foro
)

#inicalizando ruta
foro_routes = Blueprint('foro_routes', __name__)

##validando token
@foro_routes.before_request
def verificar_token():
    try:
        token = request.headers['Authorization'].split(" ")[1]
        validar_token(token, output=False)
    except:
        return jsonify({"Mensaje":"Error de autenticacion, no estas autorizado"})

#ruta crear foro
@foro_routes.route('/foro', methods=['POST'])
def insertar_foro_ruta():
    return insertar_foro(collections('foro'))

#ruta mostrar foros
@foro_routes.route('/foros', methods=['GET'])
def obtener_foros_ruta():
    return obtener_foros(collections('foro'))

#ruta mostrar foro por id
@foro_routes.route('/foro/<id>', methods=['GET'])
def obtener_foro_ruta(id):
    return obtener_foro(collections('foro'), id)

#ruta actualizar foro
@foro_routes.route('/foro/<id>', methods=['PUT'])
def actualizar_foro_ruta(id):
    return actualizar_foro(collections('foro'), id)

#ruta eliminar foro
@foro_routes.route('/foro/<id>', methods=['DELETE'])
def eliminar_foro_ruta(id):
    return eliminar_foro(collections('foro'), id) 