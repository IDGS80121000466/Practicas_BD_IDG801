import os
from sqlalchemy import create_engine
import urllib

class Config(object):
    SECRET_KEY = 'Clave nueva'
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Soporte2003@localhost/pizzas'
    SQLALCHEMY_BINDS = {
        'prueba': 'mysql+pymysql://root:Soporte2003@localhost/prueba',
        'pizzas': 'mysql+pymysql://root:Soporte2003@localhost/pizzas'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
