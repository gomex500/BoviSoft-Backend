from datetime import datetime
from bson import ObjectId

class CalendarioCuidados:
    def __init__(self, bovinoId, fechaProgramada, actividad, descripcion=None, estado='Pendiente', costoEstimado=None):
        self.bovinoId = ObjectId(bovinoId)  # ID del bovino
        self.fechaProgramada = fechaProgramada
        self.actividad = actividad
        self.descripcion = descripcion
        self.estado = estado
        self.costoEstimado = costoEstimado
        self.fechaCreacion = datetime.now()  # Fecha de creación en UTC

    def to_dict(self):
        return {
            "_id": self._id,
            "bovinoId": self.bovinoId,
            "fechaProgramada": self.fechaProgramada,
            "actividad": self.actividad,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "costoEstimado": self.costoEstimado,
            "fechaCreacion": self.fechaCreacion
        }
#actividad ENUM('Vacunación', 'Desparasitación', 'Examen Médico', 'Parto', 'Monta', 'Otro') NOT NULL,
