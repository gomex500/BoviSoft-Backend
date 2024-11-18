from flask import request, jsonify
from datetime import datetime
from bson import ObjectId
from models.Comentarios import ComentarioModel
import json

def insertar_comentario(collections):
    try:
        data = json.loads(request.data)
        comentario_instance = ComentarioModel(data)
        id = collections.insert_one(comentario_instance.__dict__).inserted_id
        return jsonify({'id':str(id)})
    except Exception as e:
        response = jsonify({"message": "Error de petición", "error": str(e)})
        response.status_code = 500
        return response
##obtener todas los comentarios de un foro
def obtener_comentarios_por_foro(collections, foro_id):
    try:
        comentarios = []
        for doc in collections.find({"foroId": ObjectId(foro_id)}):
            comentario = ComentarioModel(doc).__dict__
            comentario['_id'] = str(doc['_id'])
            comentarios.append(comentario)
        return jsonify(comentarios)
    except Exception as e:
        response = jsonify({"message": "Error de petición", "error": str(e)})
        response.status_code = 500
        return response

##obtener todas las comentarios
def obtener_comentarios(collections):
    try:
        comentarios = []
        for doc in collections.find():
            comentario = ComentarioModel(doc).__dict__
            comentario['_id'] = str(doc['_id'])
            comentarios.append(comentario)
        return jsonify(comentarios)
    except Exception as e:
        response = jsonify({"message": "Error de petición", "error": str(e)})
        response.status_code = 500
        return response


#controlador mostrar comentario
def obtener_comentario(collections, id):
    try:
        doc = collections.find_one({'_id': ObjectId(id)})
        comentario_data = ComentarioModel(doc).__dict__
        comentario_data['_id'] = str(doc['_id'])
        return jsonify(comentario_data)
    except:
        response = jsonify({"menssage":"error de peticion"})
        response.status = 401
        return response


#controlador eliminar comentario
def eliminar_comentario(collections, id):
    try:
        collections.delete_one({'_id': ObjectId(id)})
        return jsonify({'mensaje': 'comentario eliminado'})
    except:
        response = jsonify({"menssage":"Error al Eliminar"})
        response.status = 401
        return response

#controlador actualizar comentario
def actualizar_comentario(collections, id):
    try:
        comentario_data = collections.find_one({'_id': ObjectId(id)})
        comentario_data_update = ComentarioModel(request.json)

        #insertando datos sencibles
        comentario_data_update.create_at = comentario_data['create_at']
        comentario_data_update.update_at = datetime.now()

        collections.update_one({'_id': ObjectId(id)}, {"$set": comentario_data_update.__dict__})
        return jsonify({"message": "comentario actualizado"})
    except:
        response = jsonify({"menssage":"error de peticion"})
        response.status = 401
        return response