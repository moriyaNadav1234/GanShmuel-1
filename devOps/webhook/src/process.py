import subprocess, os
import app, constants
from mailingService import mail_Service
from git import Repo


def getCodeFromGitHub():
    #git clone git@github.com:develeapDorZ/GanShmuel.git
    #if fail - notify devOps Team
    try:
        repo.clone(os.path.join(constants.gitHubURL, constants.deployDirectory))
    except:
        #to log file
        #to mail service for devOps Team
        pass

def dockerBuild_Weight():
    # docker compose - weight
    # if fail- fail email
    # if success - success email
    # mail notificaiton for devOps & Weight Team
    try:
        subprocess.run("docker-compose -f /app/GanShmuel/billing/docker-compose.yml build", shell=True, check=True)
    except:
        # to log file
        # to mail service for devOps Team
    pass

def dockerBuild_Billig():
    # docker compose weight
    # if fail- fail email
    # if success - success email
    # mail notificaiton for devOps & Billing Team
    try:
        subprocess.run("docker-compose -f /app/GanShmuel/weight/docker-compose.yml build", shell=True, check=True)
    except:
    # to log file
    # to mail service for devOps Team
    pass

def productionDeploy_Billing():
    try:
        subprocess.run("docker-compose -f /app/GanShmuel/billing/docker-compose.yml up", shell=True, check=True)
    except:
        # to log file
        # to mail service for devOps Team
        pass

def productionDeploy_Weight():
    try:
        subprocess.run("docker-compose -f /app/GanShmuel/weight/docker-compose.yml up", shell=True, check=True)
    except:
        # to log file
        # to mail service for devOps Team
        pass


def testingDeploy_Billing():
    # TODO: run docker-compose for testing
    # docker-compose up -d >> /app/test.log
    # mail notification accordingly
    try:
        subprocess.run("docker-compose -f /app/GanShmuel/billing/docker-compose.yml up", shell=True, check=True)
    except:
        # to log file
        # to mail service for devOps Team
        pass

def productionDeploy_Weight():
    try:
        subprocess.run("docker-compose -f /app/GanShmuel/weight/docker-compose.yml up", shell=True, check=True)
    except:
        # to log file
        # to mail service for devOps Team
        pass