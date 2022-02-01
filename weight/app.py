from flask import Flask ,request
import mysql.connector
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
        user="root",
        port="3306",
        password="1234",
        database = "weight"
        )
        #used to send queries
        mycursor = mydb.cursor()
        if request.method=='GET':
            #fetch vals from url
            #TODO: check if vals were sent ******************** TODO TODO
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
            
            #TODO: query to get all transactions by the vals from URL
            #####mycursor.execute(f"SELECT * FROM transactions where direction = {filter} and datetime between {fromTime} and {toTime}")
            #TODO: itareate the query result into a arry of json object 

            #TODO: return the JSON objects

    except:
        return "connection to database failed 500"
    
    mycursor.execute("SELECT * FROM transactions where direction = '{From}' and datetime between '{From}' and '{To}'")
    myresult = mycursor.fetchall()
    y = []
    for x in myresult:
        y.append(x)
    return y #TODO: test only use: return 'this is route weight'

@app.route('/')
def hello():
    return 'Hello, World!'


if __name__=="__main__":
    app.run(debug=True)