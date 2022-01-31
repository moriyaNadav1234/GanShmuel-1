from flask import Flask, request, json
import app, process
import subprocess

@app.route("/webhook", methods=['POST'])
def process():
    data = json.loads(request.data)
    process.getCodeFromGitHub() # git clone
    process.dockerBuild_Billig()
    process.dockerBuild_Weight()
    process.productionDeploy_Weight()
    process.productionDeploy_Billing()

    #!!!main will call functions from process.py! this part will be depreciated.
    # Call bash script to process for git trigger
    # subprocess.check_call("./process.sh '%s'" % data['ref'], shell=True)
    # commits = json.dumps(data['commits'])

    return data['ref']