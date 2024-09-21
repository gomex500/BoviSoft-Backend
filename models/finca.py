from datetime import datetime

##modelo de objeto Finca
class FincaModel:
    def __init__(self, data):
        self.nombre = data.get('nombre', '')
        self.direccion = data.get('direccion', '')
        self.ubicacion = data.get('ubicacion', '')
        self.cantidadReses = data.get('cantidadReses', '')
        self.medida = data.get('medida', '')
        self.recursosN = data.get('recursosN', '')
        self.create_at = data.get('create_at', datetime.now())
        self.update_at = data.get('update_at', datetime.now())