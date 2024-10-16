import database as db
import sqliteDatabaseConection as sqLite


def login(user,password):
    cursor = db.database.cursor()
    sql = "SELECT user,password FROM users WHERE user='%s' AND password='%s'"%(user,password)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()    
    return result


def registrar(user,password):
    cursor = db.database.cursor()
    sql = "INSERT INTO users (user,password) VALUES ('%s','%s')"%(user,password)
    sql2 = "SELECT id FROM users WHERE user='%s'"%(user)        
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.execute(sql2)
    result2 = cursor.fetchall()
    p_id = result2[0]
    sql3 = "UPDATE users SET p_id=%s WHERE user='%s'"%(p_id[0],user)
    cursor.execute(sql3)        
    cursor.close()
    return result

def obtener_users():
    cursor = db.database.cursor()
    sql = "SELECT * FROM users"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

# PUBLICAR UN POST     
def publicar(text,user):
    cursor = db.database.cursor()
    sql = "INSERT INTO post (descrp,p_username) VALUES ('%s','%s')"%(text,user)           
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
        
# Subir una pic

def upload(pic,user):
    cursor = db.database.cursor()
    sql = "UPDATE users SET pic='%s' WHERE user='%s'"%(pic,user)           
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
        
