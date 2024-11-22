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

def obtener_comentarios_por_foro(collections, collectionsInteraccion, foro_id):
    try:
        user = g.current_user
        if not user or '_id' not in user:
            return jsonify({"message": "Usuario no autenticado"}), 401

        # Obtener todos los comentarios del foro
        comentariosGet = list(collections.find({"idForo": foro_id}))
        if not comentariosGet:
            return jsonify({"message": "No hay comentarios para este foro"}), 404

        # Extraer los IDs de comentarios para consultar interacciones de manera eficiente
        comentario_ids = [str(doc['_id']) for doc in comentariosGet]

        # Obtener todas las interacciones relevantes para este usuario y estos comentarios
        interacciones = list(collectionsInteraccion.find({
            "idComment": {"$in": comentario_ids},
            "idUsuario": user['_id']
        }))

        # Mapear interacciones por tipo e ID de comentario
        interacciones_por_comentario = {}
        for interaccion in interacciones:
            comment_id = interaccion["idComment"]
            if comment_id not in interacciones_por_comentario:
                interacciones_por_comentario[comment_id] = {}
            interacciones_por_comentario[comment_id][interaccion["tipo"]] = interaccion.get("estado", False)

        # Construir la respuesta de comentarios
        comentarios = []
        for doc in comentariosGet:
            comentario = ComentariosModel(doc).__dict__
            comentario['id'] = str(doc['_id'])

            # Obtener las interacciones del usuario actual con este comentario
            interacciones_usuario = interacciones_por_comentario.get(comentario['id'], {})

            comentario["userInteractions"] = {
                "likes": interacciones_usuario.get("likes", False),
                "dislikes": interacciones_usuario.get("dislikes", False),
                "reports": interacciones_usuario.get("reports", False)
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

def actualizar_interaccion_comentario(collectionsComentario, collectionsCommentInteraccion):
    try:
        # Cargar datos desde la solicitud
        data = json.loads(request.data)
        id_comment = data.get('idComment')
        id_usuario = data.get('idUsuario')
        tipo_interaccion = data.get('tipo')
        estado = data.get('estado')

        if not id_comment or not id_usuario or not tipo_interaccion or estado is None:
            return jsonify({"message": "Datos incompletos"}), 400

        # Consulta inicial: encontrar el comentario y la interacción en una sola pasada
        comment = collectionsComentario.find_one({"_id": ObjectId(id_comment)})
        if not comment:
            return jsonify({"message": "Comentario no encontrado"}), 404

        # Obtener el conteo actual de interacciones del tipo especificado
        interacciones = comment.get('interacciones', {})
        count_interaccion = interacciones.get(tipo_interaccion, 0)

        # Buscar o insertar la interacción
        result_interaccion = collectionsCommentInteraccion.find_one_and_update(
            {"idUsuario": id_usuario, "idComment": id_comment, "tipo": tipo_interaccion},
            {"$set": {"estado": estado}},
            upsert=True,
            return_document=True
        )

        # Calcular el nuevo conteo de interacciones
        if result_interaccion is None:  # Nueva interacción
            nuevo_conteo = count_interaccion + 1 if estado else count_interaccion
        else:  # Interacción existente
            estado_anterior = result_interaccion.get('estado', False)
            if estado_anterior != estado:  # Solo ajustar si el estado cambió
                nuevo_conteo = count_interaccion + 1 if estado else count_interaccion - 1
            else:
                nuevo_conteo = count_interaccion

        # Actualizar el comentario con el nuevo conteo
        collectionsComentario.update_one(
            {"_id": ObjectId(id_comment)},
            {"$set": {f"interacciones.{tipo_interaccion}": nuevo_conteo}}
        )

        return jsonify({"message": "Interacción actualizada con éxito", "idComment": id_comment}), 200

    except Exception as e:
        response = jsonify({"message": "Error al actualizar interacciones", "error": str(e)})
        response.status_code = 500
        return response