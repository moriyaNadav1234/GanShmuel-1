from flask import Flask ,request
import mysql.connector, json
from datetime import datetime

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
    return 'ok 200',200

@app.route('/item/<id>')
def item(id):
    #default vals
    From = "1st of month at 000000"
    To = "now"
    item=""
    if request.args.get('item') =="truck" or request.args.get('item') =="container":
        item=request.args.get('item')
    else:
        return "404 please specify in the URL item=container/truck",404

    #checking if values were sent
    if not request.args.get('from') == None and not request.args.get('from') =="":
        From=request.args.get('from') 
    if not request.args.get('to') == None and not request.args.get('to') =="":
        To=request.args.get('to')

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

@app.route('/weight',methods=['GET','POST'])
def weight():

    #default vals
    From = "today at 000000"
    To = "now"
    filter = "in,out,none"
    try: #TODO: delete this try, moved the connection to a function
        #conncet to DB
        mydb = dbConnection()
        #used to send queries
        mycursor = mydb.cursor()

        if request.method=='GET':
            #fetch vals from url
            if not request.args.get('from') == None and not request.args.get('from') =="":
                From=request.args.get('from') 
            if not request.args.get('to') == None and not request.args.get('to') =="":
                To=request.args.get('to') 
            if not request.args.get('filter') == None and not request.args.get('filter') =="":
                filter=request.args.get('filter')
            
            if From=="today at 000000":
                fromTime = datetime.now().strftime("%Y-%m-%d 00:00:00")
            else:
                try:
                    #TODO: make sure the from time have passed, if it's in the future cry.
                    fromTime=datetime.strptime(From,"%Y-%m-%d %H:%M:%S")
                except:
                    return "invalid from time, please make sure to use the YYYY-MM-DD HH:MM:SS format"

            if To=="now":
                toTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                try:
                    #TODO: make sure the from time have passed, if it's in the future cry.
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
            #TODO: check if all the needed parms (all the parms in the table except id)
            #TODO: insert the correct data into dict/vals
            #TODO: execute to the insert quetry
            #TODO: 
            return "TODO"
    except:
        return "connection to database failed 500"

    # mycursor.execute(f"SELECT * FROM transactions where direction = '{filter}' and datetime between '{fromTime}' and '{toTime}'")
    # queryresult = mycursor.fetchall()
    # jsonList=[]
    # for row in queryresult:
    #     jsonList.append(json.dumps({"id":row[0],
    #     "datetime":str(row[1]),
    #     "direction":row[2],
    #     "truck":row[3],
    #     "containers":row[4],
    #     "bruto":row[5],
    #     "truckTara":row[6],
    #     "neto":row[7],
    #     "produce":row[8]})) 
    #y=list(myresult)
    # for x in myresult:
    #     y.append(str(x))
    return "this is not working contact the local zoo for help" #TODO: test only use: return 'this is route weight'

@app.route('/')
def home():
    return 'this will be a home page'


if __name__=="__main__":
    app.run()