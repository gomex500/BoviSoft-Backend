from flask import request, jsonify
from datetime import datetime
from bson import ObjectId
from models.Finca import FincaModel
import json


#controlador insertar finca
def insertar_finca(collections):
    try:
        data = json.loads(request.data)
        finca_instance = FincaModel(data)
        id = collections.insert_one(finca_instance.__dict__).inserted_id
        return jsonify({'id':str(id)})
    except Exception as e:
        response = jsonify({"message": "Error de petición", "error": str(e)})
        response.status_code = 500
        return response

##obtener todas las fincas
def obtener_fincas(collections, idUsuario):
    try:
        fincas = []
        for doc in collections.find({"idUsuario": idUsuario}):
            finca = FincaModel(doc).__dict__
            finca['_id'] = str(doc['_id'])
            fincas.append(finca)
        return jsonify(fincas)
    except Exception as e:
        response = jsonify({"message": "Error de petición", "error": str(e)})
        response.status_code = 500
        return response


#controlador mostrar finca
def obtener_finca(collections, id):
    try:
        doc = collections.find_one({'_id': ObjectId(id)})
        finca_data = FincaModel(doc).__dict__
        finca_data['_id'] = str(doc['_id'])
        return jsonify(finca_data)
    except:
        response = jsonify({"menssage":"error de peticion"})
        response.status = 401
        return response


#controlador eliminar finca
def eliminar_finca(collections, id):
    try:
        collections.delete_one({'_id': ObjectId(id)})
        return jsonify({'mensaje': 'finca eliminada'})
    except:
        response = jsonify({"menssage":"Error al Eliminar"})
        response.status = 401
        return response

#controlador actualizar finca
def actualizar_finca(collections, id):
    try:
        finca_data = collections.find_one({'_id': ObjectId(id)})
        finca_data_update = FincaModel(request.json)

        #insertando datos sencibles
        finca_data_update.create_at = finca_data['create_at']
        finca_data_update.update_at = datetime.now()

        collections.update_one({'_id': ObjectId(id)}, {"$set": finca_data_update.__dict__})
        return jsonify({"message": "finca actualizada"})
    except:
        response = jsonify({"menssage":"error de peticion"})
        response.status = 401
        return response