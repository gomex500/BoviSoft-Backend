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
        foros = []
        for doc in collectionsForo.find():
            foro = ForoModel(doc).__dict__
            foro['id'] = str(doc['_id'])
            
            iLikedItForo = collectionsPostInteraccion.find_one({"idForo": foro['id'], "idUsuario": user['id'], "tipoInteraccion": "likes"})
            iDidNotLikeForo = collectionsPostInteraccion.find_one({"idForo": foro['id'], "idUsuario": user['id'], "tipoInteraccion": "dislikes"})
            iReportedForo = collectionsPostInteraccion.find_one({"idForo": foro['id'], "idUsuario": user['id'], "tipoInteraccion": "reports"})
            
            foro["userInteractions"] = {
              "likes": iLikedItForo is not None,
              "dislikes": iDidNotLikeForo is not None,
              "reports": iReportedForo is not None
            }
            
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
      
      
def actualizar_Interaccion_post(collectionsForo, collectionsPostInteraccion):
    try:
        data = json.loads(request.data)
        post_interaccion_instance = PostInteractionModel(data)
        foro = collectionsForo.find_one({'_id': ObjectId(data['idForo'])})
        foro_model = ForoModel(foro)
        
        result_interaccion = collectionsPostInteraccion.find_one({'idUsuario': data['idUsuario'], 'idForo': data['idForo'], 'tipoInteraccion': data['tipoInteraccion']})
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
          return jsonify(data)
    except:
        response = jsonify({"menssage":"Error al actualizar Interacciones"})
        response.status = 401
        return response
