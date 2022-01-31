from src import app
from flask import request
from enum import Enum
import json
import mysql.connector


class LOG_TYPE(Enum):
    INFO=0
    ERROR=1
    WARNING=2

type_desc = ["[INFO]","[ERROR]","[WARNING]"]

def LOG(str,TYPE):
    with open("log","a+") as f:
        f.write(f'{type_desc[TYPE.value]} {str}\n')


def connect():
    mydb=None
    LOG("Connecting to Database...",LOG_TYPE.INFO)
    
    try:
        mydb = mysql.connector.connect(
            host="billingDB",
            user="root",
            password="catty",
            database="billdb"
        )
    except:
        LOG("Connection failed!",LOG_TYPE.ERROR)
        return None

    LOG("Connection successful!",LOG_TYPE.INFO)
    return mydb

@app.route("/health")
def health():
    return "OK"

@app.route("/db_health")
def db_health():
    return ("BAD" if connect() == None else "OK")

@app.route('/provider',methods=['POST'])
def Insert_provider():

    if request.form['name'] == None or len(request.form['name']) == 0:
        LOG("Invalid data provided! Cannot insert into Provider table",LOG_TYPE.ERROR)
        return "BAD"
    
    #Open connection to the database
    db = connect()
    if db == None:
        return "BAD"

    LOG("Inserting into Provider table...",LOG_TYPE.INFO)

    try:
        mycursor = db.cursor()
        #Query SQL
        sql = 'INSERT INTO Provider(name) VALUES(%s)'
        val = (request.form['name'],)
        
        mycursor.execute(sql,val)
        
        db.commit()#Commit changes of the SQL Query

        LOG("Inserted new record into Provider table",LOG_TYPE.INFO)

        return json.dumps({'id':mycursor.lastrowid}), 200, {'ContentType':'application/json'}
    except ValueError:
        LOG("Failed to insert data into Provider Table",LOG_TYPE.ERROR)
    finally:
        LOG("Closing connection to database...",LOG_TYPE.INFO)
        db.close()#Close connection

    return "BAD"


@app.route('/provider/<id>',methods=['PUT'])
def Update_provider(id):

    if request.form['name'] == None or len(request.form['name']) == 0:
        LOG("Invalid data provided! Cannot Update Provider table",LOG_TYPE.ERROR)
        return "BAD"
    
    #Open connection to the database
    db = connect()
    if db == None:
        return "BAD"

    try:
        mycursor = db.cursor()
        
        sql = "UPDATE Provider SET name=%s WHERE id=%s"
        val = (request.form['name'],id)

        mycursor.execute(sql,val)
        db.commit()

        LOG("Updated Provider table successfully!",LOG_TYPE.INFO)

        return "OK"
    except:
        LOG("Failed to Update Provider table",LOG_TYPE.ERROR)
        pass
    finally:
        LOG("Closing connection to database...",LOG_TYPE.INFO)
        db.close()
    
    return "BAD"

@app.route('/truck',methods=['POST'])
def Insert_truck():

    #Open connection to the database
    db = connect()
    if db == None:
        return "BAD"

    try:
        mycursor = db.cursor()
        sql = "INSERT INTO Trucks (id,provider_id) VALUES (%s,%s)"
        val = (request.form['id'],request.form['provider'])
        
        mycursor.execute(sql,val)
        db.commit()

        LOG("Inserted new record into Trucks table successfully!",LOG_TYPE.INFO)

        return "OK"
    except:
        LOG("Failed to insert new record into Trucks table",LOG_TYPE.ERROR)
        pass
    finally:
        LOG("Closing connection to database...",LOG_TYPE.INFO)
        db.close()

    return "BAD"

@app.route("/truck/<id>",methods=['PUT'])
def Update_ProviderID(id):

    #Open connection to the database
    db = connect()
    if db == None:
        return "BAD"
    
    try:
        mycursor = db.cursor()
        
        sql = "UPDATE Trucks SET provider_id=%s WHERE id=%s"
        val = (request.form['provider_id'],id)

        mycursor.execute(sql,val)
        db.commit()

        LOG("Updated Trucks table Column[provider_id] successfully!",LOG_TYPE.INFO)

        return "OK"
    except:
        LOG("Failed to Update Trucks table",LOG_TYPE.ERROR)
        pass
    finally:
        LOG("Closing connection to database...",LOG_TYPE.INFO)
        db.close()
    
    return "OK"