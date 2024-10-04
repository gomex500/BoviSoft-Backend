from datetime import datetime

##modelo de objeto Tratamientos
class TratamientosModel:
    def __init__(self, data):
        self.nombre = data.get('nombre', '') ##Nombre de la vacuna o tratamiento
        self.tipo = data.get('tipo', '') ## Ej: "vacuna", "antibiótico", "suplemento"
        self.descripcion = data.get('descripcion', '')
        self.periodicidad = data.get('periodicidad', '') ## Ej: "anual", "mensual"
        self.dosis = data.get('dosis', '')
        self.fechaRegistro = data.get('fechaRegistro', '')
        self.create_at = data.get('create_at', datetime.now())
        self.update_at = data.get('update_at', datetime.now())