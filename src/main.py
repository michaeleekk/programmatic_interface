from connection import Connection

connection = Connection('email', 'pass')
experiment_id = connection.create_experiment()
connection.upload_samples(experiment_id, 'test')




