from fastapi import FastAPI #importar clase FastAPI

app = FastAPI(title = 'Proyecto para reseniar peliculas', #titulo de proyecto
              description = 'En este proyecto, seremos capaces de reseniar peliculas', #description for project
              version = '1' #versionar proyecto
              )

#La funcion encargada de retornar respuesta
#Si hay multiples funciones, se completen de forma asincrona
@app.get('/')
async def index():
    return 'Hola mundo, desde un server en FastAPI'