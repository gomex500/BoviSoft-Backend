from crypt import methods
from flask import Blueprint
from configs.conecction import collections
from controllers.login import signin, login

##inicializando ruta login y registro
login_routes = Blueprint('login_routes', __name__)

##ruta de login
@login_routes.route('/login', methods=['POST'])
def login_route():
    return login(collections('usuarios'))

#ruta de resgistros de usuarios
@login_routes.route('/signin', methods=['POST'])
def signin_route():
    return signin(collections('usuarios'))