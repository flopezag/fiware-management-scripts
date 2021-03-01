# <a name="top"></a>FIWARE HelpDesk and Desks reminders script
[![License badge](https://img.shields.io/badge/license-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This script was developed in order to facilitate the diary operations of the Jira
and the synchronization with different tools. The Purpose is to check if there are issues
open and send reminders to the owners in order to resolve them and synchronize Jira issues 
with the data from Askbot and StackOverFlow.

These scripts were originally developed by Manuel Escriche from Telefónica I+D and now 
is maintained by me.

[Top](#top)

## Build and Install

### Requirements

The following software must be installed:

- Python 3.9
- pip
- virtualenv


### Installation

The recommended installation method is using a virtualenv. Actually, the installation 
process is only about the python dependencies, because the python code do not need 
installation.

1. Clone this repository.
2. Define the configuration file: `./Config/management.ini`
3. Create the virtualenv: `virtualenv -ppython3.9 env`
4. Activate the python environment: `source ./env/bin/activate`
5. Install the requirements: `pip install -r requirements.txt

By default, the service will take the content of the Environment variable `CONFIG_FILE`. If it is not specified, the
service will take the values by default from the [local configuration file](./Config/management.ini) file.

[Top](#top)

## Configuration

The scripts are searching the configuration parameters or in the '/etc/fiware.d'
directory or in the environment variables. It tries to find if there is defined an environment
variable whose name is 'CONFIG_FILE' to the 'management.ini' file. 
If the scripts cannot get this environment variable, it tries to find this file in 
'/etc/init.d'. In any other case, the scripts will give you an error.

One possible solution might be to provide a soft link in the `/etc/fiware.d` to the `management.ini`
file in the corresponding `./Config` folder, excuting the command:

```bash
ln -s /home/ubuntu/fiware-management-scripts/Config/management.ini management.ini
```

Last but not least, it is possible to create a cronjob to automatically execute the tests, just execute
the following commands:

```bash
echo "# FIWARE Management Script" | crontab -
( crontab -l ; echo "00 2 * * MON /home/ubuntu/fiware-management-scripts/management.py -a Tech" ) | crontab -
( crontab -l ; echo "30 2 * * MON /home/ubuntu/fiware-management-scripts/management.py -a Lab" ) | crontab - 
( crontab -l ; echo "00 3 * * MON /home/ubuntu/fiware-management-scripts/management.py -a Other" ) | crontab - 
( crontab -l ; echo "30 3 * * MON /home/ubuntu/fiware-management-scripts/management.py -a Urgent" ) | crontab -
( crontab -l ; echo "00 4 * * MON /home/ubuntu/fiware-management-scripts/management.py -a Accounts" ) | crontab -

( crontab -l ; echo "30 4 * * * /home/ubuntu/fiware-management-scripts/management.py -a Askbot" ) | crontab -
( crontab -l ; echo "00 5 * * * /home/ubuntu/fiware-management-scripts/management.py -a Caretaker" ) | crontab -
( crontab -l ; echo "30 5 * * * /home/ubuntu/fiware-management-scripts/management.py -a Stackoverflow" ) | crontab -
```

[Top](#top)

## Docker and Docker Compose

For more details about the docker version of the service, take a look to the [README](./docker/README.md) content.
In case that you need to access to the created image, execute the following command:

```bash
docker run -it <Docker Image ID> sh
```

## Troubleshooting 

### Problems with Google Credentials

It is natural that the Google Access Token and Google Refresh Token expires after a while. If it is the Access Token
the one that it expires the system can regenerate automatically a new Access Token using the Refresh Token. Nevertheless,
if the Refresh Token is expired too, you need to request new Access Token and Refresh Token using the Client ID and 
Client Secret. You can use the script [oauth2.py](./Common/oauth2.py) to generate and authorize an OAuth2 token.

```bash
  oauth2 --user=xxx@yyy.zzz \
    --client_id=1038[...].apps.googleusercontent.com \
    --client_secret=[...] \
    --generate_oauth2_token
```

More details, take a look to the [README](./Common/README.md) content.

## License

These scripts are licensed under Apache License 2.0.
