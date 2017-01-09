from flask import Flask, render_template, redirect, url_for, request, session
import os
from flask_login import LoginManager
from flask.ext import shelve
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)
#app.config['SHELVE_FILENAME'] = 'datos.db'
#shelve.init_app(app)

@app.route('/')
@app.route('/principal')
def home():
    titulo = "HOME"
    if session.get('logged_in') is not None:
        if session['logged_in'] == True:
            session['enlaces'].insert(0, "HOME")
    return render_template('index.html', titulo=titulo)

@app.route('/comida')
def comida():
    titulo = "COMIDA"
    if session.get('logged_in') is not None:
        if session['logged_in'] == True:
            session['enlaces'].insert(0, "COMIDA")
    return render_template('comida.html', titulo=titulo)

@app.route('/contacto')
def contacto():
    titulo = "CONTACTO"
    if session.get('logged_in') is not None:
        if session['logged_in'] == True:
            session['enlaces'].insert(0, "CONTACTO")
    return render_template('contacto.html', titulo=titulo)

@app.route('/registro')
def registro():
    titulo = "REGISTRO"
    if session.get('logged_in') is not None:
        if session['logged_in'] == True:
            session['enlaces'].insert(0, "REGISTRO")
    return render_template('registro.html', titulo=titulo)

@app.route('/insert')
def insert():
    titulo = "INSERTAR RESTAURANTE"
    if session.get('logged_in') is not None:
        if session['logged_in'] == True:
            session['enlaces'].insert(0, "INSERTAR RESTAURANTE")
    return render_template('insertar.html', titulo=titulo)

@app.route('/mod')
def mod():
    titulo = "MODIFICAR RESTAURANTE"
    if session.get('logged_in') is not None:
        if session['logged_in'] == True:
            session['enlaces'].insert(0, "MODIFICAR RESTAURANTE")
    return render_template('mod.html', titulo=titulo)

@app.route('/editar')
def editar():
    titulo = "EDITAR"
    if session.get('logged_in') is not None:
        if session['logged_in'] == True:
            session['enlaces'].insert(0, "EDITAR")
            db = shelve.get_shelve('c')
            nombre = session['nombre']
            nombre = nombre.encode('utf8')
            session['contra'] = db[nombre]['contra']
            session['name'] = db[nombre]['nombre']
            session['apellidos'] = db[nombre]['apellidos']
            session['correo']=db[nombre]['email']
    return render_template('editar.html', titulo=titulo)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/login', methods=['POST'])
def login():
    error = None
    titulo = "HOME"
    db = shelve.get_shelve('c')
    usuario = request.form['username']
    usuario = usuario.encode('utf8')
    password = request.form['password']
    password = password.encode('utf8')
    if usuario in db and db[usuario]['contra'] == password:
        session['logged_in'] = True
        session['nombre'] = request.form['username']
        session['enlaces'] = []
    else:
        error = "Usuario o password erroneo."
    return render_template('index.html', error=error, titulo=titulo)

@app.route('/buscar', methods=['POST'])
def buscar():
    error4 = None
    titulo = "MODIFICAR RESTAURANTE"

    nombre=request.form['nombre']
    nombre=nombre.encode('utf8')
    ide=request.form['id']
    ide=ide.encode('utf8')

    mongoClient = MongoClient()
    db = mongoClient.test
    collection = db.restaurants

    if not collection.find({"name": nombre}).count() == 0 and not collection.find({"restaurant_id": ide}).count() == 0:
        error4 = " "
        session['nombre_restaurante'] = nombre
        session['id_restaurante'] = ide
        cursor = collection.find({"name": nombre, "restaurant_id": ide})
        cursor2 = {}
        for i in cursor:
            session['ciudad'] = i['borough']
            session['cocina'] = i['cuisine']
            session['calle'] =  i["address"]['street']
            session['edificio'] = i["address"]['building']
            session['cp'] = i["address"]['zipcode']

    else:
        error4 = "No existe un restaurante llamado de ese modo."
    mongoClient.close()
    return render_template('mod.html', error4=error4, titulo=titulo)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session['enlaces'] = []
    return home()

