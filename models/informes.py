from datetime import datetime

##modelo de objeto alertas
class InformesModel:
    def __init__(self, data):
        self.idUsuario = data.get('idUsuario', '')
        self.tipoInforme = data.get('tipoInforme', '')
        self.detalles = data.get('detalles', {})
        self.fechaGeneracion = data.get('fechaGeneracion', '')
        self.create_at = data.get('create_at', datetime.now())
        self.update_at = data.get('update_at', datetime.now())

#ejemplo de detalles
### "detalles": {
#      "idFinca": "ObjectId",
#      "idBovino": "ObjectId",
#      "observaciones": "string"
#    }