from flask import Blueprint, request, jsonify
from controllers.jwt import validar_token
from configs.conecction import collections
from controllers.informes_controller import (
    insertar_informe,
    obtener_informes,
    obtener_informe,
    eliminar_informe,
    actualizar_informe
)

#inicalizando ruta
informes_routes = Blueprint('informes_routes', __name__)

##validando token
@informes_routes.before_request
def verificar_token():
    try:
        token = request.headers['Authorization'].split(" ")[1]
        validar_token(token, output=False)
    except:
        return jsonify({"Mensaje":"Error de autenticacion, no estas autorizado"})

#ruta crear informe
@informes_routes.route('/informe', methods=['POST'])
def insertar_informe_ruta():
    return insertar_informe(collections('informes'))

#ruta mostrar informes por usuario
@informes_routes.route('/informes/<idUsuario>', methods=['GET'])
def obtener_informe_ruta(idUsuario):
    return obtener_informes(collections('informes'), idUsuario)

#ruta mostrar informe por id
@informes_routes.route('/informe/<id>', methods=['GET'])
def obtener_informe_id_ruta(id):
    return obtener_informe(collections('informes'), id)

#ruta eliminar informe
@informes_routes.route('/informe/<id>', methods=['DELETE'])
def eliminar_informe_ruta(id):
    return eliminar_informe(collections('informes'), id)

#ruta actualizar informe
@informes_routes.route('/informe/<id>', methods=['PUT'])
def actualizar_informe_ruta(id):
    return actualizar_informe(collections('informes'), id)