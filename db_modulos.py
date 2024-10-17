import database as db
import sqlite3




def login(user,password):
    connection = sqlite3.connect("Sqldatabase/mars.db")
    cursor = connection.cursor()
    sql = "SELECT user,password FROM users WHERE user='%s' AND password='%s'"%(user,password)
    cursor.execute(sql)
    connection.commit()
    result = cursor.fetchall()
    cursor.close()    
    connection.close()
    return result


def registrar(user,password):
    connection = sqlite3.connect("Sqldatabase/mars.db")
    cursor = connection.cursor()
    try:

        # Insertar el nuevo usuario
        sql = "INSERT INTO users (user,password,pic_name) VALUES ('%s','%s','default.webp')"%(user,password)
        cursor.execute(sql)
        # Guarda los cambios
        connection.commit()

        # Obtiene el id del usuario insertado
        sql2 = "SELECT id FROM users WHERE user='%s'"%(user)                
        cursor.execute(sql2, (user,))
        result2 = cursor.fetchall()

        # asignar el p_id
        if result2:
            p_id = result2[0]
            sql3 = "UPDATE users SET p_id=%s WHERE user='%s'"%(p_id[0],user)
            cursor.execute(sql3)        
            connection.commit()
        
        
    except sqlite3.Error as e:
        print("Error en la operacion:",e)    
    cursor.close()
    connection.close()
        

def obtener_users():
    connection = sqlite3.connect("Sqldatabase/mars.db")
    cursor = connection.cursor()

    sql = "SELECT * FROM users"
    cursor.execute(sql)

    result = cursor.fetchall()
    cursor.close()
    connection.close()

    return result

# PUBLICAR UN POST     
def publicar(text,user):
    connection = sqlite3.connect("Sqldatabase/mars.db")
    cursor = connection.cursor()

    try: 
        sql = "INSERT INTO post (descrp,p_username) VALUES ('%s','%s')"%(text,user)           
        cursor.execute(sql)
        connection.commit()
    except sqlite3.Error as e:
        print("Error en la operacion: ",e)
    
    cursor.close()
    connection.close()
    
        
# Subir una pic

def upload(pic,user):
    connection = sqlite3.connect("Sqldatabase/mars.db")
    cursor = connection.cursor()

    try:
        sql = "UPDATE users SET pic='%s' WHERE user='%s'"%(pic,user)           
        cursor.execute(sql)
        connection.commit()
    except sqlite3.Error as e:
        print("Error en la operacion: ",e)
    

    cursor.close()
    connection.close()
        
