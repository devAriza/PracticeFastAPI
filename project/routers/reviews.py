from fastapi import HTTPException, APIRouter, Depends
from ..database import UserReview, Movie, User
from ..schemas import ReviewRequestDeleteModel, ReviewRequestPutModel, ReviewResponseModel, ReviewRequestModel
from ..common import get_current_user
from typing import List

router = APIRouter(prefix = '/reviews')

@router.post('', response_model = ReviewResponseModel)
async def create_reviews(user_reviews : ReviewRequestModel, user : User = Depends(get_current_user)):
    
    #Validar llaves foraneas
    #Validar id de usuario exista
    #Validacion sin autenticacion OAuth2
    '''if User.select().where(User.id == user_reviews.user_id).first() is None:
        raise HTTPException(status_code = 404, detail = 'User not found')'''

    #Validar que el id de pelicula exista
    if Movie.select().where(Movie.id == user_reviews.movie_id).first() is None:
        raise HTTPException(status_code = 404, detail = 'Movie not found')

    #Crear a partir de los datos que envie el cliente
    user_reviews = UserReview.create(
        user_id = user.id, #Owner
        movie_id = user_reviews.movie_id,
        reviews = user_reviews.reviews,
        score = user_reviews.score
    )

    return user_reviews

#Obtener listado de resenias #TODAS
#Indicamos retornar listado de objetos tipo reviewresponseModel
# @app.get('/reviews', response_model = List[ReviewResponseModel])
# async def get_reviews():
#     reviews = UserReview.select().paginate(page, limit) #SELECT * FROM user_reviews

#     #generar lista de objetos user_review
#     return [user_reviews for user_reviews in reviews]

#24/02/2024 JAR
#Obtener listado de X cantidad de resenias
@router.get('', response_model = List[ReviewResponseModel])
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
@router.get('/{review_id}', response_model = ReviewResponseModel)
async def get_review(review_id : int):
    
    #Realizar peticion
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(status_code = 404, detail = 'Review not found')
    
    return user_review

#Actualizar resenia, con respecto a valores que se envian
#Valores deben de enviarse a traves el cuerpo de la peticion. que son el segundo parametro de la funcion async
@router.put('/{review_id}', response_model = ReviewResponseModel)
#En segundo parametro, vienen los datos enviados
async def update_review(review_id : int, review_request: ReviewRequestPutModel, user : User = Depends(get_current_user)):

    #Obtener resenia a actualizar
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(status_code = 404, detail = 'Review not found')
    
    #Usuario autenticado mediante OAuth2
    if user_review.user_id != user.id:
        raise HTTPException(status_code=401, detail="No eres propietario")
    
    user_review.reviews = review_request.reviews
    user_review.score = review_request.score

    user_review.save()

    return user_review
    
@router.delete('/{review_id}', response_model = ReviewRequestDeleteModel)
async def delete_review(review_id : int, user : User = Depends(get_current_user)) :
    
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    #Usuario autenticado mediante OAuth2
    if user_review.user_id != user.id:
        raise HTTPException(status_code=401, detail="No eres propietario")

    if user_review is None:
        raise HTTPException(status_code = 404, detail = 'Review not found')
    

    user_review.delete_instance()

    return user_review