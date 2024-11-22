from datetime import datetime

##modelo de objeto Interacciones
class CommentInteractionModel:
    def __init__(self, data):
        self.idUsuario = data.get('idUsuario', '')
        self.idComment = data.get('idComment', '')
        self.tipo = data.get('tipo', '') ## EJ: "likes", "dislikes", "reports"
        self.fecha = data.get('fecha', '')
        self.estado = data.get('estado', False)
        self.create_at = data.get('create_at', datetime.now())
        self.update_at = data.get('update_at', datetime.now())