from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()  # Instancia única de SQLAlchemy

# Modelo vinculado a la base de datos "prueba"
class Empleados(db.Model):
    __tablename__= 'empleados'
    __bind_key__ = 'prueba' 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50))
    direccion = db.Column(db.String(50))
    telefono = db.Column(db.String(50))
    correo = db.Column(db.String(50))
    sueldo = db.Column(db.Float)

# Modelos vinculados a la base de datos "pizzas"
class Clientes(db.Model):
    __tablename__ = 'clientes'
    __bind_key__ = 'pizzas'
    idCliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50))
    direccion = db.Column(db.String(50))
    telefono = db.Column(db.String(20))
    fechaCompra = db.Column(db.DateTime)
    tamano = db.Column(db.String(50))
    ingredientes = db.Column(db.Text)
    numeroPizzas = db.Column(db.Integer)
    subtotal = db.Column(db.Float)

class DetalleVentas(db.Model):
    __tablename__ = 'detalleVentas'
    __bind_key__ = 'pizzas'
    idDetalle = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50))
    direccion = db.Column(db.String(50))
    telefono = db.Column(db.String(20))
    fechaCompra = db.Column(db.DateTime)
    tamano = db.Column(db.String(50))
    ingredientes = db.Column(db.Text)
    numeroPizzas = db.Column(db.Integer)
    subtotal = db.Column(db.Float)