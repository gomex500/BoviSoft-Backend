from flask import Blueprint, request, jsonify
from controllers.jwt import validar_token
from configs.conecction import collections
from controllers.historialSalud import (
  crear_historial,
  obtener_historial_por_id,
  obtener_historiales_por_bovino,
  actualizar_historial,
  eliminar_historial,
)

#inicalizando ruta
historialSalud_routes = Blueprint('historialSalud_routes', __name__)

##validando token
@historialSalud_routes.before_request
def verificar_token():
    try:
        token = request.headers['Authorization'].split(" ")[1]
        validar_token(token, output=False)
    except:
        return jsonify({"Mensaje":"Error de autenticacion, no estas autorizado"})

#ruta crear historialSalud
@historialSalud_routes.route('/historialSalud', methods=['POST'])
def insertar_finca_ruta():
    return crear_historial(collections('historialSalud'))

#ruta mostrar historialSalud
@historialSalud_routes.route('/historialSalud/<bovinoId>', methods=['GET'])
def obtener_historial_por_bovino_ruta(bovinoId):
    return obtener_historiales_por_bovino(collections('historialSalud'), bovinoId)

#ruta mostrar historialSalud
@historialSalud_routes.route('/historialSalud/<id>', methods=['GET'])
def obtener_historial_por_id_ruta(id):
    return obtener_historial_por_id(collections('historialSalud'), id)

#ruta eliminar historialSalud
@historialSalud_routes.route('/historialSalud/<id>', methods=['DELETE'])
def eliminar_historial_ruta(id):
    return eliminar_historial(collections('historialSalud'), id)

#ruta actualizar historialSalud
@historialSalud_routes.route('/historialSalud/<id>', methods=['PUT'])
def actualizar_historial_ruta(id):
    return actualizar_historial(collections('historialSalud'), id)