from flask import Flask, request, json
import subprocess

app = Flask(__name__)


@app.route("/webhook", methods=['POST'])
def process():
    data = json.loads(request.data)

    # Call bash script to process for git trigger
    subprocess.check_call("./process.sh '%s'" % data['ref'], shell=True)

    # commits = json.dumps(data['commits'])
    return data['ref']


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8086 ,  debug=True)
