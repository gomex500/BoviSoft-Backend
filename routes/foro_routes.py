from flask import Blueprint, request, jsonify, g
from controllers.jwt import validar_token
from configs.conecction import collections
from controllers.foro_controller import (
    insertar_foro,
    obtener_foros,
    obtener_foro,
    actualizar_foro,
    eliminar_foro,
    actualizar_Interaccion_post
)

#inicalizando ruta
foro_routes = Blueprint('foro_routes', __name__)

##validando token
# @foro_routes.before_request
# def verificar_token():
#     try:
#         token = request.headers['Authorization'].split(" ")[1]
#         payload = validar_token(token, output=True)
#         g.current_user = payload
#     except:
#         return jsonify({"Mensaje":"Error de autenticacion, no estas autorizado"})

#ruta crear foro
@foro_routes.route('/foro', methods=['POST'])
def insertar_foro_ruta():
    return insertar_foro(collections('foros'))

#ruta mostrar foros
@foro_routes.route('/foros', methods=['GET'])
def obtener_foros_ruta():
    token = request.headers['Authorization'].split(" ")[1]
    payload = validar_token(token, output=True)
    g.current_user = payload
    return obtener_foros(collections('foros'), collections('interaccionesPost'))

#ruta mostrar foro por id
@foro_routes.route('/foro/<id>', methods=['GET'])
def obtener_foro_ruta(id):
    return obtener_foro(collections('foros'), id)

#ruta actualizar foro
@foro_routes.route('/foro/<id>', methods=['PUT'])
def actualizar_foro_ruta(id):
    return actualizar_foro(collections('foros'), id)

#ruta eliminar foro
@foro_routes.route('/foro/<id>', methods=['DELETE'])
def eliminar_foro_ruta(id):
    return eliminar_foro(collections('foros'), id) 
  
@foro_routes.route('/interacciones/publicaciones', methods=['POST'])
def actualizar_interaccion_post_ruta():
    print("@actualizar_interaccion_post_ruta")
    return actualizar_Interaccion_post(collections('foros'), collections('interaccionesPost'))
