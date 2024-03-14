from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session
from forms import UserForm2, PizzaForm, BuscarVenta
from flask_wtf.csrf import CSRFProtect
from config import Config
from flask import g
from flask import flash
from sqlalchemy import func
from datetime import datetime, date
from models import db, Empleados, Clientes, DetalleVentas
import os
import forms, calendar

app = Flask(__name__)
app.secret_key = 'esta es mi clave secreta'
app.config.from_object(Config)
csrf = CSRFProtect()

db.init_app(app)

@app.errorhandler(404)
def page_not_fouund(e):
    return render_template('404.html'),404

@app.route("/")
def indexx():
    return render_template("principal.html")

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

@app.route('/eliminar', methods=['POST', 'GET'])
def eliminar():
    create_form = forms.UserForm2(request.form)
    if request.method=='GET':
        id= request.args.get('id')
        # SELECT * FROM empleados WHERE id = id
        emple1 = db.session.query(Empleados).filter(Empleados.id == id).first()
        create_form.id.data = request.args.get('id')
        create_form.nombre.data= emple1.nombre
        create_form.direccion.data= emple1.direccion
        create_form.telefono.data= emple1.telefono
        create_form.correo.data= emple1.correo
        create_form.sueldo.data= emple1.sueldo
    if request.method=='POST':
        id=create_form.id.data
        emple =Empleados.query.get(id)
        #DELETE from empleados WHERE id = id
        db.session.delete(emple)
        db.session.commit()
        return redirect(url_for('ABCompleto'))
    return render_template('eliminar.html',form=create_form)

@app.route('/modificar', methods=['POST', 'GET'])
def modificar():
    create_form = forms.UserForm2(request.form)
    if request.method=='GET':
        id= request.args.get('id')
        emple1 = db.session.query(Empleados).filter(Empleados.id == id).first()
        create_form.id.data = request.args.get('id')
        create_form.nombre.data= emple1.nombre
        create_form.direccion.data= emple1.direccion
        create_form.telefono.data= emple1.telefono
        create_form.correo.data= emple1.correo
        create_form.sueldo.data= emple1.sueldo
    if request.method=='POST':
        id=create_form.id.data
        emple1 = db.session.query(Empleados).filter(Empleados.id == id).first()
        emple1.nombre = create_form.nombre.data
        emple1.direccion = create_form.direccion.data
        emple1.telefono = create_form.telefono.data
        emple1.correo = create_form.correo.data
        emple1.sueldo = create_form.sueldo.data
        db.session.add(emple1)
        db.session.commit()
        return redirect(url_for('ABCompleto'))
    return render_template('modificar.html',form=create_form)


@app.route('/pizza', methods=['POST', 'GET'])
def pizza():
    form = PizzaForm()
    formBVenta = BuscarVenta()
    cliente = session.get('cliente', {'nombre': '', 'direccion': '', 'telefono': ''})  
    if request.method == 'POST' and form.validate_on_submit():
        nombre = form.nombre.data
        direccion = form.direccion.data
        telefono = form.telefono.data
        try:
            ingredientes_seleccionados = request.form.getlist('ingredientes[]')
            ingredientes = ','.join(ingredientes_seleccionados)
            cliente_nuevo = Clientes(
                nombre=nombre,
                direccion=direccion,
                telefono=telefono,
                fechaCompra=form.fecha.data,
                tamano=form.tamano.data,
                ingredientes=ingredientes,
                numeroPizzas=int(form.numeroPizzas.data),
                subtotal=calcular_subtotal(form.tamano.data, ingredientes_seleccionados, form.numeroPizzas.data)               
            )
            db.session.add(cliente_nuevo)
            db.session.commit()
            flash('Pedido agregado al carrito exitosamente', 'success')
            session['cliente'] = {'nombre': nombre, 'direccion': direccion, 'telefono': telefono}
            return redirect(url_for('mostrarPizzas'))
        except Exception as e:
            flash(str(e), 'error')
    return render_template('pizzas.html', form=form, cliente=cliente, formBVenta=formBVenta)


def calcular_subtotal(tamano, ingredientes, numero_pizzas):
    precios_tamano = {
        'chica': 40,
        'mediana': 80,
        'grande': 120
    }
    precios_ingredientes = {
        'jamon': 10,
        'pina': 10,
        'champinones': 10
    }
    subtotal = precios_tamano.get(tamano, 0)
    costo_ingredientes = sum(precios_ingredientes.get(ingrediente, 0) for ingrediente in ingredientes)
    subtotal += costo_ingredientes
    subtotal *= numero_pizzas
    print(subtotal)
    return subtotal

