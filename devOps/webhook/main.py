from flask import Flask, request, json
import subprocess

app = Flask(__name__)


@app.route("/webhook", methods=['POST'])
def process():
    data = json.loads(request.data)

    # Call bash script to process for git trigger
    subprocess.call("/home/ec2-user/app/process.sh")

    # ref = data['ref']
    # commits = json.dumps(data['commits'])
    # return commits
    return data['ref']


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
