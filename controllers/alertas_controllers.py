from flask import request, jsonify
from datetime import datetime
from bson import ObjectId
from models.Alertas import AlertasModel
import json


#controlador insertar alerta
def insertar_alerta(collections):
    try:
        data = json.loads(request.data)
        alerta_instance = AlertasModel(data)
        id = collections.insert_one(alerta_instance.__dict__).inserted_id
        return jsonify({'id':str(id)})
    except Exception as e:
        response = jsonify({"message": "Error de petición", "error": str(e)})
        response.status_code = 500
        return response

##obtener todas los alerta por usuario
def obtener_alertas(collections, idUsuario):
    try:
        alertas = []
        for doc in collections.find({"idUsuario": idUsuario}):
            alerta = AlertasModel(doc).__dict__
            alerta['_id'] = str(doc['_id'])
            alertas.append(alerta)
        return jsonify(alerta)
    except Exception as e:
        response = jsonify({"message": "Error de petición", "error": str(e)})
        response.status_code = 500
        return response

#controlador mostrar alerta por id
def obtener_alerta(collections, id):
    try:
        doc = collections.find_one({'_id': ObjectId(id)})
        alerta_data = AlertasModel(doc).__dict__
        alerta_data['_id'] = str(doc['_id'])
        return jsonify(alerta_data)
    except:
        response = jsonify({"menssage":"error de peticion"})
        response.status = 401
        return response

#controlador eliminar alerta
def eliminar_alerta(collections, id):
    try:
        collections.delete_one({'_id': ObjectId(id)})
        return jsonify({'mensaje': 'alerta eliminada'})
    except:
        response = jsonify({"menssage":"Error al Eliminar"})
        response.status = 401
        return response

#controlador actualizar alerta
def actualizar_alerta(collections, id):
    try:
        alerta_data = collections.find_one({'_id': ObjectId(id)})
        alerta_data_update = AlertasModel(request.json)

        #insertando datos sencibles
        alerta_data_update.create_at = alerta_data['create_at']
        alerta_data_update.update_at = datetime.now()

        collections.update_one({'_id': ObjectId(id)}, {"$set": alerta_data_update.__dict__})
        return jsonify({"message": "alerta actualizada"})
    except:
        response = jsonify({"menssage":"error de peticion"})
        response.status = 401
        return response