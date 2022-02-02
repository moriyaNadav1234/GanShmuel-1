from crypt import methods
from email import header
import re
from flask import Flask ,request
import mysql.connector, json,csv
from datetime import datetime
import os

app = Flask(__name__)

#conncet to DB
def dbConnection():
    try:
        mydb = mysql.connector.connect(
        host="weightMySql",
        port='3306',
        database="weight",
        user="root",
        password="1234"
        )
        return mydb
    except:
        return "connection to DB failed 500",500

@app.route('/health')
def health():
    dbConnection()
    return 'ok 200',200

@app.route('/item/<id>')
def item(id):
    #default vals
    From = "1st of month at 000000"
    To = "now"
    item=""

    #making sure user specefied if he want's truck or container
    if request.args.get('item') =="truck" or request.args.get('item') =="container":
        item=request.args.get('item')
    else:
        return "404 please specify in the URL item=container/truck",404

    #checking if values were sent
    if not request.args.get('from') == None and not request.args.get('from') =="":
        From=request.args.get('from') 
    if not request.args.get('to') == None and not request.args.get('to') =="":
        To=request.args.get('to')

    #converting the string into date in the right format.
    if From=="1st of month at 000000":
        fromTime = datetime.now().strftime("%Y-%m-1 00:00:00")
    else:
        try:
            fromTime=datetime.strptime(From,"%Y-%m-%d %H:%M:%S")
        except:
            return "invalid from time, please make sure to use the YYYY-MM-DD HH:MM:SS format"
    if To=="now":
        toTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        try:
            toTime=datetime.strptime(To,"%Y-%m-%d %H:%M:%S")
        except:
            return "invalid to time, please make sure to use the YYYY-MM-DD HH:MM:SS format"

    #conncet to DB
    mydb = dbConnection()
    #used to send queries
    mycursor = mydb.cursor()

    #trenary condition based on if user is asking for container or a truck
    query = f"SELECT truck,truckTara,id FROM transactions where truck = '{id}' and datetime between '{fromTime}' and '{toTime}'" if item=="truck" else f"SELECT id FROM transactions where containers like '%{id}%'"
    mycursor.execute(query)
    queryresult = mycursor.fetchall()

    transactions=[]
    #iterating the results and converting them to json, appending then into a list
    if request.args.get('item') =="truck": 
        for row in queryresult:
            transactions.append(row[2])
            truckTara=row[1]
            
        jsonFile=json.dumps({
        "truck":id, 
        "truckTara":truckTara,
        "transactions":transactions})
    else:
        for row in queryresult:
            transactions.append(row[0])
        
        mycursor.execute(f"SELECT weight FROM containers_registered where container_id = '{id}'")
        queryresult = mycursor.fetchall()
        jsonFile=json.dumps({
        "container_id":id, 
        "weight":queryresult[0][0],
        "transactions":transactions})

    return str(jsonFile)


@app.route('/unknown') 
def unknown():
    
    #conncet to DB
    mydb = dbConnection()

    #used to send queries
    mycursor = mydb.cursor()
    mycursor.execute("SELECT container_id FROM containers_registered WHERE weight IS NULL")
    queryres = mycursor.fetchall()
    unknownList=[]
    for row in queryres:
        unknownList.append(str(row[0]))

    return str(unknownList)


