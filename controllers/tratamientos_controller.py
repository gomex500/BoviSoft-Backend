from flask import request, jsonify
from datetime import datetime
from bson import ObjectId
from models.Tratamientos import TratamientosModel
import json


#controlador insertar tratamiento
def insertar_tratamiento(collections):
    try:
        data = json.loads(request.data)
        tratamiento_instance = TratamientosModel(data)
        id = collections.insert_one(tratamiento_instance.__dict__).inserted_id
        return jsonify({'id':str(id)})
    except Exception as e:
        response = jsonify({"message": "Error de petición", "error": str(e)})
        response.status_code = 500
        return response

##obtener todas los tratamiento por usuario
def obtener_tratamientos(collections, idUsuario):
    try:
        tratamientos = []
        for doc in collections.find({"idUsuario": idUsuario}):
            tratamiento = TratamientosModel(doc).__dict__
            tratamiento['_id'] = str(doc['_id'])
            tratamientos.append(tratamiento)
        return jsonify(tratamientos)
    except Exception as e:
        response = jsonify({"message": "Error de petición", "error": str(e)})
        response.status_code = 500
        return response

#controlador mostrar tratamientos por id
def obtener_tratmiento(collections, id):
    try:
        doc = collections.find_one({'_id': ObjectId(id)})
        tratamiento_data = TratamientosModel(doc).__dict__
        tratamiento_data['_id'] = str(doc['_id'])
        return jsonify(tratamiento_data)
    except:
        response = jsonify({"menssage":"error de peticion"})
        response.status = 401
        return response

#controlador eliminar tratamiento
def eliminar_tratamiento(collections, id):
    try:
        collections.delete_one({'_id': ObjectId(id)})
        return jsonify({'mensaje': 'tratamiento eliminado'})
    except:
        response = jsonify({"menssage":"Error al Eliminar"})
        response.status = 401
        return response

#controlador actualizar tratamiento
def actualizar_tratamieto(collections, id):
    try:
        tratamiento_data = collections.find_one({'_id': ObjectId(id)})
        tratamiento_data_update = TratamientosModel(request.json)

        #insertando datos sencibles
        tratamiento_data_update.create_at = tratamiento_data['create_at']
        tratamiento_data_update.update_at = datetime.now()

        collections.update_one({'_id': ObjectId(id)}, {"$set": tratamiento_data_update.__dict__})
        return jsonify({"message": "tratatmiento actualizado"})
    except:
        response = jsonify({"menssage":"error de peticion"})
        response.status = 401
        return response