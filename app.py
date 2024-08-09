from flask import Flask
from flask_cors import CORS
from configs.config import DEBUG, PORT
from routes.home import home

##inicializando servidor
app = Flask(__name__)


#habilitando cors
CORS(app)


#routes
app.register_blueprint(home)

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)