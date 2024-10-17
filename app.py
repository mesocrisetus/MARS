from flask import Flask, render_template, request, redirect,url_for,flash,session,g
import os
import db_modulos as db_m
import sqlite3


# Ruta para guardar las fotos

UPLOAD_FOLDER = 'static/profile_pics'
ALLOWED_EXTENSIONS = {'jpg'}

# APP CONFIG
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Clave secreta para el correcto funcionamiento de la APP
app.secret_key = os.urandom(24)





# Area formulario

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
        
    
    

# Area registro

# Registrarse
@app.route('/registro')
def registro():    
    return render_template('form.html')

@app.route('/registrar',methods=['POST'])
def registrar():
    user = request.form['_user']
    password = request.form['_password']    
    db_m.registrar(user,password)
    message = 'Registro exitoso'    
    flash(message)    
    return redirect('/')

# Area index

# Ruta index 
@app.route('/index/<user>')
def index(user):
    # Valida si hay una sesion de usuario activa
    if g.user:

        #Cargar la foto de perfil
        connection = sqlite3.connect("Sqldatabase/mars.db")
        cursor = connection.cursor()    
        sql = "SELECT * FROM users WHERE user='%s'"%user
        cursor.execute(sql)
        connection.commit()
        pic_name =  cursor.fetchall()
        for row in pic_name:
            pic_name = row[4]
        
        print(pic_name)
        pic= '/static/profile_pics/' +  pic_name

        
        #cargar posts
        users = db_m.obtener_users()
        
        connection = sqlite3.connect("Sqldatabase/mars.db")
        cursor = connection.cursor()        

        sql = "SELECT * FROM post"
        cursor.execute(sql)
        connection.commit()


        result = cursor.fetchall()
        result = result[::-1]  # Invertir el orden de los resultados       
        cursor.close()            
        return render_template('index.html',username = session['user'], posts=result,pic=pic,users = users,user={0}).format(user)
    # Si no se encuentra una sesion activa, nos regresara al formulario
    else:
        return render_template('form.html')



# Area post

# Publicar un POST

@app.route('/publicar', methods=['POST'])
def publicar():     
    text = request.form['text']
    user = request.form['_user']
    db_m.publicar(text,user)
    return redirect(url_for('index',user=user))
    
    

# Area perfil


# Ruta perfil

@app.route('/profile/<user>')
def profile(user):
    if g.user:
        #Cargar la foto de perfil
        connection = sqlite3.connect("Sqldatabase/mars.db")
        cursor = connection.cursor()    
        sql = "SELECT * FROM users WHERE user='%s'"%user
        cursor.execute(sql)
        connection.commit()
        pic_name =  cursor.fetchall()
        for row in pic_name:
            pic_name = row[4]
        
        print(pic_name)
        pic= '/static/profile_pics/' +  pic_name

        #panel de admin
        connection = sqlite3.connect("Sqldatabase/mars.db")
        cursor = connection.cursor()    
        sql = "SELECT * FROM users WHERE user='%s'"%user
        cursor.execute(sql)
        connection.commit()
        root=0
        root_or_not =  cursor.fetchall()
        for row in root_or_not:
            root = row[5]
        
        if root == 1:    
            #cargar posts
            users = db_m.obtener_users()
            connection = sqlite3.connect("Sqldatabase/mars.db")
            cursor = connection.cursor()
            sql = "SELECT * FROM post"
            cursor.execute(sql)
            connection.commit()

            result = cursor.fetchall()
            print(result)
            
            result = result[::-1]  # Invertir el orden de los resultados       
            cursor.close()            
            connection.close()
            print(result)
            # retornar el perfil root
            return render_template('profile.html',pic = pic,user={0},posts=result,users = users).format(user)
        else:
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

        #subir la foto
        pic_name = request.form['username'] + '.jpg'
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],pic_name))


        #Actualizar la foto en la BD

        connection = sqlite3.connect("Sqldatabase/mars.db")
        cursor = connection.cursor()    
        sql = "UPDATE users SET pic_name='%s' WHERE user='%s'"%(pic_name,user)           
        cursor.execute(sql)
        connection.commit()

        pic = '/static/profile_pics/' + pic_name

        message = 'Se ha subido la foto de perfil'    
        flash(message)
        
        return redirect(url_for('profile',user=user, pic = pic))


# Borrar un post
@app.route('/delete_post', methods = ['GET', 'POST'])
def delete_post():
    if request.method =='POST':
        adminName= request.form['adminName']
        user = request.form['username']
        post_id  =request.form['post_id']

        connection = sqlite3.connect("Sqldatabase/mars.db")
        cursor = connection.cursor()    
        sql = "DELETE FROM post WHERE id='%s'"%(post_id)           
        cursor.execute(sql)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for('profile',user=adminName))


# Area FAQ


# Ruta FAQ

@app.route('/faq/<user>')
def faq(user):
    if g.user:
        pic_name = user + '.jpg'
        pic = '/static/profile_pics/' + pic_name    
        return render_template('faq.html',pic = pic,user=user)
    else:
        return render_template('form.html')


#Area cerrar sesion

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect("/")


# Main

if __name__ == '__main__':
    app.run(debug=True) 
