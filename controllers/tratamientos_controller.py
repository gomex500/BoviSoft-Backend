from flask import request, jsonify
from datetime import datetime
from bson import ObjectId
from models.Chatbot import ChatBotModel
import json


#controlador insertar chat
def insertar_chat(collections):
    try:
        data = json.loads(request.data)
        chat_instance = ChatBotModel(data)
        id = collections.insert_one(chat_instance.__dict__).inserted_id
        return jsonify({'id':str(id)})
    except Exception as e:
        response = jsonify({"message": "Error de petición", "error": str(e)})
        response.status_code = 500
        return response

##obtener todas los chat por usuario
def obtener_chats(collections, idUsuario):
    try:
        chats = []
        for doc in collections.find({"idUsuario": idUsuario}):
            chat = ChatBotModel(doc).__dict__
            chat['_id'] = str(doc['_id'])
            chats.append(chat)
        return jsonify(chats)
    except Exception as e:
        response = jsonify({"message": "Error de petición", "error": str(e)})
        response.status_code = 500
        return response

#controlador mostrar chat por id
def obtener_chat(collections, id):
    try:
        doc = collections.find_one({'_id': ObjectId(id)})
        chat_data = ChatBotModel(doc).__dict__
        chat_data['_id'] = str(doc['_id'])
        return jsonify(chat_data)
    except:
        response = jsonify({"menssage":"error de peticion"})
        response.status = 401
        return response

#controlador eliminar chat
def eliminar_chat(collections, id):
    try:
        collections.delete_one({'_id': ObjectId(id)})
        return jsonify({'mensaje': 'chat eliminado'})
    except:
        response = jsonify({"menssage":"Error al Eliminar"})
        response.status = 401
        return response

#controlador actualizar chat
def actualizar_chat(collections, id):
    try:
        chat_data = collections.find_one({'_id': ObjectId(id)})
        chat_data_update = ChatBotModel(request.json)

        #insertando datos sencibles
        chat_data_update.create_at = chat_data['create_at']
        chat_data_update.update_at = datetime.now()

        collections.update_one({'_id': ObjectId(id)}, {"$set": chat_data_update.__dict__})
        return jsonify({"message": "chat actualizada"})
    except:
        response = jsonify({"menssage":"error de peticion"})
        response.status = 401
        return response