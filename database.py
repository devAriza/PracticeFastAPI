from peewee import * 

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