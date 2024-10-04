from datetime import datetime

##modelo de objeto comentarios
class ComentariosModel:
    def __init__(self, data):
        self.idUsuario = data.get('idUsuario', '')
        self.idPublicacion = data.get('idPublicacion', '')
        self.contenido = data.get('contenido', '')
        self.fechaCreacion = data.get('fechaCreacion', '')
        self.likes = data.get('likes', 0)
        self.create_at = data.get('create_at', datetime.now())
        self.update_at = data.get('update_at', datetime.now())


###"Interaciones": [
#        {
#            "idUsuario": "ObjectId", // Referencia al usuario que interactuó
#            "tipoInteraccion": "string", // Ej: "like", "dislike", "reportar"
#            "fecha": "Date"
#          }          
#    ]