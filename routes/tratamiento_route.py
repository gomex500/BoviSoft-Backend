from flask import Blueprint, request, jsonify
from controllers.jwt import validar_token
from configs.conecction import collections
from controllers.tratamientos_controller import (
    actualizar_tratamieto,
    insertar_tratamiento,
    obtener_tratamientos,
    obtener_tratmiento,
    eliminar_tratamiento
)

#inicalizando ruta
tratamiento_routes = Blueprint('tratamiento_routes', __name__)

##validando token
@tratamiento_routes.before_request
def verificar_token():
    try:
        token = request.headers['Authorization'].split(" ")[1]
        validar_token(token, output=False)
    except:
        return jsonify({"Mensaje":"Error de autenticacion, no estas autorizado"})

#ruta crear tratmiento
@tratamiento_routes.route('/tratamiento', methods=['POST'])
def insertar_tratmiento_ruta():
    return insertar_tratamiento(collections('tratamiento'))

# #ruta mostrar tratmientos por usuario
# @tratamiento_routes.route('/tratmientos/<idUsuario>', methods=['GET'])
# def obtener_tratmiento_ruta(idUsuario):
#     return obtener_tratamientos(collections('tratamiento'), idUsuario)

#ruta mostrar tratmiento por id
@tratamiento_routes.route('/tratamiento/<id>', methods=['GET'])
def obtener_tratmiento_id_ruta(id):
    return obtener_tratmiento(collections('tratamiento'), id)

#ruta eliminar tratmiento
@tratamiento_routes.route('/tratamiento/<id>', methods=['DELETE'])
def eliminar_tratmiento_ruta(id):
    return eliminar_tratamiento(collections('tratamiento'), id)

#ruta actualizar tratmiento
@tratamiento_routes.route('/tratamiento/<id>', methods=['PUT'])
def actualizar_tratmiento_ruta(id):
    return actualizar_tratamieto(collections('tratamiento'), id)