from flask import Blueprint, request, jsonify
from controllers.jwt import validar_token
from configs.conecction import collections
from controllers.alertas_controller import (
    insertar_alerta,
    obtener_alertas,
    obtener_alerta,
    eliminar_alerta,
    actualizar_alerta
)

#inicalizando ruta
alertas_routes = Blueprint('alertas_routes', __name__)

##validando token
@alertas_routes.before_request
def verificar_token():
    try:
        token = request.headers['Authorization'].split(" ")[1]
        validar_token(token, output=False)
    except:
        return jsonify({"Mensaje":"Error de autenticacion, no estas autorizado"})

#ruta crear alertas
@alertas_routes.route('/alerta', methods=['POST'])
def insertar_alertas_ruta():
    return insertar_alerta(collections('alertas'))

#ruta mostrar alertas por usuario
@alertas_routes.route('/alertas/<idUsuario>', methods=['GET'])
def obtener_alertas_ruta(idUsuario):
    return obtener_alertas(collections('alertas'), idUsuario)

#ruta mostrar alertas por id
@alertas_routes.route('/alerta/<id>', methods=['GET'])
def obtener_alertas_id_ruta(id):
    return obtener_alerta(collections('alertas'), id)

#ruta eliminar alertas
@alertas_routes.route('/alerta/<id>', methods=['DELETE'])
def eliminar_alertas_ruta(id):
    return eliminar_alerta(collections('alertas'), id)

#ruta actualizar alertas
@alertas_routes.route('/alerta/<id>', methods=['PUT'])
def actualizar_alertas_ruta(id):
    return actualizar_alerta(collections('alertas'), id)