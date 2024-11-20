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
        if not user or 'id' not in user:
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
            "idUsuario": user['id']
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
      
      
def actualizar_Interaccion_post(collectionsForo, collectionsPostInteraccion):
    try:
        data = json.loads(request.data)
        
        post_interaccion_instance_dist = PostInteractionModel(data).__dict__
        post_interaccion_instance = PostInteractionModel(data)
        
        foro = collectionsForo.find_one({'_id': ObjectId(data['idForo'])})
        foro_model = ForoModel(foro)
        
        id_usuario = post_interaccion_instance_dist['idUsuario']
        id_foro = post_interaccion_instance_dist['idForo']
        tipo_interaccion = post_interaccion_instance_dist['tipoInteraccion']
        
        result_interaccion = collectionsPostInteraccion.find_one({'idUsuario': id_usuario, 'idForo': id_foro, 'tipoInteraccion': tipo_interaccion})

        if result_interaccion == None:
          id = collectionsPostInteraccion.insert_one(post_interaccion_instance.__dict__).inserted_id
          foro_model.interacciones[post_interaccion_instance.tipoInteraccion] = foro_model.interacciones[post_interaccion_instance.tipoInteraccion] + 1
          collectionsForo.update_one({'_id': ObjectId(data['idForo'])}, {"$set": foro_model.__dict__})
          return jsonify({'id': str(id)})
        else:
          estado = post_interaccion_instance.estado
          tipoInteraccion = post_interaccion_instance.tipoInteraccion
          foro_model.interacciones[tipoInteraccion] = foro_model.interacciones[tipoInteraccion] + 1 if estado else foro_model.interacciones[tipoInteraccion] - 1
          collectionsPostInteraccion.update_one({'idUsuario': data['idUsuario'], 'idForo': data['idForo']}, {"$set": post_interaccion_instance.__dict__})
          collectionsForo.update_one({'_id': ObjectId(data['idForo'])}, {"$set": foro_model.__dict__})
          return jsonify({'estado': True })
    except:
        response = jsonify({"menssage":"Error al actualizar Interacciones"})
        response.status = 500
        return response
