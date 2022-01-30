from flask import Flask, request

app = Flask(__name__)


@app.route("/webhook", methods=['POST'])
def process():
    json = request.json
    print(json['ref'])
    return 1


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
