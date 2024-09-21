from datetime import datetime

##modelo de objeto Bovino
class BovinoModel:
    def __init__(self, data):
        self.nombre = data.get('nombre', '')
        self.create_at = data.get('create_at', datetime.now())
        self.update_at = data.get('update_at', datetime.now())