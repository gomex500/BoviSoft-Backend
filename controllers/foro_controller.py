from flask import request, jsonify
from datetime import datetime
from bson import ObjectId
from models.Foro import ForoModel
import json

def insertar_foro(collections):
    try:
        data = json.loads(request.data)
        foro_instance = ForoModel(data)
        id = collections.insert_one(foro_instance.__dict__).inserted_id
        return jsonify({'id':str(id)})
    except Exception as e:
        response = jsonify({"message": "Error de petición", "error": str(e)})
        response.status_code = 500
        return response

##obtener todas las foros
def obtener_foros(collections):
    try:
        foros = []
        for doc in collections.find():
            foro = ForoModel(doc).__dict__
            foro['_id'] = str(doc['_id'])
            foros.append(foro)
        return jsonify(foros)
    except Exception as e:
        response = jsonify({"message": "Error de petición", "error": str(e)})
        response.status_code = 500
        return response


#controlador mostrar foro
def obtener_foro(collections, id):
    try:
        doc = collections.find_one({'_id': ObjectId(id)})
        foro_data = ForoModel(doc).__dict__
        foro_data['_id'] = str(doc['_id'])
        return jsonify(foro_data)
    except:
        response = jsonify({"menssage":"error de peticion"})
        response.status = 401
        return response

def actualizar_foro(collections, id):
    try:
        foro_data = collections.find_one({'_id': ObjectId(id)})
        foro_data_update = ForoModel(request.json)

        #insertando datos sencibles
        foro_data_update.create_at = foro_data['create_at']
        foro_data_update.update_at = datetime.now()

        collections.update_one({'_id': ObjectId(id)}, {"$set": foro_data_update.__dict__})
        return jsonify({"message": "foro actualizada"})
    except:
        response = jsonify({"menssage":"error de peticion"})
        response.status = 401
        return response
def eliminar_foro(collections, id):
    try:
        collections.delete_one({'_id': ObjectId(id)})
        return jsonify({'mensaje': 'foro eliminada'})
    except:
        response = jsonify({"menssage":"Error al Eliminar"})
        response.status = 401
        return response 