@app.route('/weight',methods=['GET','POST'])
def weight():

    #default vals
    From = "today at 000000"
    To = "now"
    filter = "in,out,none"

    #conncet to DB
    mydb = dbConnection()
    #used to send queries
    mycursor = mydb.cursor()

    if request.method == 'GET':

        #fetch vals from url
        if not request.args.get('from') == None and not request.args.get('from') =="":
                From=request.args.get('from') 
        if not request.args.get('to') == None and not request.args.get('to') =="":
                To=request.args.get('to') 
        if not request.args.get('filter') == None and not request.args.get('filter') =="":
                filter=request.args.get('filter')

        #converting the string into date in the right format.    
        if From=="today at 000000":
            fromTime = datetime.now().strftime("%Y-%m-%d 00:00:00")
        else:
            try:
                fromTime=datetime.strptime(From,"%Y-%m-%d %H:%M:%S")
            except:
                return "invalid from time, please make sure to use the YYYY-MM-DD HH:MM:SS format"
        if To=="now":
            toTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            try:
                toTime=datetime.strptime(To,"%Y-%m-%d %H:%M:%S")
            except:
                return "invalid to time, please make sure to use the YYYY-MM-DD HH:MM:SS format"
            
            #query everything from the table
            mycursor.execute(f"SELECT * FROM transactions where direction = '{filter}' and datetime between '{fromTime}' and '{toTime}'")
            queryresult = mycursor.fetchall()
            jsonList=[]
            #iterating the results and converting them to json, appending then into a list
            for row in queryresult:
                jsonList.append(json.dumps({"id":row[0],
                "datetime":str(row[1]),
                "direction":row[2],
                "truck":row[3],
                "containers":row[4],
                "bruto":row[5],
                "truckTara":row[6],
                "neto":row[7],
                "produce":row[8]}))
            return str(jsonList)

    else:
        parms={"direction":None, #string in/out/None
        "truck":None, #string
        "containers":None, #list of string
        "weight":None, #int =>0
        "unit":None, #string
        "force":None, #bool True/Flse
        "produce":None} #string
        
        for i in request.args.items():
            if not i[0] in parms:
                return f"{i[0]} isn't a legal value, values you need to send are: direction,truck,containers,weight,unit,force,produce", 400
            # if i[0]=="weight" and i[1]<0 or i[0]=="force" and not isinstance(i[1], bool) or i[0]=="direction" and not i[1]=="in" and not i[1]=="out":
            #     return "make sure to insert into weight 0 or more, force to be True or False and direction to be in/out or keep it empty for None",400
            
            if not i[0]=="":
                parms[i[0]]=i[1]
            # else:
            #    parms[i[0]]=None 

        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return str(parms) #TODO: make post 

    return "this is not working, contact the local zoo for help" #TODO: test only use: return 'this is route weight'


    
@app.route('/session/<id>')
def session(id):
    
    #connecting to DB
    mydb = dbConnection()
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT truck,bruto,truckTara,neto FROM transactions where id = '{id}'")
    queryresult = mycursor.fetchall()
    
    #if query is empty returning 404
    if mycursor.rowcount == 0:
        return "404 non-existent", 404
    else:
        jasonList=[]
        for row in queryresult:
            jasonList.append(json.dumps({
            "id": id,
            "truck":row[0],
            "bruto":row[1],
            "truckTara":row[2],
            "neto":row[3]}))

        return str(jasonList)

@app.route('/batch-weight',methods=['POST'])
def batch():
     
    mydb=dbConnection()
    if not request.args.get('file') == None and not request.args.get('file') =="":
        file_name=request.args.get('file')
        if not file_name.endswith('.csv') and not file_name.endswith('.json'):
            return "please make sure the file type is csv or json"    
    else:
        return "please enter file name"
    
    try: #trying to open the file
        a=os.path.dirname(os.path.abspath(__file__))
        path=a+f"/in/{file_name}"
        f=open(path, 'r')
        
    except: 
        return "file is not readable"

    if file_name.endswith('.json'):#if the file type is json
        json_data = json.load(f)       
        for row in json_data:
            if row['weight'] == '':
                row['weight']=None
        mycursor = mydb.cursor()
        query = "INSERT INTO containers_registered (container_id,weight,unit) VALUES (%s,%s,%s);"     
        for item in json_data:   
            try:            
                 mycursor.execute(query, [item['id'],item['weight'],item['unit']])
            except:
                return "data is allready exists"
        mydb.commit() 
        f.close()
        return "data intered successfully"

    if file_name.endswith('.csv'):
        csvreader = csv.reader(f)
        header = next(csvreader) 
        unit = str(header[1])       
        jsonList = []
        row1=""        
        for row in csvreader:
            if row[1] == "":# checking if a wieght in the file is empty
               row1=None
            else:
                row1 = row[1]    
            jsonList.append({
            "id":row[0],
            "weight":row1,
            "unit": unit
            })
        mycursor = mydb.cursor()
        query = "INSERT INTO containers_registered (container_id,weight,unit) VALUES (%s,%s,%s);"      
        for item in jsonList:     
            try:                  
                mycursor.execute(query, [item['id'],item['weight'],item['unit']])   
            except:
                 return "data is allready exists"        
        mydb.commit()
        f.close() 
        return "data intered successfully" 
        

@app.route('/')
def home():
    return 'this will be a home page'


if __name__=="__main__":
    app.run()