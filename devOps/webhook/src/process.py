import os, subprocess

# from git import Repo
from mailingService.mail_Service import sendErrorToLog, mailNotification

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
        sendErrorToLog('repo_log.txt', 'failed', 'repo update')
        mailNotification('updateRepo', 'devops', False)
    else:
        mailNotification('updateRepo', 'devops', True)
        sendErrorToLog('repo_log.txt', 'success', 'repo update')


def dockerBuild_Weight():
    try:
        subprocess.run("docker-compose -f /app/GanShmuel/billing/docker-compose.yml build", shell=True, check=True)

    except:
        sendErrorToLog('weight_team_log.txt', 'failed', 'build')
        mailNotification('build', 'weight', False)
    else:
        mailNotification('build', 'weight', True)
        sendErrorToLog('weight_team_log.txt', 'success', 'build')


def dockerBuild_Billig():
    try:
        subprocess.run("docker-compose -f /app/GanShmuel/weight/docker-compose.yml build", shell=True, check=True)

    except:
        sendErrorToLog('billing_team_log.txt', 'failed', 'build')
        mailNotification('build', 'billing', False)
    else:
        mailNotification('build', 'billing', True)
        sendErrorToLog('billing_team_log.txt', 'success', 'build')


def productionDeploy_Billing():
    try:
        subprocess.run("docker-compose -f /app/GanShmuel/billing/docker-compose.yml up", shell=True, check=True)

    except:
        sendErrorToLog('billing_team_log.txt', 'failed', 'deploy')
        mailNotification('build', 'weight', False)
    else:
        mailNotification('build', 'weight', True)
        sendErrorToLog('billing_team_log.txt', 'success', 'deploy')


def productionDeploy_Weight():
    try:
        subprocess.run("docker-compose -f /app/GanShmuel/weight/docker-compose.yml up", shell=True, check=True)

    except:
        sendErrorToLog('weight_team_log.txt', 'failed', 'deploy')
        mailNotification('deploy', 'weight', False)
    else:
        mailNotification('deploy', 'weight', True)
        sendErrorToLog('weight_team_log.txt', 'success', 'deploy')


def testingDeploy_Billing():
    # TODO: run docker-compose for testing
    # docker-compose up -d >> /app/test.log
    try:
        subprocess.run("docker-compose -f /app/GanShmuel/billing/docker-compose.yml up", shell=True, check=True)

    except:
        sendErrorToLog('billing_team_log.txt', 'failed', 'deploy')
        mailNotification('deploy', 'billing', False)
    else:
        mailNotification('deploy', 'billing', True)
        sendErrorToLog('billing_team_log.txt', 'success', 'deploy')


def productionDeploy_Weight():
    try:
        subprocess.run("docker-compose -f /app/GanShmuel/weight/docker-compose.yml up", shell=True, check=True)

    except:
        sendErrorToLog('weight_team_log.txt', 'failed', 'deploy')
        mailNotification('deploy', 'weight', False)
    else:
        mailNotification('deploy', 'weight', True)
        sendErrorToLog('weight_team_log.txt', 'success', 'deploy')
