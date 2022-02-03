from os import path
import requests
import json

HOST = "0.0.0.0"
PORT = "5000"
URL = f'http://{HOST}:{PORT}'

def test():
    test_results = []
    
    dirname = path.dirname(path.realpath(__file__))
    filename = path.join(dirname,"tests.json")
    
    with open(filename) as f:
        tests = json.load(f)

    for test in tests:
        try:
            api = test['api']
            result = test['result']
            reason = test['description']
            parameters = test['parameters']
            response_type = test['response_type']
            request_type = test['request_type']
            res = None

            if request_type == "GET":
                res = requests.get(f'{URL}/{api}',(None if parameters == "None" else parameters))
            elif request_type == "POST":
                res = requests.post(f'{URL}/{api}',(None if parameters == "None" else parameters))
            elif request_type == "PUT":
                res = requests.put(f'{URL}/{api}',(None if parameters == "None" else parameters))
            
            if response_type == "status_code":
                if res != None and res.status_code == result:
                    test_results.append({"status":"ok","reason":f'{reason} success'})
                else:
                    test_results.append({"status":"err","reason":f'{reason} failed'})
            elif response_type == "body_response":
                if res != None and res.content.decode("utf-8") == result:
                    test_results.append({"status":"ok","reason":f'{reason} success'})
                else:
                    test_results.append({"status":"err","reason":f'{reason} failed'})
        except:
            test_results.append({"status":"err","reason":f'{reason} failed'})

    for i in test_results:
    	print(i)
    return test_results
    
test()
