import subprocess
import json
from os import path

def perform_billing_test():
    dirname = path.dirname(__file__)
    filename = path.join(dirname,'/GanShmuel/billing/test/',"tests.py")

    #TODO: check which python is availble here
    output = subprocess.check_output(f'python3 {filename}',shell=True)

    data = json.loads(output.decode("utf-8"))
    
    count=0
    results=[]
    for test in data:
        if test['status'] == "err":
            results.append({
                "name": test['reason'],
                "result": "Failed!"
            })
            count += 1

    print(f'Failed {count}/{len(data)} Tests')
    return count
    
# import os
# #important that path will look like this 
# #billingTestsNames=os.listdir('./GanShmuel/billing/app/test/')
# #weightTestsNames=os.listdir('./GanShmuel/weight/app/test/')

# def testProduction(pathBill,pathWeight):
#     billingTestsNames=os.listdir(pathBill)
#     weightTestsNames=os.listdir(pathWeight)
#     ans=[]
#     for billTest,weightTest in zip(billingTestsNames,weightTestsNames):
#         #make sure tests are in python or check for bash tests
#         testOutputBilling = os.popen(pathBill + billTest).read
#         testOutputWeight = os.popen(pathWeight + weightTest).read
#         ans.append([testOutputBilling,testOutputWeight])
#     return ans

# def testWeight(pathWeight):
#     weightTestsNames=os.listdir(pathWeight)
#     ans=[]
#     for weightTest in weightTestsNames:
#          testOutputWeight = os.popen(pathWeight + weightTest).read
#          ans.append(testOutputWeight)
#     return ans


# def testBilling(pathBill):
#     billingTestsNames=os.listdir(pathBill)
#     ans = []
#     for billTest in billingTestsNames:
#         testOutputBilling = os.popen(pathBill + billTest).read
#         ans.append(testOutputBilling)
#     return ans

