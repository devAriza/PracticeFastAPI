#Realizar peticiones a servidor
import requests

#2. envio de parametros
#URL = 'http://127.0.0.1:8000/api/v1/reviews?page=1&limit=2'

URL = 'http://127.0.0.1:8000/api/v1/reviews'
#Encabezados de peticion
HEADERS = {'accept' : 'application/json'}
#1. QuerySET
QUERYSET = { 'page' : 1, 'limit' : 2 }

#Enviar peticion a servidor
#response = requests.get(URL)

#Enviar encabezados en peticion
#response = requests.get(URL, headers = HEADERS)

#Enviar encabezados y parametros en peticion
response = requests.get(URL, headers = HEADERS, params = QUERYSET)

#Envio de parametros. Utilizando requests 1. Con QuerySET 2. Alterando URL 

if response.status_code == 200:
    print("Peticion realizada de forma exitosa")

    # #Arreglo de bites con contenido de la respuesta
    # print(response.content)
    # print('\n')
    # #Imprimir encabezado
    # #Conocer encabezados que se encuentran en respuesta de servidor
    # print(response.headers)

    #Convertir respuesta a JSON = diccionario
    # if response.headers.get('content-type') == 'application/json':
    #     print(
    #         response.json()
    #     )
    #Dar por seguro que el servidor esta retornando un JSON
    if response.headers.get('content-type') == 'application/json':
        reviews = response.json() #Coleccion Lista o Diccionario
        for review in reviews:
            #Accede a la llave score y a la llave reviews del objeto JSON
            print(f"score: {review['score']} - {review['reviews']}")
