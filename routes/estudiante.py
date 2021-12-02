from flask import render_template,request,redirect,flash,url_for
from . import routes
from operacionesBD import Op_estudiante

@routes.route('/nuevo-estudiante')
def nuevoEstudiante():
    return render_template('estudiante/nuevoEstudiante.html')


@routes.route("/guardar_estudiante", methods=["POST"])
def guardar_estudiante():
    if request.method=="POST":
        nombre = request.form["nombre"]
        apellidos = request.form["apellidos"]
        email = request.form["email"]
        password=request.form["password"]
        edad=request.form["edad"]
        grupo=request.form["grupo"]
        Op_estudiante.insertar_estudiante(nombre, apellidos, email,password,edad,grupo)
        flash(f'{nombre} te has registrado correctamente!!')
        return redirect(url_for('index'))
    return render_template('estudiante/nuevoEstudiante')


@routes.route("/listaEstudiantes")
def listaEstudiantes():
    estudiantes=Op_estudiante.obtener_estudiantes()

    return render_template("estudiante/listaEstudiantes.html",estudiantes=estudiantes)