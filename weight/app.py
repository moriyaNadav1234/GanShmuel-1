from flask import Flask ,request
import mysql.connector, json
from datetime import datetime



app = Flask(__name__)

@app.route('/health')
def health():
    return 'ok 200'

@app.route('/weight',methods=['GET','POST'])
def weight():

    #default vals
    From = "today at 000000"
    To = "now"
    filter = "in,out,none"
    try:
        #conncet to DB
        mydb = mysql.connector.connect(
        host="weightMySql",
        port='3306',
        database="weight",
        user="root",
        password="1234"
        )

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
            jasonList=[]
            #iterating the results and converting them to json, appending then into a list
            for row in queryresult:
                jasonList.append(json.dumps({"id":row[0],
                "datetime":str(row[1]),
                "direction":row[2],
                "truck":row[3],
                "containers":row[4],
                "bruto":row[5],
                "truckTara":row[6],
                "neto":row[7],
                "produce":row[8]}))

            #TODO: make sure if we have to return as a string :((((
            return str(jasonList)

    except:
        return "connection to database failed 500"

    # mycursor.execute(f"SELECT * FROM transactions where direction = '{filter}' and datetime between '{fromTime}' and '{toTime}'")
    # queryresult = mycursor.fetchall()
    # jasonList=[]
    # for row in queryresult:
    #     jasonList.append(json.dumps({"id":row[0],
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