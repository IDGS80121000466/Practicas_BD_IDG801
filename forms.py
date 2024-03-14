from wtforms import Form
from flask_wtf import FlaskForm

from wtforms import StringField, TelField, IntegerField, FloatField, SelectField, RadioField, SelectMultipleField, DateField
from wtforms.validators import Length
from wtforms import EmailField

from wtforms import validators

class UserForm2(Form):
    id = IntegerField('id', validators=[validators.Optional(), validators.NumberRange(min=1, max=20, message='Valor no válido')])
    nombre=StringField('nombre',[validators.DataRequired(message='El campo Nombre es requerido'),
                                 validators.Length(min=4,max=10,message='Ingresa nombre valido')])
    direccion=StringField('direccion',[validators.DataRequired(message='El campo Direccion es requerido'),
                                 validators.Length(min=4,max=20,message='Ingresa una Direccion valida')])
    telefono = TelField('telefono', [validators.DataRequired(message='El campo Telefono es requerido')])
    correo=EmailField('correo',[validators.Email(message='Ingrese un correo valido')])
    sueldo = FloatField('sueldo', [validators.DataRequired(message='El campo Sueldo es requerido')])


class PizzaForm(FlaskForm):
    idCliente = IntegerField('id', validators=[validators.Optional(), validators.NumberRange(min=1, max=20, message='Valor no válido')])
    nombre = StringField('Nombre', [validators.DataRequired(), validators.Length(min=4, max=20)])
    direccion = StringField('Dirección', [validators.DataRequired(), validators.Length(min=4, max=20)])
    telefono = StringField('Teléfono', [validators.DataRequired()])
    tamano = RadioField('Tamano', choices=[('chica', 'Chica $40'), ('mediana', 'Mediana $80'), ('grande', 'Grande $120')], validators=[validators.DataRequired()])
    ingredientes = SelectMultipleField('Ingredientes', choices=[('jamon', 'Jamón $10'), ('pina', 'Piña $10'), ('champinones', 'Champiñones $10')])
    numeroPizzas = FloatField('numeroPizzas', [validators.DataRequired(message='El campo Sueldo es requerido')])
    fecha = DateField('Fecha', format='%Y-%m-%d')

class BuscarVenta(FlaskForm):
    # dia = IntegerField('dia', validators=[validators.NumberRange(min=1, max=2, message='Dia no válido')])
    dia = IntegerField('dia')
    mes = IntegerField('mes')
    anio = IntegerField('annio')
    diaTexto = StringField('diaTexto')
    mesTexto = StringField('mesTexto')
