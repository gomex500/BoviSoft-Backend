from flask import Blueprint, request, jsonify
from controllers.jwt import validar_token
from configs.conecction import collections
from controllers.chatbot_controller import (
    insertar_chat,
    obtener_chat, 
    obtener_chats,
    eliminar_chat,
    actualizar_chat
)

#inicalizando ruta
chatbot_routes = Blueprint('chatbot_routes', __name__)

##validando token
@chatbot_routes.before_request
def verificar_token():
    try:
        token = request.headers['Authorization'].split(" ")[1]
        validar_token(token, output=False)
    except:
        return jsonify({"Mensaje":"Error de autenticacion, no estas autorizado"})

#ruta crear chat
@chatbot_routes.route('/chat', methods=['POST'])
def insertar_chatbot_ruta():
    return insertar_chat(collections('chatbot'))

#ruta mostrar chats por usuario
@chatbot_routes.route('/chats/<idUsuario>', methods=['GET'])
def obtener_chatbot_ruta(idUsuario):
    return obtener_chats(collections('chatbot'), idUsuario)

#ruta mostrar chat por id
@chatbot_routes.route('/chat/<id>', methods=['GET'])
def obtener_chatbot_id_ruta(id):
    return obtener_chat(collections('chatbot'), id)

#ruta eliminar chat
@chatbot_routes.route('/chat/<id>', methods=['DELETE'])
def eliminar_chatbot_ruta(id):
    return eliminar_chat(collections('chatbot'), id)

#ruta actualizar chat
@chatbot_routes.route('/chat/<id>', methods=['PUT'])
def actualizar_chatbot_ruta(id):
    return actualizar_chat(collections('chatbot'), id)