@app.route('/mostrarPizzas', methods=['GET'])
def mostrarPizzas():
    pizzas = Clientes.query.all()
    form = PizzaForm() 
    formBVenta = BuscarVenta()
    cliente = session.get('cliente', {'nombre': '', 'direccion': '', 'telefono': ''})
    return render_template('pizzas.html', pizzas=pizzas, form=form, formBVenta = formBVenta, cliente=cliente)

@app.route('/modificarPizzas', methods=['POST', 'GET'])
def modificarPizzas():
    formBVenta = BuscarVenta()
    create_form = forms.PizzaForm(request.form)
    if request.method == 'GET':
        idCliente = request.args.get('idCliente')
        pizza = db.session.query(Clientes).filter(Clientes.idCliente == idCliente).first()
        create_form.idCliente.data = idCliente
        create_form.nombre.data = pizza.nombre
        create_form.direccion.data = pizza.direccion
        create_form.telefono.data = pizza.telefono
        create_form.tamano.data = pizza.tamano
        create_form.ingredientes.data = pizza.ingredientes
        create_form.numeroPizzas.data = pizza.numeroPizzas
    if request.method == 'POST':
        ingredientes_seleccionados = request.form.getlist('ingredientes[]')
        ingredientes = ingredientes_seleccionados  # Usar la lista directamente
        idCliente = create_form.idCliente.data
        pizza = db.session.query(Clientes).filter(Clientes.idCliente == idCliente).first()
        pizza.nombre = create_form.nombre.data
        pizza.direccion = create_form.direccion.data
        pizza.telefono = create_form.telefono.data
        pizza.fechaCompra = create_form.fecha.data
        pizza.tamano = create_form.tamano.data
        pizza.ingredientes = ','.join(ingredientes_seleccionados)  # Convertir nuevamente a cadena si es necesario
        pizza.numeroPizzas = create_form.numeroPizzas.data
        pizza.subtotal = calcular_subtotal(create_form.tamano.data, ingredientes, create_form.numeroPizzas.data)  # Pasar los datos correctamente
        db.session.commit()
        return redirect(url_for('mostrarPizzas'))
    return render_template('modificarPizzas.html', form=create_form, formBVenta = formBVenta)

@app.route('/eliminarPizzas', methods=['POST', 'GET'])
def eliminarPizzas():
    formBVenta = BuscarVenta()
    create_form = forms.PizzaForm(request.form)
    if request.method == 'GET':
        idCliente = request.args.get('idCliente')
        pizza = db.session.query(Clientes).filter(Clientes.idCliente == idCliente).first()
        create_form.idCliente.data = idCliente
        create_form.nombre.data = pizza.nombre
        create_form.direccion.data = pizza.direccion
        create_form.telefono.data = pizza.telefono
        create_form.tamano.data = pizza.tamano
        create_form.ingredientes.data = pizza.ingredientes
        create_form.numeroPizzas.data = pizza.numeroPizzas
    if request.method == 'POST':
        idCliente = create_form.idCliente.data
        pizza = Clientes.query.get(idCliente)
        db.session.delete(pizza)
        db.session.commit()
        return redirect(url_for('mostrarPizzas'))
    return render_template('eliminarPizzas.html', form=create_form, formBVenta = formBVenta)


@app.route('/alertaConfirmacion', methods=['GET'])
def alertaConfirmacion():
    formBVenta = BuscarVenta()
    form = PizzaForm
    total_ventas = db.session.query(func.sum(Clientes.subtotal)).scalar() or 0   
    cliente = session.get('cliente', {'nombre': '', 'direccion': '', 'telefono': ''})
    return render_template('alertaConfirmacion.html', total_ventas=total_ventas, form = form, formBVenta = formBVenta, cliente = cliente)

