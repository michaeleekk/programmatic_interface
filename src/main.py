import json
import boto3

import datetime
import hashlib
import requests

def load_cognito_config():
    with open('cognito.config.json') as raw_file:
        config = json.load(raw_file)

    return config

def authenticate_and_get_token(username: str, password: str) -> None:
    cognito_config = load_cognito_config()
    client = boto3.client('cognito-idp')

    try:
        resp = client.admin_initiate_auth(
            UserPoolId=cognito_config['UserPoolId'],
            ClientId=cognito_config['ClientId'],
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters = { 
                "USERNAME": username,
                "PASSWORD": password
            }
        )

        print('Authorization succesfull')
        return resp['AuthenticationResult']['IdToken']
    except:
        print("Incorrect username or password.")
        raise Exception("Incorrect username or password")

def create_experiment(email, password):
    created_at = datetime.datetime.now().isoformat()
    hashed_string = hashlib.md5(created_at.encode())
    experiment_id = hashed_string.hexdigest()

    jwt_token = authenticate_and_get_token(email, password)

    headers = {
        'Authorization': 'Bearer ' + jwt_token,
        'Content-Type': 'application/json'
    }

    project_data = {
        'id': experiment_id,
        'name': experiment_id,
        'description': ''
    }

    response = requests.post('https://api-default.scp-staging.biomage.net/v2/experiments/' + experiment_id, json=project_data, headers=headers)

    print('Experiment {} created!'.format(experiment_id))

