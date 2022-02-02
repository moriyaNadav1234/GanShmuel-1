from flask import Flask
from flask import request, json
import process
import constants

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    data = json.loads(request.data) 
    
    # fetch branch name form data['ref']
    branchName = data['ref'].split("/")[-1]

    success, firstCopy = process.firstCopy()
    if not success: return False

    if not firstCopy:
        process.getCodeFromGitHub()  # git clone
        if not success: return False
    
    if branchName == 'biling': branchName = 'billing' # location == branch (branch name fix)

    #if branch not main do only test
        #process.buildtest
        #process.deploytest
        #ans =test.runtest
        #if ans ok send mail

    if branchName == "billing" or branchName == "weight":

        process.dockerBuild(branchName)
        if not success: return False

        process.dockerDeploy(branchName,'test')
        if not success: return False

        process.testingDeploy(branchName)
        if not success: return False

    #if branch main test and deploy
        #process.buildtest
        #process.deploytest
        #ans =test.runtest
        #if ans ok send mail
        #if test ok deploy production

    elif branchName == "main":

        # build, deploy and test weight
        process.dockerBuild("weight")
        if not success: return False

        process.dockerDeploy("weight",'test')
        if not success: return False

        process.testingDeploy("weight")
        if not success: return False


        # build, deploy and test billing
        process.dockerBuild("billing")
        if not success: return False

        process.dockerDeploy("billing",'test')
        if not success: return False

        process.testingDeploy("billing")
        if not success: return False


        # deploy to production
        process.dockerDeploy("weight",'production')
        if not success: return False
        
        process.dockerDeploy("billing",'production')
        if not success: return False

    return data['ref']

       
if __name__ == '__main__':
    app.run(host=constants.HOST, port=constants.PORT, debug=constants.TEST)
    # debug=True only in test. should be off in prod!