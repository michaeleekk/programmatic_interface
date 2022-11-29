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
1. `email` - Biomage email
2. `password` - Biomage password
3. `instance_url` - Biomage instance url

- Copy the url of the Biomage instance *excluding* `https://`
- If the url is https://scp.biomage.net/ enter just the domain name: `scp.biomage.net`

### Development

If you cloned the repository and want to try using your local version, do the following:

- Install the local version of the pip package:
```bash
cd programmatic_interface
make install
```

- Now you can import the package and use your local version

```python
import biomage_programmatic_interface as bpi
```

***NOTE***: There is **NO** need to run `make install` every time you make changes to the package. When the local changes have been saved the changes will be automatically reflected.