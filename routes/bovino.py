from flask import Blueprint, request, jsonify
from controllers.jwt import validar_token
from configs.conecction import collections
from controllers.bovino import (
    insertar_bovino,
    obtener_bovino,
    obtener_bovinosByFarm,
    obtener_bovinosByUser,
    eliminar_bovino,
    actualizar_bovino
)

#inicalizando ruta
bovino_routes = Blueprint('bovino_routes', __name__)

##validando token
@bovino_routes.before_request
def verificar_token():
    try:
        token = request.headers['Authorization'].split(" ")[1]
        validar_token(token, output=False)
    except:
        return jsonify({"Mensaje":"Error de autenticacion, no estas autorizado"})

#ruta crear bovino
@bovino_routes.route('/bovino', methods=['POST'])
def insertar_bovino_ruta():
    return insertar_bovino(collections('fincas'), collections('bovinos'))

#ruta mostrar bovino
@bovino_routes.route('/bovino/byUsers/<idUsuario>', methods=['GET'])
def obtener_bovino_por_usuario_ruta(idUsuario):
    return obtener_bovinosByUser(collections('fincas'), collections('bovinos'), idUsuario)
  
#ruta mostrar bovino
@bovino_routes.route('/bovino/byFarm/<fincaId>', methods=['GET'])
def obtener_bovino_por_finca_ruta(fincaId):
    return obtener_bovinosByFarm(collections('bovinos'), fincaId)

#ruta mostrar bovino
@bovino_routes.route('/bovino/<id>', methods=['GET'])
def obtener_bovino_id_ruta(id):
    return obtener_bovino(collections('bovinos'), id)

#ruta eliminar bovino
@bovino_routes.route('/bovino/<id>', methods=['DELETE'])
def eliminar_bovino_ruta(id):
    return eliminar_bovino(collections('bovinos'), id)

#ruta actualizar bovino
@bovino_routes.route('/bovino/<id>', methods=['PUT'])
def actualizar_bovino_ruta(id):
    return actualizar_bovino(collections('bovinos'), id)