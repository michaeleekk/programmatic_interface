from connection import Connection
from utils import load_json

credentials = load_json('credentials.json')

connection = Connection(credentials['email'], credentials['password'])
experiment_id = connection.create_experiment()
connection.upload_samples(experiment_id, 'data')




