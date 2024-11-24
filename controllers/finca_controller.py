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
      
def clasificar_ganado(fecha_nacimiento, genero: str) -> str:
    # Verificar si fecha_nacimiento es un string y convertirlo a datetime
    if isinstance(fecha_nacimiento, str):
        fecha_nacimiento_dt = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
    elif isinstance(fecha_nacimiento, datetime):
        fecha_nacimiento_dt = fecha_nacimiento
    else:
        raise ValueError("La fecha de nacimiento debe ser un string o un objeto datetime.")

    hoy = datetime.now()

    # Calcular la diferencia en meses
    edad_meses = (hoy.year - fecha_nacimiento_dt.year) * 12 + (hoy.month - fecha_nacimiento_dt.month)

    clasificacion = ''

    # Determinar si es ternero, vaquilla o novillo
    if edad_meses < 12:
        clasificacion = 'Ternero'
    elif genero.lower() == 'macho':
        if 12 <= edad_meses < 24:
            clasificacion = 'Novillo'
        else:
            clasificacion = 'Toro'
    elif genero.lower() == 'hembra':
        if 12 <= edad_meses < 24:
            clasificacion = 'Vaquilla'
        else:
            clasificacion = 'Vaca'

    return clasificacion

##obtener todas las fincas
def obtener_fincas(collections, idUsuario, colecctionsBovinos):
    try:
        fincas = []
        fincas_ids = []
        
        for doc in collections.find({"idUsuario": idUsuario}):
            finca = FincaModel(doc).__dict__
            finca['id'] = str(doc['_id'])
            finca['_id'] = str(doc['_id'])
            fincas_ids.append(doc['_id'])
            fincas.append(finca)
        
        bovinos = list(colecctionsBovinos.find({
            "fincaId": {"$in": fincas_ids},
        }))
        
        cantidadBovinosPorFinca = {}
        cantidadClasificacionGanadoPorFinca = {}
                
        for bovino in bovinos:
            fincaId = str(bovino['fincaId'])
            if fincaId not in cantidadBovinosPorFinca:
                cantidadBovinosPorFinca[fincaId] = 0
            cantidadBovinosPorFinca[fincaId] += 1
            if fincaId not in cantidadClasificacionGanadoPorFinca:
                cantidadClasificacionGanadoPorFinca[fincaId] = {}
            clasificacion = clasificar_ganado(bovino['fechaNacimiento'], bovino['genero'])
            if clasificacion not in cantidadClasificacionGanadoPorFinca[fincaId]:
                cantidadClasificacionGanadoPorFinca[fincaId][clasificacion] = 0
            cantidadClasificacionGanadoPorFinca[fincaId][clasificacion] += 1 if clasificacion else 0
        
        for finca in fincas:
            finca['cantidadBovinos'] = cantidadBovinosPorFinca.get(finca['id'], 0)
            finca['cantidadClasificacionGanado'] = {
                'ternero': cantidadClasificacionGanadoPorFinca.get(finca['id'], {}).get('Ternero', 0),
                'novillo': cantidadClasificacionGanadoPorFinca.get(finca['id'], {}).get('Novillo', 0),
                'toro': cantidadClasificacionGanadoPorFinca.get(finca['id'], {}).get('Toro', 0),
                'vaquilla': cantidadClasificacionGanadoPorFinca.get(finca['id'], {}).get('Vaquilla', 0),
                'vaca': cantidadClasificacionGanadoPorFinca.get(finca['id'], {}).get('Vaca', 0)
            }
        
        return jsonify(fincas)
    except Exception as e:
        response = jsonify({"message": "Error de petición", "error": str(e)})
        response.status_code = 500
        return response


#controlador mostrar finca
def obtener_finca(collections, id, colecctionsBovinos):
    try:
        doc = collections.find_one({'_id': ObjectId(id)})
        finca = FincaModel(doc).__dict__
        finca['_id'] = str(doc['_id'])
        finca['id'] = str(doc['_id'])
        
        bovinos = colecctionsBovinos.find({
            "fincaId":  ObjectId(id)
        })
        
        cantidadBovinosPorFinca = {}
        cantidadClasificacionGanadoPorFinca = {}
        
        for bovino in bovinos:
            fincaId = str(bovino['fincaId'])
            if fincaId not in cantidadBovinosPorFinca:
                cantidadBovinosPorFinca[fincaId] = 0
            cantidadBovinosPorFinca[fincaId] += 1
            if fincaId not in cantidadClasificacionGanadoPorFinca:
                cantidadClasificacionGanadoPorFinca[fincaId] = {}
            clasificacion = clasificar_ganado(bovino['fechaNacimiento'], bovino['genero'])
            if clasificacion not in cantidadClasificacionGanadoPorFinca[fincaId]:
                cantidadClasificacionGanadoPorFinca[fincaId][clasificacion] = 0
            cantidadClasificacionGanadoPorFinca[fincaId][clasificacion] += 1 if clasificacion else 0
            
            
        finca['cantidadBovinos'] = cantidadBovinosPorFinca.get(finca['id'], 0)
        finca['cantidadClasificacionGanado'] = {
            'ternero': cantidadClasificacionGanadoPorFinca.get(finca['id'], {}).get('Ternero', 0),
            'novillo': cantidadClasificacionGanadoPorFinca.get(finca['id'], {}).get('Novillo', 0),
            'toro': cantidadClasificacionGanadoPorFinca.get(finca['id'], {}).get('Toro', 0),
            'vaquilla': cantidadClasificacionGanadoPorFinca.get(finca['id'], {}).get('Vaquilla', 0),
            'vaca': cantidadClasificacionGanadoPorFinca.get(finca['id'], {}).get('Vaca', 0)
        }
        
        return jsonify(finca)
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