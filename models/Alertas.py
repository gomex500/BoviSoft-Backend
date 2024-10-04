from datetime import datetime

##modelo de objeto alertas
class AlertasModel:
    def __init__(self, data):
        self.idUsuario = data.get('idUsuario', '')
        self.tipoAlerta = data.get('tipoAlerta', '') ##Ej: "vacunación", "enfermedad", "producción baja"
        self.detalles = data.get('detalles', {})
        self.fechaAlerta = data.get('fechaAlerta', '')
        self.leido = data.get('leido', '')
        self.create_at = data.get('create_at', datetime.now())
        self.update_at = data.get('update_at', datetime.now())


#ejemplo de detalles
### "detalles": {
#      "idFinca": "ObjectId",
#      "idBovino": "ObjectId",
#      "mensaje": "string"
#    }