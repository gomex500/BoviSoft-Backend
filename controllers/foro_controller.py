from flask import request, jsonify, g
from datetime import datetime
from bson import ObjectId
from models.Foro import ForoModel
from models.Comentarios import ComentariosModel
from models.PostInteraction import PostInteractionModel
from models.CommentInteraction import CommentInteractionModel
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
def obtener_foros(collectionsForo, collectionsPostInteraccion):
    try:
        user = g.current_user
        if not user or '_id' not in user:
            return jsonify({"message": "Usuario no autenticado"}), 401

        foros = []
        foro_ids = []

        # Obtener todos los foros y sus IDs
        for doc in collectionsForo.find():
            foro = ForoModel(doc).__dict__
            foro['id'] = str(doc['_id'])
            foro_ids.append(foro['id'])
            foros.append(foro)

        # Obtener todas las interacciones relevantes para este usuario y estos foros
        interacciones = list(collectionsPostInteraccion.find({
            "idForo": {"$in": foro_ids},
            "idUsuario": user['_id']
        }))

        # Mapear interacciones por tipo e ID de foro
        interacciones_por_foro = {}
        for interaccion in interacciones:
            foro_id = interaccion["idForo"]
            if foro_id not in interacciones_por_foro:
                interacciones_por_foro[foro_id] = {}
            interacciones_por_foro[foro_id][interaccion["tipoInteraccion"]] = True

        # Añadir las interacciones del usuario a cada foro
        for foro in foros:
            interacciones_usuario = interacciones_por_foro.get(foro['id'], {})
            foro["userInteractions"] = {
                "likes": interacciones_usuario.get("likes", False),
                "dislikes": interacciones_usuario.get("dislikes", False),
                "reports": interacciones_usuario.get("reports", False)
            }

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
        response.status = 500
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
      
      
def actualizar_interaccion_post(collectionsForo, collectionsPostInteraccion):
    try:
        data = request.get_json()

        post_interaccion_instance = PostInteractionModel(data)
        post_interaccion_dict = post_interaccion_instance.__dict__

        foro = collectionsForo.find_one({'_id': ObjectId(data['idForo'])})
        if not foro:
            return jsonify({"message": "Foro no encontrado"}), 404

        foro_model = ForoModel(foro)

        id_usuario = post_interaccion_dict['idUsuario']
        id_foro = post_interaccion_dict['idForo']
        tipo_interaccion = post_interaccion_dict['tipoInteraccion']

        result_interaccion = collectionsPostInteraccion.find_one({
            'idUsuario': id_usuario,
            'idForo': id_foro,
            'tipoInteraccion': tipo_interaccion
        })

        if result_interaccion is None:
            # Insert new interaction
            inserted_id = collectionsPostInteraccion.insert_one(post_interaccion_dict).inserted_id
            foro_model.interacciones[tipo_interaccion] += 1
            collectionsForo.update_one({'_id': ObjectId(id_foro)}, {"$set": foro_model.__dict__})
            return jsonify({'id': str(inserted_id)})
        else:
            # Update existing interaction
            estado = post_interaccion_instance.estado
            foro_model.interacciones[tipo_interaccion] += 1 if estado else -1
            collectionsPostInteraccion.update_one({
                'idUsuario': id_usuario,
                'idForo': id_foro,
                'tipoInteraccion': tipo_interaccion
            }, {"$set": post_interaccion_dict})
            collectionsForo.update_one({'_id': ObjectId(id_foro)}, {"$set": foro_model.__dict__})
            return jsonify({'estado': True})

    except Exception as e:
        response = jsonify({"message": "Error al actualizar interacciones", "error": str(e)})
        response.status_code = 500
        return response