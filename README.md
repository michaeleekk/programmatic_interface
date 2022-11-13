# biomage-programmatic-interface

### About
This python package provides an easy way to create projects and upload samples into Biomage.

### Installation
To install the package execute the following line:
`pip install biomage-programmatic-interface`
 
### Usage
In order to use the package you first need to create an account in Biomage (https://scp.biomage.net/) if you don't have one yet.

Then the package is used in the following way:
```python
import biomage_programmatic_interface as bpi

# 1. Authenticate user and create a connection tunnel with the api
# Default instance-url: https://api.scp.biomage.net/
connection = bpi.Connection('email', 'password', 'instance_url')

# 2. Create an experiment
experiment_id = connection.create_experiment()

# 3. Upload samples associated with the experiment
connection.upload_samples(experiment_id, 'local/path/to/samples')
```
Once the upload is complete you can navigate to [Biomage](https://scp.biomage.net/) and process your project there.

### `Connection` class

The object accepts 3 parameters:
`email` - Biomage email
`password` - Biomage password
`instance_url` - Biomage instance url
- Copy the url of the Biomage instance *excluding* `https://`
- If the url is https://scp.biomage.net/ enter just the domain name: `scp.biomage.net` 

### Troubleshooting

`Max retries exceeded with url: / (Caused by SSLError(SSLEOFError(8, 'EOF occurred in violation of protocol (_ssl.c:2396)')))`
1. Navigate to your project in [Biomage](https://scp.biomage.net/) and manually delete the failed sample
2. Run step #3 again

*This will be fixed when error handling is introduced*

### How to build the pip package

Update the version of the package in `setup.cfg` and `requirements.txt` then build it using the bash script:

```bash 
./pip-build-upload.sh
```

### How to build the docker images

After `requirements.txt` has been updated with the correct package version run:
```bash
./docker-build-upload.sh {version}
```
where `version` is the version of the docker image, e.g. 0.0.3 