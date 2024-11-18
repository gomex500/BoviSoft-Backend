from datetime import datetime
from bson import ObjectId

class HistorialSanitario:
    def __init__(self, bovinoId, fechaRealizada, actividad, productoUsado=None, dosis=None, veterinario=None, observaciones=None, costoReal=None):
        self._id = ObjectId()  # MongoDB genera un ID único automáticamente
        self.bovinoId = ObjectId(bovinoId)  # ID del bovino
        self.fechaRealizada = fechaRealizada
        self.actividad = actividad
        self.productoUsado = productoUsado
        self.dosis = dosis
        self.veterinario = veterinario
        self.observaciones = observaciones
        self.costoReal = costoReal
        self.fechaCreacion = datetime.utcnow()  # Fecha de creación en UTC

    def to_dict(self):
        return {
            "_id": self._id,
            "bovinoId": self.bovinoId,
            "fechaRealizada": self.fechaRealizada,
            "actividad": self.actividad,
            "productoUsado": self.productoUsado,
            "dosis": self.dosis,
            "veterinario": self.veterinario,
            "observaciones": self.observaciones,
            "costoReal": self.costoReal,
            "fechaCreacion": self.fechaCreacion
        }
# actividad ENUM('Vacunación', 'Examen Médico', 'Otro') NOT NULL,