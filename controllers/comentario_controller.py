from flask import request, jsonify, g
from datetime import datetime
from bson import ObjectId
from models.Comentarios import ComentariosModel
from models.CommentInteraction import CommentInteractionModel
import json

def insertar_comentario(collections):
    try:
        data = json.loads(request.data)
        comentario_instance = ComentariosModel(data)
        id = collections.insert_one(comentario_instance.__dict__).inserted_id
        return jsonify({'id':str(id)})
    except Exception as e:
        response = jsonify({"message": "Error de petición", "error": str(e)})
        response.status_code = 500
        return response
##obtener todas los comentarios de un foro
def obtener_comentarios_por_foro(collections,collectionsInteraccion, foro_id):
    try:
        user = g.current_user
        comentarios = []
        for doc in collections.find({"idForo": ObjectId(foro_id)}):
            comentario = ComentariosModel(doc).__dict__
            comentario['id'] = str(doc['_id'])
            
            iLikedItForo = collectionsInteraccion.find_one({"idComment": comentario['id'], "idUsuario": user['id'], "tipo": "likes"})
            iDidNotLikeForo = collectionsInteraccion.find_one({"idComment": comentario['id'], "idUsuario": user['id'], "tipo": "dislikes"})
            iReportedForo = collectionsInteraccion.find_one({"idComment": comentario['id'], "idUsuario": user['id'], "tipo": "reports"})
            
            comentario["userInteractions"] = {
              "likes": iLikedItForo is not None,
              "dislikes": iDidNotLikeForo is not None,
              "reports": iReportedForo is not None
            }
            
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
            comentario = ComentariosModel(doc).__dict__
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
        comentario_data = ComentariosModel(doc).__dict__
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
        comentario_data_update = ComentariosModel(request.json)

        #insertando datos sencibles
        comentario_data_update.create_at = comentario_data['create_at']
        comentario_data_update.update_at = datetime.now()

        collections.update_one({'_id': ObjectId(id)}, {"$set": comentario_data_update.__dict__})
        return jsonify({"message": "comentario actualizado"})
    except:
        response = jsonify({"menssage":"error de peticion"})
        response.status = 401
        return response

def actualizar_Interaccion_comentario(collectionsComentario, collectionsCommentInteraccion):
    try:
        data = json.loads(request.data)
        comment_interaccion_instance = CommentInteractionModel(data)
        comment = collectionsComentario.find_one({'_id': ObjectId(data['idComment'])})
        comment_model = ComentariosModel(comment)
        tipoInteraccion = comment_interaccion_instance.tipo
        countInteraccion = comment_model.interaciones[tipoInteraccion]
        
        result_interaccion = collectionsCommentInteraccion.find_one({'idUsuario': data['idUsuario'], 'idComment': data['idComment'], 'tipo': data['tipo']})
        
        if result_interaccion == None:
          id = collectionsCommentInteraccion.insert_one(comment_interaccion_instance.__dict__).inserted_id
          comment_model.interaciones[tipoInteraccion] = countInteraccion + 1
          collectionsComentario.update_one({'_id': ObjectId(data['idComment'])}, {"$set": comment_model.__dict__})
          return jsonify(str(id))
        else:
          estado = comment_interaccion_instance.estado
          
          comment_model.interaciones[tipoInteraccion] = countInteraccion + 1 if estado else countInteraccion - 1
          collectionsCommentInteraccion.update_one({"_id": ObjectId(result_interaccion['_id'])}, {"$set": comment_interaccion_instance.__dict__})
          collectionsComentario.update_one({'_id': ObjectId(data['idComment'])}, {"$set": comment_model.__dict__})
          
          return jsonify(str(result_interaccion['_id']))
    except:
        response = jsonify({"menssage":"Error al actualizar Interacciones"})
        response.status = 401
        return response