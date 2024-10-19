# from flask import request, jsonify
# import requests
# # from decouple import config

# # GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'
# # GEMINI_API_KEY = config('keyGeminis')

# def generar_contenido():
#     try:
#         # Obtener el input del usuario
#         data = request.get_json()
#         user_input = data.get('message')

#         if not user_input:
#             return jsonify({"error": "No se envió ningún mensaje"}), 400
        
#         # Preparar la solicitud a la API de Gemini
#         headers = {'Content-Type': 'application/json'}
#         payload = {
#             "contents": [{"parts": [{"text": user_input}]}]
#         }
        
#         response = requests.post(f"{GEMINI_API_URL}?key={GEMINI_API_KEY}", headers=headers, json=payload)
#         response.raise_for_status()  # Lanzar error si la respuesta no es exitosa

#         # Extraer la respuesta del contenido
#         gemini_response = response.json().get('contents', [{'parts': [{'text': 'No se pudo obtener una respuesta'}]}])[0]['parts'][0]['text']
#         return jsonify({"response": gemini_response})

#     except requests.exceptions.RequestException as e:
#         print(f"Error al comunicarse con la API de Gemini: {e}")
#         return jsonify({"error": "Error al comunicarse con el servicio de chatbot."}), 500

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
