from wtforms import Form
from flask_wtf import FlaskForm

from wtforms import StringField, TelField, IntegerField, FloatField
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


