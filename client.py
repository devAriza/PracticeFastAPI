#Realizar peticiones a servidor
import requests

URL = 'http://127.0.0.1:8000/api/v1/reviews'

response = requests.get(URL)

if response.status_code == 200:
    print("Peticion realizada de forma exitosa")

    #Arreglo de bites con contenido de la respuesta
    print(response.content)