from ctypes import cast
from email.policy import default
from decouple import config

##configurando variables de entorno
DEBUG = True  # O False, dependiendo de tu necesidad
PORT = 5000   # O el puerto que estés utilizando
MONGO_URI = config('MONGO_URI')
SECRET_KEY = config('SECRET_KEY')
# GEMINI_API_KEY = config('keyGeminis')
# GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'