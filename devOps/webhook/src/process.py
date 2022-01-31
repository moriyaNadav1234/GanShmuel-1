import subprocess, os
import app, constants
from mailingService import mail_Service
from git import Repo
import datetime



def getCodeFromGitHub():
    #git clone git@github.com:develeapDorZ/GanShmuel.git
    #if fail - notify devOps Team
    try:
        repo.clone(os.path.join(constants.gitHubURL, constants.deployDirectory))
        mail_Service.mailNotification('updateRepo', 'devops', True)
        mail_Service.sendErrorToLog('repo_log.txt','success','repo update')
    except:
        mail_Service.sendErrorToLog('repo_log.txt','failed','repo update')
        mail_Service.mailNotification('updateRepo', 'devops', False)

def dockerBuild_Weight():
    # docker compose - weight
    # if fail- fail email
    # if success - success email
    # mail notificaiton for devOps & Weight Team
    try:
        subprocess.run("docker-compose -f /app/GanShmuel/billing/docker-compose.yml build", shell=True, check=True)
        mail_Service.mailNotification('build', 'weight', True)
        mail_Service.sendErrorToLog('weight_team_log.txt','success','build')
    except:
        mail_Service.sendErrorToLog('weight_team_log.txt','failed','build')
        mail_Service.mailNotification('build', 'weight', False)
        

def dockerBuild_Billig():
    # docker compose weight
    # if fail- fail email
    # if success - success email
    # mail notificaiton for devOps & Billing Team
    try:
        subprocess.run("docker-compose -f /app/GanShmuel/weight/docker-compose.yml build", shell=True, check=True)
        mail_Service.mailNotification('build', 'billing', True)
        mail_Service.sendErrorToLog('billing_team_log.txt','success','build')
    except:
        mail_Service.sendErrorToLog('billing_team_log.txt','failed','build')
        mail_Service.mailNotification('build', 'billing', False)


def productionDeploy_Billing():
    try:
        subprocess.run("docker-compose -f /app/GanShmuel/billing/docker-compose.yml up", shell=True, check=True)
        mail_Service.mailNotification('build', 'weight', True)
        mail_Service.sendErrorToLog('billing_team_log.txt','success','deploy')
    except:
        mail_Service.sendErrorToLog('billing_team_log.txt','failed','deploy')
        mail_Service.mailNotification('build', 'weight', False)

def productionDeploy_Weight():
    try:
        subprocess.run("docker-compose -f /app/GanShmuel/weight/docker-compose.yml up", shell=True, check=True)
        mail_Service.mailNotification('deploy', 'weight', True)
        mail_Service.sendErrorToLog('weight_team_log.txt','success','deploy')
    except:
        mail_Service.sendErrorToLog('weight_team_log.txt','failed','deploy')
        mail_Service.mailNotification('deploy', 'weight', False)
        

def testingDeploy_Billing():
    # TODO: run docker-compose for testing
    # docker-compose up -d >> /app/test.log
    # mail notification accordingly
    try:
        subprocess.run("docker-compose -f /app/GanShmuel/billing/docker-compose.yml up", shell=True, check=True)
        mail_Service.mailNotification('deploy', 'billing', True)
        mail_Service.sendErrorToLog('billing_team_log.txt','success','deploy')
    except:
        mail_Service.sendErrorToLog('billing_team_log.txt','failed','deploy')
        mail_Service.mailNotification('deploy', 'billing', False)

def productionDeploy_Weight():
    try:
        subprocess.run("docker-compose -f /app/GanShmuel/weight/docker-compose.yml up", shell=True, check=True)
        mail_Service.mailNotification('deploy', 'weight', True)
        mail_Service.sendErrorToLog('weight_team_log.txt','success','deploy')
    except:
        mail_Service.sendErrorToLog('weight_team_log.txt','failed','deploy')
        mail_Service.mailNotification('deploy', 'weight', False)