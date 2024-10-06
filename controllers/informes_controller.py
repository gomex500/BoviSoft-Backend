from flask import request, jsonify
from datetime import datetime
from bson import ObjectId
from models.Informes import InformesModel
import json


#controlador insertar informe
def insertar_informe(collections):
    try:
        data = json.loads(request.data)
        informe_instance = InformesModel(data)
        id = collections.insert_one(informe_instance.__dict__).inserted_id
        return jsonify({'id':str(id)})
    except Exception as e:
        response = jsonify({"message": "Error de petición", "error": str(e)})
        response.status_code = 500
        return response

##obtener todas los informe por usuario
def obtener_informes(collections, idUsuario):
    try:
        informes = []
        for doc in collections.find({"idUsuario": idUsuario}):
            informe = InformesModel(doc).__dict__
            informe['_id'] = str(doc['_id'])
            informes.append(informe)
        return jsonify(informes)
    except Exception as e:
        response = jsonify({"message": "Error de petición", "error": str(e)})
        response.status_code = 500
        return response

#controlador mostrar informe por id
def obtener_informe(collections, id):
    try:
        doc = collections.find_one({'_id': ObjectId(id)})
        informe_data = InformesModel(doc).__dict__
        informe_data['_id'] = str(doc['_id'])
        return jsonify(informe_data)
    except:
        response = jsonify({"menssage":"error de peticion"})
        response.status = 401
        return response

#controlador eliminar informe
def eliminar_informe(collections, id):
    try:
        collections.delete_one({'_id': ObjectId(id)})
        return jsonify({'mensaje': 'informe eliminado'})
    except:
        response = jsonify({"menssage":"Error al Eliminar"})
        response.status = 401
        return response

#controlador actualizar informe
def actualizar_informe(collections, id):
    try:
        informe_data = collections.find_one({'_id': ObjectId(id)})
        informe_data_update = InformesModel(request.json)

        #insertando datos sencibles
        informe_data_update.create_at = informe_data['create_at']
        informe_data_update.update_at = datetime.now()

        collections.update_one({'_id': ObjectId(id)}, {"$set": informe_data_update.__dict__})
        return jsonify({"message": "informe actualizado"})
    except:
        response = jsonify({"menssage":"error de peticion"})
        response.status = 401
        return response