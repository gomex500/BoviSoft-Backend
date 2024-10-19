from ctypes import cast
from distutils.debug import DEBUG
from email.policy import default
from decouple import config

##configurando variables de entorno
DEBUG = config('DEBUG', default=False, cast=bool)
PORT  = config('PORT', default=5000, cast=int)
MONGO_URI = config('MONGO_URI')
SECRET_KEY = config('SECRET_KEY')
# GEMINI_API_KEY = config('keyGeminis')
# GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'