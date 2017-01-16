# FIWARE HelpDesk and Desks reminders script

These scripts were developed in order to facilitate the diary operations of the Jira
and the synchronization with different tools. The Purpose is to check if there are issues
open and send reminder to the owners (DesksReminder) and to synchronize the askbot and
stackoverflow with the tickets created in Jira.

## Description of the scripts

The scripts are divided into 2 subgroups:

- DesksReminder: it sends reminder over tickets that are not resolved.
- HelpDesk: it synchronizes the Jira issues with the data from Askbot 
and StackOverFlow and take a review of the ticket in main and coaches helpdesk.

## Build and Install

### Requirements

The following software must be installed:

- Python 2.7
- pip
- virtualenv


### Installation

The recommend installation method for each subcomponents is using a virtualenv. 
Actually, the installation process is only about the python dependencies, because 
the python code do not need installation.

1) Create a virtualenv 'env' invoking *virtualenv env*
2) Activate the virtualenv with *source env/bin/activate*
3) Install the requirements running *pip install -r requirements.txt
   --allow-all-external*

Now the system is ready to use. For future sessions, only the step2 is required.


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

