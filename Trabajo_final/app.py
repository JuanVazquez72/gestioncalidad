
from passlib.hash import sha256_crypt
from flask import Flask, render_template, request, redirect, session, url_for

from funciones import graba_diccionario, graba_diccionario_trabajador ,lee_diccionario_csv,graba_diccionario_id, lee_diccionario_csv_id, lee_diccionario_csv_bicicleta, sacar_usuarios,lee_diccionario_csv_trabajadores, lee_diccionario_csv_admin,graba_diccionario_admin
import datetime


diccionario_mascotas={}
archivo_usuarios = 'usuarios.csv'

archivo_citas = 'citas.csv'
archivo_comentarios = 'comentarios.csv'
diccionario_usuarios = lee_diccionario_csv(archivo_usuarios)
diccionario_bicicletas = lee_diccionario_csv_bicicleta('bicicletas.csv')
diccionario_citas = lee_diccionario_csv_id(archivo_citas)
diccionario_comentarios = lee_diccionario_csv('comentarios.csv')




logeado = False
first_login = False

deslog = False
confirmacion = False
comentario_confirmacion = False
id = 0

app = Flask(__name__)
app.secret_key = "klNmsS679SDqWpñl"

@app.route("/")
def index():
    
    if logeado == True:
        user = session['usuario']
        if user in diccionario_usuarios:
            return render_template("index.html")
        else:
            if user in diccionario_trabajadores:
                return render_template("index_trabajador.html")
    else:
        try:
            user = session['usuario']
            if user in diccionario_usuarios:
                return render_template("index.html")
            else:
                if user in diccionario_trabajadores:
                     return render_template("index_trabajador.html")
        except:
            return render_template("index.html")
        return render_template("index_admin.html")



@app.route("/login/", methods=['GET','POST'])
def ingresar():
    logeado = False
    if "logged_in" in session:
        if session["logged_in"] == True:
            logeado = True

    if logeado == False:        
        if request.method == 'GET':
            msg = ''
            return render_template('login.html',mensaje=msg)
        else:
            if request.method == 'POST':
                usuario = request.form['usuario']

                if usuario in diccionario_usuarios:
                    password_db = diccionario_usuarios[usuario]['password'] # password guardado
                    password_forma = request.form['password'] #password presentado
                    verificado = sha256_crypt.verify(password_forma,password_db)
                    if (verificado == True):
                        session['usuario'] = usuario
                        session['logged_in'] = True
                        first_login = True
                        logeado = True
                        return render_template("index.html", first = first_login)
                    else:
                        msg = f'El password de {usuario} no corresponde'
                        return render_template('login.html',mensaje=msg)
                
                    
    else:
        msg = 'YA ESTA LOGEADO'
        return render_template('index.html')
   
    

@app.route('/logout', methods=['GET'])
@app.route('/logout/', methods=['GET'])
def logout():
    if request.method == 'GET':
        session.clear()
        session["logged_in"] = False
        deslog = True
        logeado = False
        return render_template("index.html", deslogeado = deslog)



@app.route("/register/", methods=['POST','GET'])
def registrarse():
    if request.method == 'POST':
                valor = request.form['enviar']
                if valor == 'Entrar':
                    nombre  =  request.form['ncompleto']
                    correo    =  request.form['correo']
                    usuario =  request.form['usuario']
                    password = request.form['password']
                    password = sha256_crypt.hash(password)
                    tipo = "usuario"
                    
                    if usuario not in diccionario_usuarios and usuario:
                        diccionario_usuarios[usuario] = {
                            'nombre': nombre,
                            'correo'  : correo,
                            'usuario' : usuario,
                            'password' : password,
                            'tipo' : tipo
                        }
                    lista_usuarios = usuario
                    graba_diccionario(diccionario_usuarios,'usuario',archivo_usuarios)
                #return render_template('lista_usuarios.html',dicc_usuarios=diccionario_usuarios)
                return redirect('/')
    else:
     return render_template("register.html")


@app.route('/comentarios', methods=['POST','GET'])
def comentarios():
    if request.method == 'POST':
            comentario = request.form['comentario']
            usuario =  session['usuario']  
            diccionario_comentarios[usuario] = {
                            'nombre': usuario,
                            'comentario': comentario
                         }
            print(diccionario_comentarios)
            
            graba_diccionario(diccionario_comentarios,'usuario',archivo_comentarios) 
            comentario_confirmacion = True
            return render_template('index.html', comentario_confirmacion= comentario_confirmacion)
    else:
        return render_template('comentarios.html')




@app.route("/lista_bicicletas/", methods=['GET'])
def dar_lista():
     if request.method == 'GET':
        return render_template("lista_bicicletas.html")


@app.route("/citas/", methods=['GET','POST'])
def citas():
     if request.method == 'GET':
        
        hoy_completo = datetime.datetime.today()
        fecha_hoy  = datetime.datetime.strftime(hoy_completo,"%Y-%m-%d")
        return render_template("calendario.html",dicc_bicicletas=diccionario_bicicletas, hoy=fecha_hoy)
     else:
        if request.method == 'POST':
            
            valor = request.form['enviar']
            if valor == 'Rentar':
                bicicleta =  request.form['bicicleta']
                fecha    =  request.form['fecha']
                usuario =  session['usuario']
                diccionario_citas = lee_diccionario_csv_id(archivo_citas)
                id = len(diccionario_citas)
                if id not in diccionario_citas:
                        diccionario_citas[id] = {
                            'id': id,
                            'tipo_bicicleta': bicicleta,
                            'fecha': fecha,
                            'usuario':usuario
                        }
                id = id+1
                graba_diccionario_id(diccionario_citas,'id',archivo_citas)
                confirmacion = True
            return render_template("index.html", confi = confirmacion)

@app.route("/lista_citas/", methods=['GET'])
def lista_citas():
    if request.method == 'GET':
        dic_citas = lee_diccionario_csv_id(archivo_citas)
        return render_template("lista_citas_users.html",dicc_citas=dic_citas)




@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")       




#@app.route("/pdf/", methods=['GET'])
#def pedefe():
 
#    return render_pdf(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)
    session['logged_in'] = False