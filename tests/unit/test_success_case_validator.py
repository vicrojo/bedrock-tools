import boto3
import json
from os import path



def test_lambda_function_created():
    client = boto3.client('lambda')    
    file_path = path.abspath(__file__) # full path of your script
    dir_path = path.dirname(file_path) # full path of the directory of your script
    json_file_path = path.join(dir_path,"case_study_1.json") # absolute file path of json file
    
    f = open(json_file_path)
    payload = {}
    payload['case_study']= json.load(f)
    
    response = client.invoke(
        FunctionName='SuccessCaseValidator-lambda',
        InvocationType='RequestResponse',
        Payload=json.dumps(payload),
        Qualifier='$LATEST'        
    )
    
    results = response['Payload'].read()
    response = json.loads(results)
    print(response['case_results'])
    
test_lambda_function_created()

