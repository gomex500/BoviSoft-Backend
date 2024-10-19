from flask import request, jsonify
from datetime import datetime
from bson import ObjectId
from models.bovino import BovinoModel
import json

def generar_abreviado_finca(nombre_finca):
    # Quitamos palabras comunes como 'Finca', 'De', 'El', 'La', etc.
    palabras_excluidas = {'de', 'el', 'la', 'los', 'las'}
    
    # Dividimos el nombre en palabras
    palabras = nombre_finca.lower().split()
    
    # Filtramos las palabras excluidas
    palabras_filtradas = [palabra for palabra in palabras if palabra not in palabras_excluidas]
    
    # Tomamos la primera letra de cada palabra restante y lo convertimos a mayúscula
    abreviado = ''.join([palabra[0].upper() for palabra in palabras_filtradas])
    
    return abreviado

#controlador insertar finca
def insertar_bovino(finca_collection, ganado_collection):
    try:
        data = json.loads(request.data)
        
        # Buscar la finca por id
        docFinca = finca_collection.find_one({'_id': ObjectId(data['fincaId'])})
        
        if not docFinca:
            return jsonify({"message": "Finca no encontrada"}), 404
        
        # Generar la abreviatura de la finca
        abreviado = generar_abreviado_finca(docFinca['nombre'])
        
        # Buscar el último bovino registrado en la finca
        ultimo_bovino = ganado_collection.find_one(
            {"fincaId": ObjectId(data['fincaId'])},  
            sort=[("consecutivo", -1)]  # Ordenar por el campo 'consecutivo' en orden descendente
        )

        # Obtener el nuevo consecutivo
        if ultimo_bovino:
            ultimo_consecutivo = ultimo_bovino["consecutivo"]
            nuevo_consecutivo = ultimo_consecutivo + 1
        else:
            nuevo_consecutivo = 1  # Si no hay bovinos, empezamos en 1
        
        # Generar el código consecutivo con el formato deseado
        codigo_bovino = f"{abreviado}-GND{str(nuevo_consecutivo).zfill(3)}"
        
        # Crear la instancia de BovinoModel y agregar el código y consecutivo
        bovino_instance = BovinoModel(data)
        bovino_instance.codigo = codigo_bovino
        bovino_instance.consecutivo = nuevo_consecutivo
        bovino_instance.fincaId = ObjectId(data['fincaId'])  # Asegúrate de que esté en formato ObjectId
        
        # Insertar el nuevo bovino en la colección de ganado
        id = ganado_collection.insert_one(bovino_instance.__dict__).inserted_id
        
        doc = ganado_collection.find_one({'_id': id})
        bovino_data = BovinoModel(doc).__dict__
        bovino_data['_id'] = str(doc['_id'])
        bovino_data['fincaId'] = str(doc['fincaId'])
        
        return jsonify(bovino_data), 201
    
    except Exception as e:
        response = jsonify({"message": "Error de petición", "error": str(e)})
        response.status_code = 500
        return response

##obtener todas los bovinos del usario
def obtener_bovinosByUser(finca_collection, ganado_collection, id_usuario):
    try:
        bovinos = []
        
        # Obtener todas las fincas del usuario
        fincas = finca_collection.find({"idUsuario": id_usuario})
        finca_ids = [doc_finca["_id"] for doc_finca in fincas]
        
        # Comprobar si se encontraron fincas
        if not finca_ids:
            return jsonify({"message": "No se encontraron fincas para el usuario."}), 404

        # Obtener todos los bovinos en las fincas del usuario
        bovinos_docs = ganado_collection.find({"fincaId": {"$in": finca_ids}})
        
        # Convertir el cursor a una lista para verificar la longitud
        bovinos_list = list(bovinos_docs)
        
        # Comprobar si se encontraron bovinos
        if not bovinos_list:
            return jsonify({"message": "No se encontraron bovinos para el usuario."}), 404
        
        for doc_ganado in bovinos_list:
            bovino = BovinoModel(doc_ganado).__dict__
            bovino['_id'] = str(doc_ganado['_id'])
            bovino['fincaId'] = str(doc_ganado['fincaId'])
            bovinos.append(bovino)

        return jsonify(bovinos), 200
        
    except Exception as e:
        response = jsonify({"message": "Error de petición", "error": str(e)})
        response.status_code = 500
        return response
      
##obtener todas los bovinos de la finca
def obtener_bovinosByFarm(collections, fincaId):
    try:
        bovinos = []
        for doc in collections.find({"fincaId": ObjectId(fincaId)}):
            bovino = BovinoModel(doc).__dict__
            bovino['_id'] = str(doc['_id'])
            bovino['fincaId'] = str(doc['fincaId'])
            bovinos.append(bovino)
        return jsonify(bovinos)
    except Exception as e:
        response = jsonify({"message": "Error de petición", "error": str(e)})
        response.status_code = 500
        return response


#controlador mostrar finca
def obtener_bovino(collections, id):
    try:
        doc = collections.find_one({'_id': ObjectId(id)})
        bovino_data = BovinoModel(doc).__dict__
        bovino_data['_id'] = str(doc['_id'])
        return jsonify(bovino_data)
    except:
        response = jsonify({"menssage":"error de peticion"})
        response.status = 401
        return response


#controlador eliminar finca
def eliminar_bovino(collections, id):
    try:
        collections.delete_one({'_id': ObjectId(id)})
        return jsonify({'mensaje': 'finca eliminada'})
    except:
        response = jsonify({"menssage":"Error al Eliminar"})
        response.status = 401
        return response

#controlador actualizar finca
def actualizar_bovino(collections, id):
    try:
        print("Iniciando actualización...")
        
        # Obtener el documento existente
        bovino_data = collections.find_one({'_id': ObjectId(id)})

        if bovino_data is None:
            return jsonify({"message": "Bovino no encontrado"}), 404

        # Obtener los nuevos datos a actualizar
        nuevos_datos = request.get_json()

        # Solo actualiza los campos que se pasaron en los nuevos datos
        update_data = {}
        if 'nombre' in nuevos_datos:
            update_data['nombre'] = nuevos_datos['nombre']
        if 'raza' in nuevos_datos:
            update_data['raza'] = nuevos_datos['raza']
        if 'edad' in nuevos_datos:
            update_data['edad'] = nuevos_datos['edad']
        if 'peso' in nuevos_datos:
            update_data['peso'] = nuevos_datos['peso']
        if 'fechaNacimiento' in nuevos_datos:
            update_data['fechaNacimiento'] = nuevos_datos['fechaNacimiento']
        if 'genero' in nuevos_datos:
            update_data['genero'] = nuevos_datos['genero']
        if 'tipo' in nuevos_datos:
            update_data['tipo'] = nuevos_datos['tipo']
        if 'estadoSalud' in nuevos_datos:
            update_data['estadoSalud'] = nuevos_datos['estadoSalud']
        if 'image' in nuevos_datos:
            update_data['image'] = nuevos_datos['image']
        # Siempre actualiza la fecha de modificación
        update_data['update_at'] = datetime.now()

        # Realizar la actualización solo si hay datos nuevos
        if update_data:
            collections.update_one({'_id': ObjectId(id)}, {"$set": update_data})

        return jsonify({"message": "Bovino actualizado con éxito"})

    except Exception as e:
        print(f"Error: {str(e)}")
        response = jsonify({"message": "Error de petición"})
        response.status_code = 500
        return response

