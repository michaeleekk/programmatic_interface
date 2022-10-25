# biomage-programmatic-interface

### About
This python package provides an easy way to create projects and upload samples into Cellenics.

### Installation
To install the package execute the following line:
`pip install biomage-programmatic-interface`
 
### Usage
In order to use the package you first need to create an account in Cellenics (https://scp.biomage.net/) if you don't have one yet.

Then the package is used in the following way:
```python
import biomage_programmatic_interface as bpi

# 1. Authenticate user and create a connection tunnel with the api
# Default instance-url: https://api.scp.biomage.net/
connection = bpi.Connection('email', 'password', 'instance')

# 2. Create an experiment
experiment_id = connection.create_experiment()

# 3. Upload samples associated with the experiment
connection.upload_samples(experiment_id, 'local/path/to/samples')
```
Once the upload is complete you can navigate to [Cellenics](https://scp.biomage.net/) and process your project there.

### `Connection` class

The object accepts 3 parameters:
`email` - Cellenics email
`password` - Cellenics password
`instance` - Cellenics instance 
- `'biomage'` - (Default) Cellenics production build
-  `'staging'` - Cellenics staging environment

### Troubleshooting

`Max retries exceeded with url: / (Caused by SSLError(SSLEOFError(8, 'EOF occurred in violation of protocol (_ssl.c:2396)')))`
1. Navigate to your project in [Cellenics](https://scp.biomage.net/) and manually delete the failed sample
2. Run step #3 again

*This will be fixed when error handling is introduced*

### How to build the pip package

Update the version of the package and then build it:

`python3 -m build`

`twine upload dist/*`


### How to build the docker images
