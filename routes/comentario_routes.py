from flask import Blueprint, request, jsonify
from controllers.jwt import validar_token
from configs.conecction import collections
from controllers.comentario_controller import (
    insertar_comentario,
    obtener_comentarios_por_foro,
    obtener_comentarios,
    obtener_comentario,
    eliminar_comentario,
    actualizar_comentario
)

#inicalizando ruta
comentario_routes = Blueprint('comentario_routes', __name__)

##validando token
@comentario_routes.before_request
def verificar_token():
    try:
        token = request.headers['Authorization'].split(" ")[1]
        validar_token(token, output=False)
    except:
        return jsonify({"Mensaje":"Error de autenticacion, no estas autorizado"})

#ruta crear comentario
@comentario_routes.route('/comentario', methods=['POST'])
def insertar_comentario_ruta():
    return insertar_comentario(collections('comentario'))

#ruta mostrar comentarios por foro
@comentario_routes.route('/comentarios/<foro_id>', methods=['GET'])
def obtener_comentarios_por_foro_ruta(foro_id):
    return obtener_comentarios_por_foro(collections('comentario'), foro_id)

#ruta mostrar comentarios
@comentario_routes.route('/comentarios', methods=['GET'])
def obtener_comentarios_ruta():
    return obtener_comentarios(collections('comentario'))

#ruta mostrar comentario por id
@comentario_routes.route('/comentario/<id>', methods=['GET'])
def obtener_comentario_ruta(id):
    return obtener_comentario(collections('comentario'), id)

#ruta eliminar comentario
@comentario_routes.route('/comentario/<id>', methods=['DELETE'])
def eliminar_comentario_ruta(id):
    return eliminar_comentario(collections('comentario'), id)

#ruta actualizar comentario
@comentario_routes.route('/comentario/<id>', methods=['PUT'])
def actualizar_comentario_ruta(id): 
    return actualizar_comentario(collections('comentario'), id) 