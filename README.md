# cellenics-api

### About
This python package provides an easy way to create projects and upload samples into Cellenics.

### Installation
To install the package execute the following line:
`pip install cellenics_api`
 
### Usage
In order to use the package you first need to create an account in Cellenics (https://scp.biomage.net/) if you don't have one yet.

Then the package is used in the following way:
```python
import cellenics_api

# 1. Authenticate user and create a connection tunnel with the api
connection = cellenics_api.Connection('email', 'password')

# 2. Create an experiment
experiment_id = connection.create_experiment()

# 3. Upload samples associated with the experiment
connection.upload_samples(experiment_id, 'local/path/to/samples')
```
Once the upload is complete you can navigate to [Cellenics](https://scp.biomage.net/) and process your project there.

### Troubleshooting

`Max retries exceeded with url: / (Caused by SSLError(SSLEOFError(8, 'EOF occurred in violation of protocol (_ssl.c:2396)')))`
1. Navigate to your project in [Cellenics](https://scp.biomage.net/) and manually delete the failed sample
2. Run step #3 again

*This will be fixed when error handling is introduced*