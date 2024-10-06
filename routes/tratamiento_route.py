from flask import Blueprint, request, jsonify
from controllers.jwt import validar_token
from configs.conecction import collections
from controllers.tratamientos_controller import (
    actualizar_tratamieto,
    insertar_chatbot_ruta,
    insertar_tratamiento,
    obtener_tratamientos,
    obtener_tratmiento,
    eliminar_tratamiento
)

#inicalizando ruta
taratmiento_routes = Blueprint('taratmiento_routes', __name__)

##validando token
@taratmiento_routes.before_request
def verificar_token():
    try:
        token = request.headers['Authorization'].split(" ")[1]
        validar_token(token, output=False)
    except:
        return jsonify({"Mensaje":"Error de autenticacion, no estas autorizado"})

#ruta crear tratmiento
@taratmiento_routes.route('/tratmiento', methods=['POST'])
def insertar_tratmiento_ruta():
    return insertar_tratamiento(collections('tratmiento'))

# #ruta mostrar tratmientos por usuario
# @taratmiento_routes.route('/tratmientos/<idUsuario>', methods=['GET'])
# def obtener_tratmiento_ruta(idUsuario):
#     return obtener_tratamientos(collections('tratmiento'), idUsuario)

#ruta mostrar tratmiento por id
@taratmiento_routes.route('/chat/<id>', methods=['GET'])
def obtener_tratmiento_id_ruta(id):
    return obtener_tratmiento(collections('tratmiento'), id)

#ruta eliminar tratmiento
@taratmiento_routes.route('/chat/<id>', methods=['DELETE'])
def eliminar_tratmiento_ruta(id):
    return eliminar_tratamiento(collections('tratmiento'), id)

#ruta actualizar tratmiento
@taratmiento_routes.route('/chat/<id>', methods=['PUT'])
def actualizar_tratmiento_ruta(id):
    return actualizar_tratamieto(collections('tratmiento'), id)