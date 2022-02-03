import os, subprocess
import testing

# from git import Repo
from mailingService.mail_Service import sendErrorToLog, mailNotification

import constants

# TODO: fix error
# Error: While importing 'main', an ImportError was raised.
def firstCopy():
    if  not os.path.isdir('GanShmuel'):
        try:
            subprocess.run("git clone https://github.com/develeapDorZ/GanShmuel", shell=True, check=True)
            # Just for testing DevOps junk!!! subprocess.run("git -C GanShmuel checkout DevOps", shell=True, check=True) 
        except:
            sendErrorToLog('repo_log.txt', 'failed', 'repo creation')
            mailNotification('updateRepo', 'devops', False)
            terminateContainer()
            return True, False
        else:
            mailNotification('updateRepo', 'devops', True)
            sendErrorToLog('repo_log.txt', 'success', 'repo creation')
            return True, True
    else:
        return False, False


def getCodeFromGitHub(branchName):
    # git clone git@github.com:develeapDorZ/GanShmuel.git
    branchName=branchName.lower()
    try:
        #Repo.pull(os.path.join(constants.gitHubURL, constants.deployDirectory))
        # pull -f --all - update the whole repo
        subprocess.run("git -C GanShmuel pull -f --all", shell=True, check=True) #noticed this can cause conflicts problematic???  
        # if branchName == "devops":
        #     pass #figure out how to update CI_SERVER
        #     # branchName="devOps"
        #     # subprocess.run(f'docker-compose -f ./GanShmuel/{branchName}/docker-compose.yml down')
        # elif branchName == "main":
        #     branchName="billing"
        #     print(f'process line 42 - main update before docker-compose down')
        #     subprocess.run(f'docker-compose -f ./GanShmuel/{branchName}/docker-compose.yml --env-file ./GanShmuel/{branchName}/.env_production_{branchName} down', shell=True, check=True)
        #     branchName="weight"
        #     subprocess.run(f'docker-compose -f ./GanShmuel/{branchName}/docker-compose.yml --env-file ./GanShmuel/{branchName}/.env_production_{branchName} down', shell=True, check=True)
            
        # else: 
        #     subprocess.run(f'docker-compose -f ./GanShmuel/{branchName}/docker-compose.yml --env-file ./GanShmuel/{branchName}/.env_production_{branchName} down', shell=True, check=True)
        
    except:
        sendErrorToLog('repo_log.txt', 'failed', 'repo update')
        mailNotification('updateRepo', 'devops', False)
        terminateContainer()
        return False
    else:
        mailNotification('updateRepo', 'devops', True)
        sendErrorToLog('repo_log.txt', 'success', 'repo update')
        return True


def dockerBuild(branchName):

    # remove image if already built
    # image = str(subprocess.run(f'docker image ls | grep {branchName}', shell=True, check=True))
    # imageName = image[0:image.find(" ")]
    # if imageName.find(branchName) >= 0:
    #     subprocess.run(f'docker rmi {imageName}')

    try:
        subprocess.run(f'docker-compose -f ./GanShmuel/{branchName}/docker-compose.yml --env-file ./GanShmuel/{branchName}/.env_production_{branchName} build', shell=True, check=True)

    except:
        sendErrorToLog(f'{branchName}_team_log.txt', 'failed', 'build')
        mailNotification('build', branchName, False)
        terminateContainer()
        return False
    else:
        mailNotification('build', branchName, True)
        sendErrorToLog(f'{branchName}_team_log.txt', 'success', 'build')
        return True


def dockerDeploy(branchName, env):
    try:
        if env == "test":
            subprocess.run(f"docker-compose -f ./GanShmuel/{branchName}/docker-compose.yml --env-file ./GanShmuel/{branchName}/.env_production_{branchName} -p {branchName}_test up -d", shell=True, check=True)
        
        else:
            subprocess.run(f"docker-compose -f ./GanShmuel/{branchName}/docker-compose.yml --env-file ./GanShmuel/{branchName}/.env_production_{branchName} up -d", shell=True, check=True)

    except:
        sendErrorToLog(f'{branchName}_team_log.txt', 'failed', 'deploy')
        mailNotification('build', branchName, False)
        terminateContainer()
        return False
    else:
        mailNotification('build', branchName, True)
        sendErrorToLog(f'{branchName}_team_log.txt', 'success', 'deploy')
        return True


def testingDeploy(branchName):
    path_weight = './GanShmuel/weight/test/'
    path_billing = './GanShmuel/billing/test/'

    answers = []
    if branchName == 'weight':
        answers = testing.testWeight(path_weight)
    elif branchName == 'billing':
        answers = testing.testWeight(path_billing)
    elif branchName == 'main':
        answers = testing.testProduction(path_billing,path_weight)

    if len(answers) == 0:
        return False

    success = True
    for ans in answers:
        for obj in ans:
            if ans.status != 'ok':
                success = False

    if not success:
        sendErrorToLog(f'{branchName}_team_log.txt', 'failed', 'test')
        mailNotification('build', branchName, False)
        terminateContainer()
        return False
    else:
        mailNotification('build', branchName, True)
        sendErrorToLog(f'{branchName}_team_log.txt', 'success', 'test')
        return True


def testHealthSiblings():
    results = []
    results.append('weight app health', subprocess.check_output('curl 127.0.0.1:8081/health', shell=True))
    results.append('billing app health', subprocess.check_output('curl 127.0.0.1:8080/health', shell=True))
    results.append('billing db health', subprocess.check_output('curl 127.0.0.1:8080/db_health', shell=True))
    # checkresults.append(subprocess.check_output(f'curl localhost:8080/db_health'))
    return results

def terminateContainer():
    pass
    # dosen't kill - problem with names of CTs
    # ---- WHat are the containers names defined by the teams
    # if subprocess.run('docker ps | grep "testbilling_ct"') == "testbilling_ct":
    #     subprocess.run("docker-compose testbilling_ct down")
    # if subprocess.run('docker ps | grep "testweight_ct"') == "testweight_ct":
    #     subprocess.run("docker-compose testweight_ct down")