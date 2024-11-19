from flask import Flask
from flask_cors import CORS
from configs.config import DEBUG, PORT


from routes.home_route import home
from routes.login_route import login_routes
from routes.user_route import user_routes
from routes.finca_route import finca_routes
from routes.chatbot_route import chatbot_routes
from routes.alertas_route import alertas_routes
from routes.informes_route import informes_routes
from routes.bovino_route import bovino_routes
from routes.historialSalud import historialSalud_routes
from routes.tratamiento_route import tratamiento_routes
from routes.foro_routes import foro_routes
from routes.comentario_routes import comentario_routes
# from routes.ia_route import gemini_routes

##inicializando servidor
app = Flask(__name__)


#habilitando cors
CORS(app)


#routes
app.register_blueprint(home)
app.register_blueprint(login_routes)
app.register_blueprint(user_routes)
app.register_blueprint(finca_routes)
app.register_blueprint(chatbot_routes)
app.register_blueprint(alertas_routes)
app.register_blueprint(informes_routes)
app.register_blueprint(historialSalud_routes)
app.register_blueprint(bovino_routes)
app.register_blueprint(tratamiento_routes)
app.register_blueprint(foro_routes)
app.register_blueprint(comentario_routes)
# app.register_blueprint(gemini_routes)

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)