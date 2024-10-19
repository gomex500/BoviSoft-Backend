from flask import Blueprint, request, jsonify
from controllers.jwt import validar_token
from controllers.ia_controller import generar_contenido

# Inicializando la ruta
gemini_routes = Blueprint('gemini_routes', __name__)

# Validando token
# @gemini_routes.before_request
# def verificar_token():
#     try:
#         token = request.headers['Authorization'].split(" ")[1]
#         validar_token(token, output=False)
#     except:
#         return jsonify({"Mensaje": "Error de autenticación, no estás autorizado"}), 401

# Ruta para generar contenido con Gemini
@gemini_routes.route('/ia', methods=['POST'])
def generar_contenido_ruta():
    return generar_contenido()
