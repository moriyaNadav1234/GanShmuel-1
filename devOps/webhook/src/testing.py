import os
#important that path will look like this 
#billingTestsNames=os.listdir('./GanShmuel/billing/app/test/')
#weightTestsNames=os.listdir('./GanShmuel/weight/app/test/')

def testProduction(pathBill,pathWeight):
    billingTestsNames=os.listdir(pathBill)
    weightTestsNames=os.listdir(pathWeight)
    ans=[]
    for billTest,weightTest in zip(billingTestsNames,weightTestsNames):
        #make sure tests are in python or check for bash tests
        testOutputBilling = os.popen(pathBill + billTest).read
        testOutputWeight = os.popen(pathWeight + weightTest).read
        ans.append([testOutputBilling,testOutputWeight])
    return ans

def testWeight(pathWeight):
    weightTestsNames=os.listdir(pathWeight)
    ans=[]
    for weightTest in weightTestsNames:
         testOutputWeight = os.popen(pathWeight + weightTest).read
         ans.append(testOutputWeight)
    return ans


def testBilling(pathBill):
    billingTestsNames=os.listdir(pathBill)
    ans = []
    for billTest in billingTestsNames:
        testOutputBilling = os.popen(pathBill + billTest).read
        ans.append(testOutputBilling)
    return ans