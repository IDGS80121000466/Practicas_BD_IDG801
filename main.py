
from flask import Flask, render_template, request, send_from_directory
from forms import UserForm2
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
from flask import flash

from models import db
from models import Empleados

import os
import forms

app = Flask(__name__)
app.secret_key = 'esta es mi clave secreta'
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()

@app.errorhandler(404)
def page_not_fouund(e):
    return render_template('404.html'),404

@app.route("/")
def indexx():
    return render_template("index.html")

@app.route('/index', methods=['POST', 'GET'])
def index():
    create_form = forms.UserForm2(request.form)
    if request.method == 'POST' and create_form.validate():
        alum = Empleados(
            nombre=create_form.nombre.data,
            direccion=create_form.direccion.data,
            telefono=create_form.telefono.data,
            correo=create_form.correo.data,
            sueldo=create_form.sueldo.data,
        )
        db.session.add(alum)
        db.session.commit()
        flash('Empleado registrado exitosamente')
    return render_template('index.html', form=create_form)

@app.route('/ABC_Completo', methods=['POST', 'GET'])
def ABCompleto():
    emple_form = forms.UserForm2(request.form)
    empleados = Empleados.query.all()
    
    return render_template('ABC_Completo.html', empleados=empleados)






@app.route("/static/bootstrap/css/<path:filename>")
def send_css(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'bootstrap', 'css'), filename, mimetype='text/css')


if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)

with app.app_context():
    db.create_all()
app.run()