@app.route('/guardarDetalleVenta', methods=['POST'])
def guardarDetalleVenta():
    form = PizzaForm()
    formBVenta = BuscarVenta()
    clientes = Clientes.query.all()  
    for cliente in clientes:
        nueva_venta = DetalleVentas(
            nombre=cliente.nombre,
            direccion=cliente.direccion,
            telefono=cliente.telefono,
            fechaCompra=cliente.fechaCompra,
            tamano=cliente.tamano,
            ingredientes=cliente.ingredientes,
            numeroPizzas=cliente.numeroPizzas,
            subtotal=cliente.subtotal
        )
        db.session.add(nueva_venta)
        db.session.delete(cliente)
    db.session.commit()
    #session.clear()
    ventas_hoy = DetalleVentas.query.filter(DetalleVentas.fechaCompra >= date.today()).all()
    total_ventas_dia = sum(venta.subtotal for venta in ventas_hoy)
    flash('Pedido guardado exitosamente', 'success')
    print("Total de ventas del día:", total_ventas_dia)   
    return render_template('pizzas.html', ventas_del_dia=ventas_hoy, totalVentasDia=total_ventas_dia, form=form, formBVenta=formBVenta)


@app.route('/buscarVentas', methods=['POST', 'GET'])
def buscarVentas():
    form = PizzaForm()
    formBVenta = BuscarVenta()    
    if request.method == 'POST' and formBVenta:
        try:
            dia = formBVenta.dia.data
            mes = formBVenta.mes.data
            anio = formBVenta.anio.data
            diaTexto = formBVenta.diaTexto.data
            mesTexto = formBVenta.mesTexto.data           
            ventas = DetalleVentas.query           
            if diaTexto:
                diaTextoCap = diaTexto.capitalize()
                diaNumero = None
                if diaTextoCap == 'Lunes':
                    diaNumero = 2
                elif diaTextoCap == 'Martes':
                    diaNumero = 3
                elif diaTextoCap == 'Miércoles':
                    diaNumero = 4
                elif diaTextoCap == 'Jueves':
                    diaNumero = 5
                elif diaTextoCap == 'Viernes':
                    diaNumero = 6
                elif diaTextoCap == 'Sábado':
                    diaNumero = 7
                elif diaTextoCap == 'Domingo':
                    diaNumero = 1
                if diaNumero is not None:
                    ventas = ventas.filter(func.DAYOFWEEK(DetalleVentas.fechaCompra) == diaNumero)
                else:
                    return render_template('pizzas.html', ventas=[], form=form, formBVenta=formBVenta, totalVentasB=0)
            
            if mesTexto:
                mesTextoCap = mesTexto.capitalize()
                mesNumero = None
                if mesTextoCap == 'Enero':
                    mesNumero = 1
                elif mesTextoCap == 'Febrero':
                    mesNumero = 2
                elif mesTextoCap == 'Marzo':
                    mesNumero = 3
                elif mesTextoCap == 'Abril':
                    mesNumero = 4
                elif mesTextoCap == 'Mayo':
                    mesNumero = 5
                elif mesTextoCap == 'Junio':
                    mesNumero = 6
                elif mesTextoCap == 'Julio':
                    mesNumero = 7
                elif mesTextoCap == 'Agosto':
                    mesNumero = 8
                elif mesTextoCap == 'Septiembre':
                    mesNumero = 9
                elif mesTextoCap == 'Octubre':
                    mesNumero = 10
                elif mesTextoCap == 'Noviembre':
                    mesNumero = 11
                elif mesTextoCap == 'Diciembre':
                    mesNumero = 12
                if mesNumero is not None:
                    ventas = ventas.filter(func.extract('month', DetalleVentas.fechaCompra) == mesNumero)
                else:
                    return render_template('pizzas.html', ventas=[], form=form, formBVenta=formBVenta, totalVentasB=0)         
            if dia:
                ventas = ventas.filter(func.extract('day', DetalleVentas.fechaCompra) == dia)            
            if mes:
                ventas = ventas.filter(func.extract('month', DetalleVentas.fechaCompra) == mes)            
            if anio:
                ventas = ventas.filter(func.extract('year', DetalleVentas.fechaCompra) == anio)                            
            resultados = ventas.all() 
            totalVentasB = ventas.with_entities(func.sum(DetalleVentas.subtotal)).scalar() or 0            
            return render_template('pizzas.html', ventas=resultados, form=form, formBVenta=formBVenta, totalVentasB=totalVentasB)
        except Exception as e:
            print("Error:", e)
    return render_template('pizzas.html', form=form, formBVenta=formBVenta)


@app.route("/static/bootstrap/css/<path:filename>")
def send_css(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'bootstrap', 'css'), filename, mimetype='text/css')

if __name__ == "__main__":
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()