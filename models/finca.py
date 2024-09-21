from datetime import datetime

##modelo de objeto Finca
class FincaModel:
    def __init__(self, data):
        self.nombre = data.get('nombre', '')
        self.image = data.get('image', '')
        self.direccion = data.get('direccion', '')
        self.coordenadas = data.get('coordenadas', {})
        self.tamano = data.get('tamano', '')
        self.recursosN = data.get('recursosN', [])
        self.descripcion = data.get('descripcion', '')
        self.idUsuario = data.get('idUsuario', '')
        self.create_at = data.get('create_at', datetime.now())
        self.update_at = data.get('update_at', datetime.now())