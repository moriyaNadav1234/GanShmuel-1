import subprocess
import json
from os import path

def perform_billing_test():
    dirname = path.dirname(__file__)
    filename = path.join(dirname,"tests.py")

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
        else:
            results.append({
                "name": test['reason'],
                "result": "Successfull!"
            })

    print(f'Failed {count}/{len(data)} Tests')
    return count
    

perform_billing_test()  
    