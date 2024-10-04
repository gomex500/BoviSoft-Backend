from datetime import datetime
from bson import ObjectId 

##modelo de objeto Finca
class HistorialSalud:
    def __init__(self, data):
        self.bovinoId = ObjectId(data.get('bovinoId')) 
        self.evento = data.get('evento', '')
        self.descripcion = data.get('descripcion', '')
        self.fecha = data.get('fecha', datetime.now())
        self.nombreVeterinario = data.get('nombreVeterinario', '')
        self.observaciones = data.get('observaciones', '')
        self.create_at = data.get('create_at', datetime.now())
        self.update_at = data.get('update_at', datetime.now())