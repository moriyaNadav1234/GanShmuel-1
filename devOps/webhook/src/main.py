from flask import Flask
from flask import request, json
from process import *
import constants

# TODO: fix error
# Error: While importing 'main', an ImportError was raised.
# import process

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    data = json.loads(request.data)

    # TODO: fix error
    # Error: While importing 'main', an ImportError was raised.

    getCodeFromGitHub()  # git clone
    dockerBuild_Billig()
    dockerBuild_Weight()
    productionDeploy_Weight()
    productionDeploy_Billing()

    # !!!main will call functions from process.py! this part will be depreciated.
    # Call bash script to process for git trigger
    # subprocess.check_call("./process.sh '%s'" % data['ref'], shell=True)
    # commits = json.dumps(data['commits'])

    return data['ref']


if __name__ == '__main__':
    app.run(host=constants.HOST, port=constants.PORT, debug=constants.TEST)
    # debug=True only in test. should be off in prod!
