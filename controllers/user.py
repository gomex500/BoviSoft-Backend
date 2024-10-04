from datetime import datetime
from urllib import response
from flask import request, jsonify
from bson import ObjectId
from models.user import UserModel
import json

##obtener todos los usuarios
def obtener_usuarios(collections):
    try:
        users = []
        for doc in collections.find():
            user = UserModel(doc).__dict__
            user['_id'] = str(doc['_id'])
            #evitar obtener la comtrasena de los usuarios
            user.pop('password', None)
            users.append(user)
        return jsonify(users)
    except Exception as e:
        response = jsonify({"mensaje":"Error de peticion", "error":str(e)})
        response.status_code = 500
        return response

#controlador mostrar un usuario
def obtener_usuario(collections, id):
    try:
        doc = collections.find_one({'_id': ObjectId(id)})
        user_data = UserModel(doc).__dict__
        user_data['_id'] = str(doc['_id'])
        return jsonify(user_data)
    except:
        response = jsonify({"menssage":"error de peticion"})
        response.status = 401
        return response