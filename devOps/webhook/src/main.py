from flask import Flask
from flask import request, json
import process
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

    process.getCodeFromGitHub()  # git clone
    process.dockerBuild_Billing() 
    process.dockerBuild_Weight()
    process.productionDeploy_Weight() 
    process.productionDeploy_Billing()

    # !!!main will call functions from process.py! this part will be depreciated.
    # Call bash script to process for git trigger
    # subprocess.check_call("./process.sh '%s'" % data['ref'], shell=True)
    # commits = json.dumps(data['commits'])

    return data['ref']


if __name__ == '__main__':
    app.run(host=constants.HOST, port=constants.PORT, debug=constants.TEST)
    # debug=True only in test. should be off in prod!


def get_code():
    print('getcode')


def build():
    print('build')


def test():
    print('test')


def deploy():
    print('deploy')


def send_mail():
    list_admin = ['admin@mydomain.com']
    if not app.debug:
        import logging
        from logging.handlers import SMTPHandler
        mail_handler = SMTPHandler(mailhost=('smtpout.secureserver.net', 25),
                                   fromaddr='admin@mydomain.com',
                                   toaddrs=list_admin, subject='YourApplication Failed',
                                   credentials=('admin@mydomain.com', 'mypassword'))
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
