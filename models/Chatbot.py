from datetime import datetime

##modelo de objeto Chabot
class ChatBotModel:
    def __init__(self, data):
        self.idUsuario = data.get('idUsuario', '')
        self.preguntaUsuario = data.get('preguntaUsuario', '')
        self.respuestaChatbot = data.get('respuestaChatbot', '')
        self.fecha = data.get('fecha', '')
        self.categoria = data.get('categoria', '')  
        self.create_at = data.get('create_at', datetime.now())
        self.update_at = data.get('update_at', datetime.now())