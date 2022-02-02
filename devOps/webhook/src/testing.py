import os
pathTobilling='./GanShmuel/billing/app/test/'
pathToWeight ='./GanShmuel/weight/app/test/'
billingTests=os.listdir('./GanShmuel/billing/app/test')
weightTests=os.listdir('./GanShmuel/weight/app/test')
for billTest,weightTest in zip(billingTests,weightTests):
    os.system(pathTobilling + billTest)
    os.system(pathToWeight+weightTest)