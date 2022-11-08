import boto3
import requests
import datetime
import hashlib
import requests
import datetime
import re
from biomage_programmatic_interface.sample import Sample

class Connection:
    def __init__(self, username, password, instance_url):
        self.__api_url = self.__get_api_url(instance_url)

        cognito_params = self.__get_cognito_params().json()
        clientId = cognito_params['clientId']
        region = cognito_params['clientRegion']

        self.__try_authenticate(username, password, clientId, region)

    def __get_cognito_params(self):
        return requests.get(self.__api_url + 'v2/programmaticInterfaceClient')

    def __try_authenticate(self, username, password, clientId, region):
        client = boto3.client('cognito-idp', region_name=region)

        try:
            resp = client.initiate_auth(
                ClientId=clientId,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters = { 
                    "USERNAME": username,
                    "PASSWORD": password
                }
            )

            print('Authorization succesfull')
            self.__jwt = resp['AuthenticationResult']['IdToken']
        except:
            raise Exception("Incorrect username or password")

    def __fetch_api(self, url, json, method='POST'):
        methods = {
            'POST': requests.post,
            'PATCH': requests.patch
        }

        headers = {
            'Authorization': 'Bearer ' + self.__jwt,
            'Content-Type': 'application/json'
        }

        return methods[method](self.__api_url + url, json=json, headers=headers)

    def __get_api_url(self, instance_url):
        if instance_url == 'local':
            return 'http://localhost:3000/'
        return f'https://api.{instance_url}/'

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

    def __notify_upload(self, experiment_id, sample_id, sample_file_type):
        url = "v2/experiments/{}/samples/{}/sampleFiles/{}".format(experiment_id, sample_id, sample_file_type)
        json = {  
            "uploadStatus": "uploaded"
        }
        response = self.__fetch_api(url, json, 'PATCH')

    def __create_sample_file(self, experiment_id, sample_uuid, sample_file):     
        url = 'v2/experiments/{}/samples/{}/sampleFiles/{}'.format(experiment_id, sample_uuid, sample_file.type())
        response = self.__fetch_api(url, sample_file.to_json())
        return response.content

    def __create_and_upload_sample(self, experiment_id, sample):
        url = 'v2/experiments/{}/samples/{}'.format(experiment_id, sample.uuid())
        self.__fetch_api(url, sample.to_json())

        print('Created sample {} - {}'.format(sample.name(), sample.uuid()))

        for sample_file in sample.get_sample_files():
            s3url_raw = self.__create_sample_file(experiment_id, sample.uuid(), sample_file)
            s3url = re.search(r"b\'\"(.*)\"\'", str(s3url_raw)).group(1)
            sample_file.upload_to_S3(s3url)
            self.__notify_upload(experiment_id, sample.uuid(), sample_file.type())
            print('Uploaded {} - {}...'.format(sample_file.name(), sample_file.uuid()))

    def upload_samples(self, experiment_id, samples_path):
        samples = Sample.get_all_samples_from_path(samples_path)
        for sample in samples:
            self.__create_and_upload_sample(experiment_id, sample)

        print('Project successfully created!')
