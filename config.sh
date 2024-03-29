#!/usr/bin/env bash
##
# Copyright 2017 FIWARE Foundation, e.V.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
##



# Initializing variables

PYTHON_FILE="management.py"
INITIAL_HEADER="#\!\/usr\/bin\/env python"
FINAL_HEADER='#\!\/usr\/bin\/env '
VIRTUALENV_DIR='\/.env\/bin\/python'



# 1) Install&Config virtualenv for DesksReminder
if [ ! -d ".env" ]; then
  # Control will enter here if env does not exist.
  virtualenv -p python3.9 .env

  source .env/bin/activate
  pip install -r requirements.txt

  deactivate
fi



# 2) Configure management.py file

working_directory=${PWD}

result=$(echo ${working_directory} | sed 's@/@\\/@g')

FINAL_HEADER=${FINAL_HEADER}${result}${VIRTUALENV_DIR}

sed -i -e "s/${INITIAL_HEADER}/${FINAL_HEADER}/" ${PYTHON_FILE}

chmod 744 ${PYTHON_FILE}



# 3) Configure logrotate

# Take the file and generate the proper content based on installation
PATH_TO_CHANGE='\/logs\/tsc-dashboard\.log'
NEW_PATH=${result}${PATH_TO_CHANGE}

sed -i -e "s/${PATH_TO_CHANGE}/${NEW_PATH}/" ./config/tsc-dashboard.logrotate
sed -i "s/\/logs/\/home\/ubuntu\/fiware-management-scripts\/logs/g" management.logrotate

echo ""
echo ""
echo "Please, with root user, execute the following command:"
echo ""
echo "sudo cp ./Config/management.logrotate /etc/logrotate.d/management-scripts"



# 4) configure crontab
username=$(whoami)
result=$(crontab -u ${username} -l 2>/dev/null)

if [ "$result" == "" ]; then
    if [ -e /tmp/cronlock ]; then
        echo "cronjob locked"
        exit 1
    fi

    touch /tmp/cronlock

    echo "# FIWARE Management Script" | crontab -
    ( crontab -l ; echo "00 2 * * MON "${working_directory}"/management.py -a Tech" ) | crontab -
    ( crontab -l ; echo "30 2 * * MON "${working_directory}"/management.py -a Lab" ) | crontab -
    ( crontab -l ; echo "00 3 * * MON "${working_directory}"/management.py -a Other" ) | crontab -
    ( crontab -l ; echo "30 3 * * MON "${working_directory}"/management.py -a Urgent" ) | crontab -
    ( crontab -l ; echo "00 4 * * MON "${working_directory}"/management.py -a Accounts" ) | crontab -

    ( crontab -l ; echo "30 4 * * * "${working_directory}"/management.py -a Askbot" ) | crontab -
    ( crontab -l ; echo "00 5 * * * "${working_directory}"/management.py -a Caretaker" ) | crontab -
    ( crontab -l ; echo "30 5 * * * "${working_directory}"/management.py -a Stackoverflow" ) | crontab -

    rm -f /tmp/cronlock

else
    crontab -u ${username} -l 2>/dev/null >a.out

    touch /tmp/cronlock

    line=$(grep "00 4 * * mon-fri "${working_directory}"/dashboard.py --noauth_local_webserver" a.out)
    if [ "$line" == "" ]; then
        (crontab -l; echo "") | crontab -
        (crontab -l; echo "# FIWARE TSC Enabler Dashboard") | crontab -
        (crontab -l; echo "00 4 * * * "${working_directory}"/dashboard.py --noauth_local_webserver") | crontab -

        (crontab -l; echo "") | crontab -
        (crontab -l; echo "# FIWARE Management Script") | crontab -

        ( crontab -l ; echo "00 2 * * MON "${working_directory}"/management.py -a Tech" ) | crontab -
        ( crontab -l ; echo "30 2 * * MON "${working_directory}"/management.py -a Lab" ) | crontab -
        ( crontab -l ; echo "00 3 * * MON "${working_directory}"/management.py -a Other" ) | crontab -
        ( crontab -l ; echo "30 3 * * MON "${working_directory}"/management.py -a Urgent" ) | crontab -
        ( crontab -l ; echo "00 4 * * MON "${working_directory}"/management.py -a Accounts" ) | crontab -

        ( crontab -l ; echo "30 4 * * * "${working_directory}"/management.py -a Askbot" ) | crontab -
        ( crontab -l ; echo "00 5 * * * "${working_directory}"/management.py -a Caretaker" ) | crontab -
        ( crontab -l ; echo "30 5 * * * "${working_directory}"s/management.py -a Stackoverflow" ) | crontab -
    fi

    rm -f /tmp/cronlock

    rm a.out
fi
