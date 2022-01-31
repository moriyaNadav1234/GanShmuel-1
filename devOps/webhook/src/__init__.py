from flask import Flask
import constants

app = Flask(__name__)

if __name__ == '__main__':
    app.run(host=constants.HOST, port=constants.PORT , debug=constants.TEST)
    #debug=True only in test. should be off in prod!
