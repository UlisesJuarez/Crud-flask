from re import template
from flask import Flask, redirect, url_for, render_template,request,flash
from datetime import datetime
from flask_mysqldb import MySQL
from routes import *


app=Flask(__name__)
app.register_blueprint(routes)
app.secret_key="clave_secreta_flask"
#conexion bd
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='proyectoflask'

mysql=MySQL(app)
#context processors
@app.context_processor
def date_now():

    return {
        'now':datetime.utcnow()
    }

@app.route('/')
def index():
    edad=101
    personas=['Ulises','Mariela','Dalila']
    return render_template('index.html',edad=edad,dato2="Valor 2",personas=personas)



@app.route('/contacto')
@app.route('/contacto/<redireccion>')
def contacto(redireccion=None):
    if redireccion!=None:
        #permite redirigir a la funcion 
        return redirect(url_for('lenguajes'))
    return render_template('contacto.html')


@app.route("/crear-coche",methods=['GET','POST'])
def crear_coche():

    if request.method=='POST':
        marca=request.form['marca']
        modelo=request.form['modelo']
        precio=request.form['precio']
        ciudad=request.form['ciudad']
        cursor=mysql.connection.cursor()
        cursor.execute("insert into coches values(NULL,%s,%s,%s,%s)",(marca,modelo,precio,ciudad))
        cursor.connection.commit()
        flash('Has creado el coche correctamente!!')
        return redirect(url_for('index'))
    return render_template('crear_coche.html')

@app.route("/coches")
def coches():
    cursor=mysql.connection.cursor()
    cursor.execute("select*from coches order by id desc")
    coches=cursor.fetchall()
    cursor.close()

    return render_template("coches.html",coches=coches)

@app.route("/coche/<coche_id>")
def coche(coche_id):
    cursor=mysql.connection.cursor()
    cursor.execute("select*from coches where id=%s",(coche_id))
    coche=cursor.fetchall()
    cursor.close()

    return render_template("coche.html",coche=coche[0])

@app.route("/borrar-coche/<coche_id>")
def borrar_coche(coche_id):
    cursor=mysql.connection.cursor()
    cursor.execute("delete from coches where id=%s",(coche_id))
    mysql.connection.commit()

    flash('El coche ha sido eliminado')

    return redirect(url_for('coches'))

@app.route("/editar-coche/<coche_id>",methods=['GET','POST'])
def editar_coche(coche_id):

    if request.method=='POST':
        marca=request.form['marca']
        modelo=request.form['modelo']
        precio=request.form['precio']
        ciudad=request.form['ciudad']
        cursor=mysql.connection.cursor()
        cursor.execute("""
        update coches 
        set marca=%s,
        modelo=%s,
        precio=%s,
        ciudad=%s
        where id=%s
        """,(marca,modelo,precio,ciudad,coche_id))
        cursor.connection.commit()
        flash('Has actualizado datos del coche correctamente!!')
        return redirect(url_for('coches'))
    cursor=mysql.connection.cursor()
    cursor.execute("select*from coches where id=%s",(coche_id))
    coche=cursor.fetchall()
    cursor.close()

    return render_template("crear_coche.html",coche=coche[0])

if __name__=='__main__':
    app.run(debug=True)