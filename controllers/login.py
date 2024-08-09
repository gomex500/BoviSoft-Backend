import json
import bcrypt
from flask import request, jsonify
from models.user import UserModel
from controllers.jwt import crear_token
import smtplib
from email.mime.text import MIMEText
import yagmail
from jinja2 import Template


#configuracion del correo
CORREO_REMITENTE = "bovinsoft@gmail.com"
PASSWORD_CORREO = "vsal gtkx dchi xyip"

# Función para enviar correo de verificación
def enviar_correo_verificacion(correo_destinatario, nombre):

    # Create a yagmail object
    yag = yagmail.SMTP(CORREO_REMITENTE, PASSWORD_CORREO)

    # Send the email
    yag.send(
        to=correo_destinatario,
        subject="Verificación de registro",
        contents=f"""\
<html>
  <body>
    <h1>Verificación de registro</h1>
    <p>Hola {nombre}, gracias por registrarte!</p>
    <img src='https://st2.depositphotos.com/1765488/5294/i/450/depositphotos_52940845-stock-photo-herd-of-cows-at-summer.jpg'/>
  </body>
</html>
""")

##funcion para validar si el correo existe
def validacion_gmail(coll, email):
    doc = coll.find_one({'email':email})
    if doc:
        return True
    return False

##valiar si el password existe
def validar_password(coll, password):
    passEncriptado = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    doc = coll.find_one({'password': passEncriptado})
    if doc:
        return True
    return False

##controlador para registro de usuarios
def signin(collections):
    try:
        data = json.loads(request.data)
        user_instace = UserModel(data)

        #verificar si el correo ya existe
        if validacion_gmail(collections, user_instace.email):
            response = jsonify({"message": "El correo electrónico ya está en uso"})
            response.status_code = 400
            return response

        #encriptando password
        password = user_instace.password.encode('utf-8')
        salt = bcrypt.gensalt()
        passEncriptado = bcrypt.hashpw(password, salt)
        user_instace.password = passEncriptado.decode('utf-8')

        #insertando password y usuario a la db
        id = collections.insert_one(user_instace.__dict__).inserted_id
        user_data = {
            "nombre": user_instace.nombre,
            "apellido": user_instace.apellido,
            "edad": user_instace.edad,
            "email": user_instace.email
        }
        token = crear_token(data=user_data)
        enviar_correo_verificacion(user_instace.email, user_instace.nombre)
        print(user_instace.email)
        return jsonify({'id':str(id), "token":token.decode('utf-8')})

    except:
        response = jsonify({"menssage","error de registro"})
        response.status = 400
        return response


#controllador de logeo de usuarios
def login(collections):
    try:
        data = json.loads(request.data)
        user_instance = UserModel(data)

        # Validar si el correo electrónico existe
        if not validacion_gmail(collections, user_instance.email):
            response = jsonify({"message": "El correo electrónico no existe"})
            response.status_code = 401
            return response

        # Obtener el documento del usuario
        user_doc = collections.find_one({'email': user_instance.email})
        user_data = {
            "nombre": user_doc['nombre'],
            "apellido": user_doc['apellido'],
            "edad": user_doc['edad'],
            "rol":user_instance.rol,
            "telefono": user_doc['telefono'],
            "email": user_doc['email'],
            "password": user_doc['password']
        }
        # Validar la contraseña
        if not bcrypt.checkpw(user_instance.password.encode('utf-8'), user_doc['password'].encode('utf-8')):
            response = jsonify({"message": "La contraseña no es válida"})
            response.status_code = 401
            return response

        # Crear y enviar el token
        token = crear_token(data=user_data)
        return jsonify({'id': str(user_doc['_id']), "token": token.decode('utf-8')})
    except Exception as e:
        print(str(e))
        response = jsonify({"message": "Error de inicio de sesión"})
        response.status_code = 400
        return response