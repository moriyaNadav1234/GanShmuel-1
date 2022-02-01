import os, subprocess

from git import Repo
from mailingService import mail_Service

import constants

# TODO: fix error
# Error: While importing 'main', an ImportError was raised.

def getCodeFromGitHub():
    # git clone git@github.com:develeapDorZ/GanShmuel.git
    try:
        #Repo.pull(os.path.join(constants.gitHubURL, constants.deployDirectory))
        # pull -f --all - update the whole repo
        subprocess.run("/app/GanShmuel/git pull -f --all", shell=True, check=True)

    except:
        mail_Service.sendErrorToLog('repo_log.txt', 'failed', 'repo update')
        mail_Service.mailNotification('updateRepo', 'devops', False)
    else:
        mail_Service.mailNotification('updateRepo', 'devops', True)
        mail_Service.sendErrorToLog('repo_log.txt', 'success', 'repo update')


def dockerBuild_Weight():
    try:
        subprocess.run("docker-compose -f /app/GanShmuel/billing/docker-compose.yml build", shell=True, check=True)

    except:
        mail_Service.sendErrorToLog('weight_team_log.txt', 'failed', 'build')
        mail_Service.mailNotification('build', 'weight', False)
    else:
        mail_Service.mailNotification('build', 'weight', True)
        mail_Service.sendErrorToLog('weight_team_log.txt', 'success', 'build')


def dockerBuild_Billig():
    try:
        subprocess.run("docker-compose -f /app/GanShmuel/weight/docker-compose.yml build", shell=True, check=True)

    except:
        mail_Service.sendErrorToLog('billing_team_log.txt', 'failed', 'build')
        mail_Service.mailNotification('build', 'billing', False)
    else:
        mail_Service.mailNotification('build', 'billing', True)
        mail_Service.sendErrorToLog('billing_team_log.txt', 'success', 'build')


def productionDeploy_Billing():
    try:
        subprocess.run("docker-compose -f /app/GanShmuel/billing/docker-compose.yml up", shell=True, check=True)

    except:
        mail_Service.sendErrorToLog('billing_team_log.txt', 'failed', 'deploy')
        mail_Service.mailNotification('build', 'weight', False)
    else:
        mail_Service.mailNotification('build', 'weight', True)
        mail_Service.sendErrorToLog('billing_team_log.txt', 'success', 'deploy')


def productionDeploy_Weight():
    try:
        subprocess.run("docker-compose -f /app/GanShmuel/weight/docker-compose.yml up", shell=True, check=True)

    except:
        mail_Service.sendErrorToLog('weight_team_log.txt', 'failed', 'deploy')
        mail_Service.mailNotification('deploy', 'weight', False)
    else:
        mail_Service.mailNotification('deploy', 'weight', True)
        mail_Service.sendErrorToLog('weight_team_log.txt', 'success', 'deploy')


def testingDeploy_Billing():
    # TODO: run docker-compose for testing
    # docker-compose up -d >> /app/test.log
    try:
        subprocess.run("docker-compose -f /app/GanShmuel/billing/docker-compose.yml up", shell=True, check=True)

    except:
        mail_Service.sendErrorToLog('billing_team_log.txt', 'failed', 'deploy')
        mail_Service.mailNotification('deploy', 'billing', False)
    else:
        mail_Service.mailNotification('deploy', 'billing', True)
        mail_Service.sendErrorToLog('billing_team_log.txt', 'success', 'deploy')


def productionDeploy_Weight():
    try:
        subprocess.run("docker-compose -f /app/GanShmuel/weight/docker-compose.yml up", shell=True, check=True)

    except:
        mail_Service.sendErrorToLog('weight_team_log.txt', 'failed', 'deploy')
        mail_Service.mailNotification('deploy', 'weight', False)
    else:
        mail_Service.mailNotification('deploy', 'weight', True)
        mail_Service.sendErrorToLog('weight_team_log.txt', 'success', 'deploy')
