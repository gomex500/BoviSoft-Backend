from datetime import datetime

##modelo de objeto usuario
class UserModel:
    def __init__(self, data):
        self.nombre = data.get('nombre', '')
        self.apellido = data.get('apellido', '')
        self.fecha_nacimiento = data.get('fecha_nacimiento', '')
        self.email = data.get('email', '')
        self.password = data.get('password', '')
        self.telefono = data.get('telefono', '')
        self.tipoSuscripcion = data.get('tipoSuscripcion', '') ## Ej: "básica", "premium"
        self.rol = data.get('rol', '') ## Ej: "admin", "ganadero"
        self.direccion = data.get('direccion', '')
        self.image = data.get('image', '')
        self.create_at = data.get('create_at', datetime.now())
        self.update_at = data.get('update_at', datetime.now())
        self.fincaId = data.get('fincaId', '')