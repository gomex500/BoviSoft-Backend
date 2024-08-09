from flask import Flask
from flask_cors import CORS
from configs.config import DEBUG, PORT
from routes.home import home
from routes.login import login_routes

##inicializando servidor
app = Flask(__name__)


#habilitando cors
CORS(app)


#routes
app.register_blueprint(home)
app.register_blueprint(login_routes)

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)