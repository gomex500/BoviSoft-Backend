from datetime import datetime

##modelo de objeto alertas
class AlertasModel:
    def __init__(self, data):
        self.idUsuario = data.get('idUsuario', '')
        self.tipoAlerta = data.get('tipoAlerta', '') ##Ej: "vacunación", "enfermedad", "producción baja"
        self.mensaje = data.get('mensaje', '')
        self.idFinca = data.get('idFinca', '')
        self.idBovino = data.get('idBovino', '')
        self.fechaAlerta = data.get('fechaAlerta', '')
        self.leido = data.get('leido', '')
        self.create_at = data.get('create_at', datetime.now())
        self.update_at = data.get('update_at', datetime.now())