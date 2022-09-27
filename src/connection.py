from utils import load_json
import boto3
import requests

import datetime
import hashlib
import requests

import datetime

from file import File
from sample import Sample

class Connection:

    def __init__(self, username, password):
        self.__cognito_config = load_json('cognito.config.json')
        self.__default_config = load_json('default.config.json')
        self.__try_authenticate(username, password)

    def __try_authenticate(self, username, password):
        client = boto3.client('cognito-idp')

        try:
            resp = client.admin_initiate_auth(
                UserPoolId=self.__cognito_config['UserPoolId'],
                ClientId=self.__cognito_config['ClientId'],
                AuthFlow='ADMIN_NO_SRP_AUTH',
                AuthParameters = { 
                    "USERNAME": username,
                    "PASSWORD": password
                }
            )

            print('Authorization succesfull')
            self.__jwt = resp['AuthenticationResult']['IdToken']
        except:
            raise Exception("Incorrect username or password")

    def __fetch_api(self, url, json):
        root_url = self.__default_config['url']

        headers = {
            'Authorization': 'Bearer ' + self.__jwt,
            'Content-Type': 'application/json'
        }

        return requests.post(root_url + url, json=json, headers=headers)

    def create_experiment(self):
        created_at = datetime.datetime.now().isoformat()
        hashed_string = hashlib.md5(created_at.encode())
        experiment_id = hashed_string.hexdigest()

        experiment_data = {
            'id': experiment_id,
            'name': experiment_id,
            'description': ''
        }

        response = self.__fetch_api('v2/experiments/' + experiment_id, json=experiment_data)

        print('Experiment {} created!'.format(experiment_id))
        return experiment_id

    def __create_sample_file(self, experiment_id, sample_uuid, sample_file):     
        url = 'v2/experiments/{}/samples/{}/sampleFiles/{}'.format(experiment_id, sample_uuid, sample_file.type())
        response = self.__fetch_api(url, sample_file.to_json())
        return response.content

    def __create_sample(self, experiment_id, sample_obj):
        sample = Sample(experiment_id, sample_obj)

        url = 'v2/experiments/{}/samples/{}'.format(experiment_id, sample.uuid())
        self.__fetch_api(url, sample.to_json())
        print(sample.get_sample_files())
        for sample_file in sample.get_sample_files():
            s3url = self.__create_sample_file(experiment_id, sample.uuid(), sample_file)
            print(s3url)

    def upload_samples(self, experiment_id, samples_path):
        samples = File.get_files(samples_path)

        for sample_obj in samples.values():
            self.__create_sample(experiment_id, sample_obj)

