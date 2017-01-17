#<a name="top"></a>FIWARE HelpDesk and Desks reminders script
[![License badge](https://img.shields.io/badge/license-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

These scripts were developed in order to facilitate the diary operations of the Jira
and the synchronization with different tools. The Purpose is to check if there are issues
open and send reminder to the owners (DesksReminder) and to synchronize the askbot and
stackoverflow with the tickets created in Jira.

These scripts were originally develop by Manuel Escriche from Telefónica I+D and now 
is maintained by me. I just updated some internal communication, moved from python3.4 to
python2.7 to use google oAuth module and improved installation and configuration of the
scripts.

## Description of the scripts

The scripts are divided into 2 subgroups:

- DesksReminder: it sends reminder over tickets that are not resolved.
- HelpDesk: it synchronizes the Jira issues with the data from Askbot 
and StackOverFlow and take a review of the ticket in main and coaches helpdesk.

[Top](#top)

## Build and Install

### Requirements

The following software must be installed:

- Python 2.7
- pip
- virtualenv


### Installation

The recommend installation method is using a virtualenv. Actually, the installation 
process is only about the python dependencies, because the python code do not need 
installation.

1. Clone this repository.
2. Excute the script 'source config.sh'
3. Define the configuration file in './DesksReminder/Basics/desksreminder.ini'
4. Define the configuration file in './HelpDesk/Basics/helpdeskreminder.ini'

Now the system is ready to use. Just activate the corresponding virtualenv and
launch the scripts.

[Top](#top)

## Configuration

The scripts are searching the configuration parameters or in the '/etc/fiware.d'
directory or in the environment variables.

In case of DesksReminder, the scripts try to find if there is defined an environment
variable whose name is 'DESKSREMINDER_SETTINGS_FILE' to the 'desksreminder.ini' file. 
If the scripts cannot get this environment variable, it tries to find this file in 
'/etc/init.d'. In any oder case, the scripts will give you an error.

In case of HelpDesk, the scripts try to find if there is defined an environment
variable whose name is 'HELPDESKREMINDER_SETTINGS_FILE' to the 'helpdeskreminder.ini' 
file. If the scripts cannot get this environment variable, it tries to find this 
file in '/etc/init.d'. In any oder case, the scripts will give you an error.

[Top](#top)

## License

These scripts are licensed under Apache License 2.0.