@app.route('/alta', methods=['POST'])
def alta():
    error2 = ""
    titulo = "REGISTRAR"
    nombreUsuario=request.form['nombreusuario']
    nombreUsuario=nombreUsuario.encode('utf8')
    contra=request.form['password']
    contra=contra.encode('utf8')
    nombre=request.form['nombre']
    nombre=nombre.encode('utf8')
    apellidos=request.form['apellidos']
    apellidos=apellidos.encode('utf8')
    email=request.form['email']
    email=email.encode('utf8')
    db = shelve.get_shelve('c')
    if nombreUsuario in db:
        error2 = "Usuario existente."
        return render_template('registro.html', error2=error2, titulo=titulo)
    else:
        db[nombreUsuario] = {'nombreusuario': nombreUsuario, 'contra': contra,  'nombre': nombre, 'apellidos': apellidos, 'email': email}
        return home()

@app.route('/modificar', methods=['POST'])
def modificar():
    nombreUsuario = session['nombre']
    nombreUsuario = nombreUsuario.encode('utf8')
    contra=request.form['password']
    contra=contra.encode('utf8')
    name=request.form['name']
    name=name.encode('utf8')
    apellidos=request.form['apellidos']
    apellidos=apellidos.encode('utf8')
    email=request.form['email']
    email=email.encode('utf8')
    db = shelve.get_shelve('c')
    db[nombreUsuario] = {'nombreusuario': nombreUsuario, 'contra': contra,  'nombre': name, 'apellidos': apellidos, 'email': email}
    return home()

@app.route('/modificar_restaurante', methods=['POST'])
def modificar_restaurante():
    nombre_r = session['nombre_restaurante']
    ide = session['id_restaurante']
    ciudad=request.form['ciudad']
    ciudad=ciudad.encode('utf8')
    calle=request.form['calle']
    calle=calle.encode('utf8')
    edificio=request.form['edificio']
    edificio=edificio.encode('utf8')
    cp=request.form['cp']
    cp=cp.encode('utf8')
    cocina=request.form['cocina']
    cocina=cocina.encode('utf8')

    mongoClient = MongoClient()
    db = mongoClient.test
    collection = db.restaurants
    result = collection.update_many(
    {"name": nombre_r, "restaurant_id": ide},
    {
        "$set": {"cuisine": cocina, "borough": ciudad, "address.zipcode": cp, "address.building": edificio, "address.street" : calle}
    })
    mongoClient.close()
    return home()


@app.route('/insertar', methods=['POST'])
def insertar():
    error3 = ""
    titulo = "INSERTAR RESTAURANTE"

    ciudad=request.form['ciudad']
    ciudad=ciudad.encode('utf8')
    calle=request.form['calle']
    calle=calle.encode('utf8')
    edificio=request.form['edificio']
    edificio=edificio.encode('utf8')
    cp=request.form['cp']
    cp=cp.encode('utf8')
    nombre=request.form['nombre']
    nombre=nombre.encode('utf8')
    ide=request.form['id']
    ide=ide.encode('utf8')
    cocina=request.form['cocina']
    cocina=cocina.encode('utf8')

    mongoClient = MongoClient()
    db = mongoClient.test
    collection = db.restaurants
    if not collection.find({"name": nombre}).count() == 0 or not collection.find({"restaurant_id": ide}).count() == 0:
        error3 = "Nombre de Restaurante o Identificador usados."
        return render_template('insertar.html', error3=error3, titulo=titulo)
    else:
        result = collection.insert(
        {
            "address": {
                "street": calle,
                "zipcode": cp,
                "building": edificio,
                "coord": [-73.9557413, 40.7720266]
            },
            "borough": ciudad,
            "cuisine": cocina,
            "grades": [
                {
                    "date": datetime.strptime("2014-10-01", "%Y-%m-%d"),
                    "grade": "A",
                    "score": 11
                },
                {
                    "date": datetime.strptime("2014-01-16", "%Y-%m-%d"),
                    "grade": "B",
                    "score": 17
                }
            ],
            "name": nombre,
            "restaurant_id": ide
        })
    mongoClient.close()
    return home()


if __name__ == '__main__':
    port=int(os.environ.get('PORT',2080))
    app.run(host='0.0.0.0', port=port)
    #app.run(debug=True)
