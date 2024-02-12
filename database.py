import hashlib
from peewee import * 
from datetime import datetime

#Clase MySQLDatabase
#nameBD
#user = 'user'
#password = ''
#host = 'localhost'
#port = 3306 #Puerto por default utilizado por MySQL

nameBD = 'fastapi_project'
usuario = 'root'
hosst = 'localhost'
puerto = 3306

database = MySQLDatabase(nameBD, user = usuario, password = '', host = hosst, port = puerto)

#Para que una clase se considere modelo, hereda de la clase Model

class User(Model):
    username = CharField(max_length = 50, unique = True) #No acepta valores duplicados
    password = CharField(max_length = 50)
    create_at = DateTimeField(default = datetime.now)

    def __str__(self): #cada que se crea, retorna el user
        return self.username
    
    class Meta:
        database = database
        table_name = 'users'

    #Encriptar contrasenia
    #Metodo de clase indicado con el decorador classmethod
    @classmethod
    def create_password(cls, password):
        h = hashlib.md5()
        #Codificar contrasenia a utf-8
        h.update(password.encode('utf-8'))

        #retorna el hexadecimal de la contrasenia
        return h.hexdigest()

class Movie(Model):
    title = CharField(max_length = 50, unique = True)
    created_at = DateTimeField(default = datetime.now)

    def __str__(self):
        return self.title
    
    class Meta:
        database = database
        table_name = 'movies'
    

class UserReview(Model):
    user = ForeignKeyField(User, backref = 'reviews')
    movie = ForeignKeyField(Movie, backref = 'reviews')
    reviews = TextField()
    score = IntegerField()
    created_at = DateTimeField(default = datetime.now)
    
    def __str__(self):
        return f'{self.user.username} - #{self.movie.title}'
    
    class Meta:
        database = database
        table_name = 'user_review'