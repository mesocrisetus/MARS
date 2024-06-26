from flask import Flask, render_template, request, redirect,url_for,flash,session,g
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_mysqldb import MySQL
import os
import db_modulos as db_m
import database as db



# Ruta para guardar las fotos

UPLOAD_FOLDER = 'static/profile_pics'
ALLOWED_EXTENSIONS = {'jpg'}

# APP CONFIG
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Clave secreta para el correcto funcionamiento de la APP
app.secret_key = os.urandom(24)



 


######################################################## FORMULARIO ########################################################

# Ruta para iniciar sesion - Ruta por defecto
@app.route('/')
def home():
    return render_template('form.html')

# Ruta LOGIN
@app.route('/login', methods=['POST'])
def login():
    
    # Se cambia el estado del user a None
    session.pop('user',None)
    
    # Solicitud de usuario y contrase;a 
    user = request.form['user']
    password = request.form['password']    
    login = db_m.login(user,password)    
    if login:
        # Se cambia el user de la sesion por el user actual
        session['user'] = user                  
        return redirect(url_for('index',user=user))
    else:
        pass   
    message = 'Usuario o password incorrectos'    
    flash(message)    
    return render_template('form.html')

# Definir la sesion de usuario
@app.before_request
def before_request():
    g.user = None    
    if 'user' in session:
        g.user=session['user']
        
    
    

###########################################################################################################################

######################################################## REGISTRO ########################################################
# Registrarse
@app.route('/registro')
def registro():    
    return render_template('form.html')

@app.route('/registrar',methods=['POST'])
def registrar():
    user = request.form['_user']
    password = request.form['_password']    
    registrar = db_m.registrar(user,password)
    message = 'Registro exitoso'    
    flash(message)    
    return redirect('/')

###########################################################################################################################

######################################################## INDEX ############################################################
# Ruta index 
@app.route('/index/<user>')
def index(user):
    # Valida si hay una sesion de usuario activa
    if g.user:
        pic_name = user + '.jpg'    
        pic = '/static/profile_pics/' + pic_name    
        users = db_m.obtener_users()
        cursor = db.database.cursor()
        sql = "SELECT * FROM post"
        cursor.execute(sql)
        result = cursor.fetchall()
        result = result[::-1]  # Invertir el orden de los resultados       
        cursor.close()            
        return render_template('index.html',username = session['user'], posts=result,pic=pic,users = users,user={0}).format(user)
    # Si no se encuentra una sesion activa, nos regresara al formulario
    else:
        return render_template('form.html')

###########################################################################################################################


######################################################## POST ############################################################


# Publicar un POST

@app.route('/publicar', methods=['POST'])
def publicar():     
    text = request.form['text']
    user = request.form['_user']
    db_m.publicar(text,user)
    return redirect(url_for('index',user=user))
    
    
###########################################################################################################################


######################################################## PERFIL ############################################################
# Ruta perfil

@app.route('/profile/<user>')
def profile(user):
    if g.user:
        pic_name = user + '.jpg'
        pic = '/static/profile_pics/' + pic_name    
        return render_template('profile.html',pic = pic,user={0}).format(user)
    
    # Si no se encuentra una sesion activa, nos regresara al formulario
    else:
        return render_template('form.html')


# Subir una foto de perfil
@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    if request.method =='POST':
        f = request.files['file']
        user = request.form['username']
        pic_name = request.form['username'] + '.jpg'
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],pic_name))
        message = 'Se ha subido la foto de perfil'    
        flash(message)
        pic = '/static/profile_pics/' + pic_name
        return redirect(url_for('profile',user=user, pic = pic))
    
###########################################################################################################################

######################################################## FAQ ############################################################
# Ruta FAQ

@app.route('/faq/<user>')
def faq(user):
    if g.user:
        pic_name = user + '.jpg'
        pic = '/static/profile_pics/' + pic_name    
        return render_template('faq.html',pic = pic,user=user)
    else:
        return render_template('form.html')

###########################################################################################################################

######################################################## CERRAR SESION ############################################################

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect("/")

###########################################################################################################################

if __name__ == '__main__':
    app.run(debug=True) 
