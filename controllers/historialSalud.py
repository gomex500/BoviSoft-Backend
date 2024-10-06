from flask import request, jsonify
from datetime import datetime
from bson import ObjectId
from models.historialSalud import HistorialSalud
import json

def crear_historial(collections):
    # Crear una nueva entrada de HistorialSalud
    data = json.loads(request.data)
    
    data['create_at'] = datetime.now()
    data['update_at'] = datetime.now()
    
    result = collections.insert_one(data)
    return str(result.inserted_id)  # Devolver el ID del historial creado

def obtener_historial_por_id(collections, historial_id):
    # Obtener un historial por su ID
    historial = collections.find_one({"_id": ObjectId(historial_id)})
    if historial:
        historial["_id"] = str(historial["_id"])  # Convertir ObjectId a string
    return historial

def obtener_historiales_por_bovino(collections, bovino_id):
    # Obtener todos los historiales asociados a un bovino
    historiales = list(collections.find({"bovinoId": ObjectId(bovino_id)}))
    for historial in historiales:
        historial["_id"] = str(historial["_id"])  # Convertir ObjectId a string
    return historiales

def actualizar_historial(collections, historial_id, data):
    # Actualizar un historial por su ID
    data['update_at'] = datetime.now()  # Actualizar la fecha de modificación
    result = collections.update_one(
        {"_id": ObjectId(historial_id)},
        {"$set": data}
    )
    return result.modified_count > 0  # Devolver si la actualización tuvo éxito

def eliminar_historial(collections, historial_id):
    # Eliminar un historial por su ID
    result = collections.delete_one({"_id": ObjectId(historial_id)})
    return result.deleted_count > 0  # Devolver si la eliminación tuvo éxito