from flask import Flask
import subprocess


app = Flask(__name__)


# results = subprocess.run(
#     '''ls -laF''', shell=True, universal_newlines=True, check=True)
# print(results.stdout)

subprocess.run('''docker -f billing/dockerfile''', shell=True)



subprocess.run('''docker-compose -f billing/docker-compose.yml up''', shell=True)
# subprocess.run('''docker-compose -f weight/docker-compose.yml up''', shell=True)




@app.route("/webhook", methods=['POST'])
def process():
    data = json.loads(request.data)

    # Call bash script to process for git trigger
    subprocess.check_call("./process.sh '%s'" % data['ref'], shell=True)

    # commits = json.dumps(data['commits'])
    return data['ref']



if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8080,debug=True)



למה צריך פלאסק?
