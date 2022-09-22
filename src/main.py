import json
import boto3

import datetime
import hashlib
import requests

import uuid
import os
from os import listdir
from os.path import isfile, join
import datetime


def get_file_name(path):
    return path.split('/')[-1]

def get_folder_name(path):
    return path.split('/')[-2]

def get_files(path):
    files = listdir(path)

    ret = {}
    for file in files:
        full_path = join(path, file)
        if isfile(full_path):
            folder_name = get_folder_name(full_path)
            file_name = get_file_name(full_path)
            
            if ret.get(folder_name) == None:
                ret[folder_name] = [file_name]
            else:
                ret[folder_name].append(file_name)
            continue

        ret.update(get_files(full_path))

    return ret
        
# def file_object(path):
#     file_stat = os.stat(path)

#     date = datetime.datetime.fromtimestamp(file_stat.st_mtime)
#     print(date)
#     return {
#         "path": path,
#         "name": trim_path(path),
#         "size": file_stat.st_size,
#         "lastModified": int(file_stat.st_mtime * 1000)
#     }

def get_file_modified_date(path):
    file_stat = os.stat(path) 
    raw_date = str(datetime.datetime.fromtimestamp(file_stat.st_ctime))

    # 1. Add 'T' character between date and time
    # 2. Trim last 3 characters to match the precision of Cellenics UI
    # 3. Add 'Z' character in the end
    return 'T'.join(raw_date.split(' '))[:-3] + 'Z'

def create_sample(path, experiment_id):
    
    date = get_file_modified_date(path)
    # files = 

    return {
        complete: false,
        createdDate: get_file_modified_date(path),
        error: false,
        experiment_id: experiment_id,
        name: get_folder_name(path),
        # TODO: ADD THE REST OF THE REQ BODY
    }

# # create_sample(1, 1)

# files = get_files('output')
# print(files)
# # print(file_object(files[0]))
# exit()

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

def create_experiment(email: str = None, password: str = None, url: str = 'https://api-default.scp-staging.biomage.net/v2/experiments/', jwt_token: str = None):
    created_at = datetime.datetime.now().isoformat()
    hashed_string = hashlib.md5(created_at.encode())
    experiment_id = hashed_string.hexdigest()

    experiment_id = '12'

    jwt_token = jwt_token if jwt_token else authenticate_and_get_token(email, password) 

    headers = {
        'Authorization': 'Bearer ' + jwt_token,
        'Content-Type': 'application/json'
    }

    project_data = {
        'id': experiment_id,
        'name': experiment_id,
        'description': ''
    }

    response = requests.post(url + experiment_id, json=project_data, headers=headers)

    print('Experiment {} created!'.format(experiment_id))
    return experiment_id

