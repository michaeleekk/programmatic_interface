import datetime
import hashlib
import re
from biomage_programmatic_interface.sample import Sample

import boto3
import requests

import biomage_programmatic_interface.exceptions as exceptions


class Connection:
    def __init__(self, username, password, instance_url, verbose=True):
        self.verbose = verbose
        self.__api_url = self.__get_api_url(instance_url)
        cognito_params = self.__get_cognito_params().json()
        clientId = cognito_params["clientId"]
        region = cognito_params["clientRegion"]
        self.__authenticate(username, password, clientId, region)

    def __get_cognito_params(self):
        try:
            return requests.get(self.__api_url + "v2/programmaticInterfaceClient")
        except Exception:
            raise exceptions.InstanceNotFound() from None

    def __authenticate(self, username, password, clientId, region):
        client = boto3.client("cognito-idp", region_name=region)

        try:
            resp = client.initiate_auth(
                ClientId=clientId,
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={"USERNAME": username, "PASSWORD": password},
            )
        except Exception:
            raise exceptions.IncorrectCredentials() from None

        print('Authorization successful') if self.verbose else ""

        self.__jwt = resp["AuthenticationResult"]["IdToken"]

    def __fetch_api(self, url, body, method='POST'):
        methods = {
            'POST': requests.post,
            'PATCH': requests.patch
        }

        headers = {
            "Authorization": "Bearer " + self.__jwt,
            "Content-Type": "application/json",
        }

        return methods[method](self.__api_url + url, json=body, headers=headers)

    def __get_api_url(self, instance_url):
        if instance_url == "local":
            return "http://localhost:3000/"
        if instance_url.startswith("https://"):
            return instance_url
        return f"https://api.{instance_url}/"

    def create_experiment(self):
        created_at = datetime.datetime.now().isoformat()
        hashed_string = hashlib.md5(created_at.encode())
        experiment_id = hashed_string.hexdigest()

        experiment_data = {
            "id": experiment_id,
            "name": experiment_id,
            "description": "",
        }

        self.__fetch_api("v2/experiments/" + experiment_id, body=experiment_data)

        print(f"Experiment {experiment_id} created!") if self.verbose else ""
        return experiment_id

    def __notify_upload(self, experiment_id, sample_id, sample_file_type):
        url = "v2/experiments/{}/samples/{}/sampleFiles/{}".format(
            experiment_id, sample_id, sample_file_type
        )
        body = {"uploadStatus": "uploaded"}
        self.__fetch_api(url, body, "PATCH")

    def __create_sample_file(self, experiment_id, sample_uuid, sample_file):
        url = "v2/experiments/{}/samples/{}/sampleFiles/{}".format(
            experiment_id, sample_uuid, sample_file.type()
        )
        response = self.__fetch_api(url, sample_file.to_json())
        return response.content

    def __create_samples(self, experiment_id, samples):
        url = f"v2/experiments/{experiment_id}/samples"
        body = [sample.to_json() for sample in samples]
        
        sample_ids_by_name = self.__fetch_api(url, body).json()

        for sample in samples:

            uuid = sample_ids_by_name[sample.name()]
            sample.set_uuid(uuid)

    def __upload_sample(self, experiment_id, sample):
        url = 'v2/experiments/{}/samples/{}'.format(experiment_id, sample.uuid())
        self.__fetch_api(url, sample.to_json())

        print('Uploading sample {} - {}'.format(sample.name(), sample.uuid())) if self.verbose else ""

        for sample_file in sample.get_sample_files():
            s3url_raw = self.__create_sample_file(
                experiment_id, sample.uuid(), sample_file
            )
            s3url = re.search(r"b\'\"(.*)\"\'", str(s3url_raw)).group(1)
            sample_file.upload_to_S3(s3url)

            self.__notify_upload(experiment_id, sample.uuid(), sample_file.type())

            print(
                f"Uploaded {sample_file.name()} - {sample_file.uuid()}..."
            ) if self.verbose else ""

    def upload_samples(self, experiment_id, samples_path):
        samples = Sample.get_all_samples_from_path(samples_path)

        self.__create_samples(experiment_id, samples)

        for sample in samples:
            try:
                self.__upload_sample(experiment_id, sample)
            except Exception as e:
                print(
                    f"Upload failed: {e}. This is likely an error within \
                     the python package for uploading."
                )
                print(
                    "Please send an email to hello@biomage.net and we \
                     will try to resolve this problem as soon as possible"
                )
