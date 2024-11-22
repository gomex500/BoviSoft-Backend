from datetime import datetime

##modelo de objeto Interacciones
class PostInteractionModel:
    def __init__(self, data):
        self.idUsuario = data.get('idUsuario', '')
        self.tipoInteraccion = data.get('tipoInteraccion', '') ## EJ: "likes", "dislikes", "reports"
        self.idForo = data.get('idForo', '')
        self.fecha = data.get('fecha', '')
        self.estado = data.get('estado', bool)
        self.create_at = data.get('create_at', datetime.now())
        self.update_at = data.get('update_at', datetime.now())