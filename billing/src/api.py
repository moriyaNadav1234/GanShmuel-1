from src import app
from flask import request
import json
import mysql.connector


mydb = mysql.connector.connect(
    host="billingDB",
    user="root",
    password="catty",
    database="billdb"
)

@app.route("/health")
def index():
    return "OK"

@app.route('/provider',methods=['POST'])
def Insert_provider():
    mycursor = mydb.cursor()
    #TODO: Error handling(Empty strings,invalid names and such)
    sql = "INSERT INTO Provider (id,name) VALUES (%s,%s)"
    val = ('9',request.form['name'])
    mycursor.execute(sql, val)

    mydb.commit()

    return "record inserted"

@app.route('/provider/<id>',methods=['PUT'])
def Update_provider(id):
    mycursor = mydb.cursor()
    #TODO: Error handling(Empty strings,invalid names and such)
    sql = "UPDATE Provider SET name=%s WHERE id=%s"
    val = (request.form['name'],id)

    mycursor.execute(sql,val)
    mydb.commit()
    return "OK"

@app.route('/truck',methods=['POST'])
def Insert_truck():
    mycursor = mydb.cursor()

    sql = "INSERT INTO Trucks (id,provider_id) VALUES (%s,%s)"
    val = (request.form['provider'],request.form['id'])

    mycursor.execute(sql,val)
    mydb.commit()
    return "OK"