from fastapi import FastAPI, HTTPException #importar clase FastAPI
from database import User, Movie, UserReview
from database import database as connection
from schemas import UserRequestModel, UserResponseModel, ReviewRequestModel, ReviewResponseModel, MovieRequestModel, MovieResponseModel, ReviewRequestPutModel, ReviewRequestDeleteModel
from typing import List

#Ingresar a documentacion del servicio web con URL/docs

#Crear instancia de FastAPI
app = FastAPI(title = 'Proyecto para reseniar peliculas', #titulo de proyecto
              description = 'En este proyecto, seremos capaces de reseniar peliculas', #description for project
              version = '1' #versionar proyecto
              )


#Ejecutar cuando el server este por comenzar
@app.on_event('startup')
async def startup_event():
    if connection.is_closed():
        connection.connect()

    #Creacion de tablas. En caso de existir no pasa nada
    connection.create_tables([User, Movie, UserReview]) 


#Ejecutar cuando el server este por finalizar
@app.on_event('shutdown')
def shutdown_event():
    if not connection.is_closed():
        connection.close()


#La funcion encargada de retornar respuesta
#Si hay multiples funciones, se completen de forma asincrona con 'async'
@app.get('/')
async def index():
    return 'Hola mundo, desde un server en FastAPI'


@app.get('/about')
async def about():
    return app.description

#indicar tipo de respuesta = objeto serializado
@app.post('/users', response_model = UserResponseModel)
async def create_user(user: UserRequestModel): #indicamos clase de tipo BaseModel, correctos datos de entrada

    #Verificar con consulta, si el username ya existe sin que el server deje de funcionar
    if User.select().where(User.username == user.username).exists():
        #notificar error
        raise HTTPException(409, 'El username ya se encuentra en uso.')

    #utilizar metodo de clase sin uso de objeto
    hash_password = User.create_password(user.password)

    user = User.create(
        username = user.username,
        #asignar la contrasenia hash al atributo creado
        password = hash_password
    )

    #Serializar objeto para ser enviado como respuesta del server. Se convierte a un diccionario


    #retornar Modelo, que nos permite validar datos de entrada y de salida
    return user

@app.post('/reviews', response_model = ReviewResponseModel)
async def create_reviews(user_reviews : ReviewRequestModel):
    
    #Validar llaves foraneas
    #Validar id de usuario exista
    if User.select().where(User.id == user_reviews.user_id).first() is None:
        raise HTTPException(status_code = 404, detail = 'User not found')

    #Validar que el id de pelicula exista
    if Movie.select().where(Movie.id == user_reviews.movie_id).first() is None:
        raise HTTPException(status_code = 404, detail = 'Movie not found')

    #Crear a partir de los datos que envie el cliente
    user_reviews = UserReview.create(
        user_id = user_reviews.user_id,
        movie_id = user_reviews.movie_id,
        reviews = user_reviews.reviews,
        score = user_reviews.score
    )

    return user_reviews

@app.post('/movies', response_model = MovieResponseModel)
async def create_movies(movie : MovieRequestModel):

    if Movie.select().where(Movie.title == movie.title).exists():
        #notificar error
        raise HTTPException(409, 'La pelicula ya se encuentra en la BD.')
    
    movie = Movie.create(
        title = movie.title
    )

    return movie

#Obtener listado de resenias #TODAS
#Indicamos retornar listado de objetos tipo reviewresponseModel
# @app.get('/reviews', response_model = List[ReviewResponseModel])
# async def get_reviews():
#     reviews = UserReview.select().paginate(page, limit) #SELECT * FROM user_reviews

#     #generar lista de objetos user_review
#     return [user_reviews for user_reviews in reviews]

#24/02/2024 JAR
#Obtener listado de X cantidad de resenias
@app.get('/reviews', response_model = List[ReviewResponseModel])
async def get_reviews(page : int = 1, limit : int = 10 ):
    #Paginar consulta, retorna bloques de registros.
    #QuerySET, es opcional. Se encuentran despues del "?"
    #Recibe a pag actual, cantidad de elementos
    reviews = UserReview.select().paginate(page, limit) #SELECT * FROM user_reviews

    #generar lista de objetos user_review
    return [user_reviews for user_reviews in reviews]

#Obtener una resenia en particular. Crear endpoint que permita obtener y mostrar resenia en particular
#Parametros que el cliente envia al server mediante url, en API REST, parametros denotar recurso en particular
#Cliente puede enviar ID de X resenia, consulta, retornar resenia
#Ruta con parametro obligatorio
@app.get('/reviews/{review_id}', response_model = ReviewResponseModel)
async def get_review(review_id : int):
    
    #Realizar peticion
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(status_code = 404, detail = 'Review not found')
    
    return user_review

#Actualizar resenia, con respecto a valores que se envian
#Valores deben de enviarse a traves el cuerpo de la peticion. que son el segundo parametro de la funcion async
@app.put('/reviews/{review_id}', response_model = ReviewResponseModel)
#En segundo parametro, vienen los datos enviados
async def update_review(review_id : int, review_request: ReviewRequestPutModel ):

    #Obtener resenia a actualizar
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(status_code = 404, detail = 'Review not found')
    
    user_review.reviews = review_request.reviews
    user_review.score = review_request.score

    user_review.save()

    return user_review
    
@app.delete('/reviews/{review_id}', response_model = ReviewRequestDeleteModel)
async def delete_review(review_id : int) :
    
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(status_code = 404, detail = 'Review not found')
    

    user_review.delete_instance()

    return user_review