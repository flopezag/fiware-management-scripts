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


# Initialicing variables

array_desk=("fiware-accountsdesk.py"
"fiware-deliveryboard.py"
"fiware-helpdesk-otherChannels.py"
"fiware-urgentDesk-daily.py"
"fiware-coachesdesk.py"
"fiware-helpdesk-lab.py"
"fiware-helpdesk-tech.py"
"fiware-urgentDesk-weekly.py")

array_help=("fiware-askbot-jira-syncronization.py"
"fiware-main-helpdesk-caretaker.py"
"fiware-coaches-helpdesk-caretaker.py"
"fiware-stackoverflow-jira-syncronization.py")

STRING_DESKSREMINDER="<PATH_DESKSREMINDER>"
STRING_HELPDESK="<PATH_HELPDESK>"


# 1.1) Install&Config virtualenv for DesksReminder
cd DesksReminder
virtualenv -p python2.7 env

source env/bin/activate
pip install -r requirements.txt

cd ..
deactivate


# 1.2) Install&Config virtualenv for HelpDesk
cd HelpDesk
virtualenv -p python2.7 env

source env/bin/activate
pip install -r requirements.txt

cd ..
deactivate


# 2) Configure files

working_directory=${PWD}

result=$(echo $working_directory | sed 's@/@\\/@g')

result_desk=$result'\/DesksReminder'
for i in "${array_desk[@]}"; do   # The quotes are necessary here
    filename=$(find . -name $i)
    sed -i -e "s/$STRING_DESKSREMINDER/$result_desk/" $filename
    rm $filename'-e' 2>/dev/null
done

result_help=$result'\/HelpDesk'
for i in "${array_help[@]}"; do   # The quotes are necessary here
    filename=$(find . -name $i)
    sed -i -e "s/$STRING_HELPDESK/$result_help/" $filename
    rm $filename'-e' 2>/dev/null
done


# 3) configure crontab
username=$(whoami)
result=$(crontab -u $username -l 2>/dev/null)

if [ "$result" == "" ]; then
    echo "Creating crontab content"

    if [ -e /tmp/cronlock ]; then
        echo "cronjob locked"
        exit 1
    fi

    touch /tmp/cronlock

    echo "5 * * * * "$working_directory"/HelpDesk/fiware-askbot-jira-syncronization.py" | crontab -
    (crontab -l; echo "5 */3 * * * "$working_directory"/HelpDesk/fiware-stackoverflow-jira-syncronization.py") | crontab -
    (crontab -l; echo "*/5 * * * * "$working_directory"/HelpDesk/fiware-coaches-helpdesk-caretaker.py") | crontab -
    (crontab -l; echo "*/5 * * * * "$working_directory"/HelpDesk/fiware-main-helpdesk-caretaker.py") | crontab -

    (crontab -l; echo "45 6 * * mon "$working_directory"/DesksReminder/fiware-urgentDesk-weekly.py") | crontab -
    (crontab -l; echo "50 6 * * mon "$working_directory"/DesksReminder/fiware-deliveryboard.py") | crontab -
    (crontab -l; echo "55 6 * * mon-fri "$working_directory"/DesksReminder/fiware-urgentDesk-daily.py") | crontab -
    (crontab -l; echo "00 7 * * mon-fri "$working_directory"/DesksReminder/fiware-helpdesk-tech.py") | crontab -
    (crontab -l; echo "05 7 * * mon-fri "$working_directory"/DesksReminder/fiware-helpdesk-lab.py") | crontab -
    (crontab -l; echo "10 7 * * mon-fri "$working_directory"/DesksReminder/fiware-coachesdesk.py") | crontab -
    (crontab -l; echo "15 7 * * mon-fri "$working_directory"/DesksReminder/fiware-accountsdesk.py") | crontab -
    (crontab -l; echo "20 7 * * mon-fri "$working_directory"/DesksReminder/fiware-helpdesk-otherChannels.py") | crontab -

    rm -f /tmp/cronlock

else
    echo "Checking crontab content"

    crontab -u $username -l 2>/dev/null >a.out

    line=$(grep "5 * * * * "$working_directory"/HelpDesk/fiware-askbot-jira-syncronization.py" a.out)
    if [ "$line" == "" ]; then
        (crontab -l; echo "5 * * * * "$working_directory"/HelpDesk/fiware-askbot-jira-syncronization.py") | crontab -l
    fi

    line=$(grep "5 */3 * * * "$working_directory"/HelpDesk/fiware-stackoverflow-jira-syncronization.py" a.out)
    if [ "$line" == "" ]; then
        (crontab -l; echo "5 */3 * * * "$working_directory"/HelpDesk/fiware-stackoverflow-jira-syncronization.py") | crontab -l
    fi

    line=$(grep "*/5 * * * * "$working_directory"/HelpDesk/fiware-coaches-helpdesk-caretaker.py" a.out)
    if [ "$line" == "" ]; then
        (crontab -l; echo "*/5 * * * * "$working_directory"/HelpDesk/fiware-coaches-helpdesk-caretaker.py") | crontab -l
    fi

    line=$(grep "*/5 * * * * "$working_directory"/HelpDesk/fiware-main-helpdesk-caretaker.py" a.out)
    if [ "$line" == "" ]; then
        (crontab -l; echo "*/5 * * * * "$working_directory"/HelpDesk/fiware-main-helpdesk-caretaker.py") | crontab -l
    fi



    line=$(grep "45 6 * * mon "$working_directory"/DesksReminder/fiware-urgentDesk-weekly.py" a.out)
    if [ "$line" == "" ]; then
        (crontab -l; echo "45 6 * * mon "$working_directory"/DesksReminder/fiware-urgentDesk-weekly.py") | crontab -l
    fi

    line=$(grep "50 6 * * mon "$working_directory"/DesksReminder/fiware-deliveryboard.py" a.out)
    if [ "$line" == "" ]; then
        (crontab -l; echo "50 6 * * mon "$working_directory"/DesksReminder/fiware-deliveryboard.py") | crontab -l
    fi

    line=$(grep "55 6 * * mon-fri "$working_directory"/DesksReminder/fiware-urgentDesk-daily.py" a.out)
    if [ "$line" == "" ]; then
        (crontab -l; echo "55 6 * * mon-fri "$working_directory"/DesksReminder/fiware-urgentDesk-daily.py") | crontab -l
    fi

    line=$(grep "00 7 * * mon-fri "$working_directory"/DesksReminder/fiware-helpdesk-tech.py" a.out)
    if [ "$line" == "" ]; then
        (crontab -l; echo "00 7 * * mon-fri "$working_directory"/DesksReminder/fiware-helpdesk-tech.py") | crontab -l
    fi

    line=$(grep "05 7 * * mon-fri "$working_directory"/DesksReminder/fiware-helpdesk-lab.py" a.out)
    if [ "$line" == "" ]; then
        (crontab -l; echo "05 7 * * mon-fri "$working_directory"/DesksReminder/fiware-helpdesk-lab.py") | crontab -l
    fi

    line=$(grep "10 7 * * mon-fri "$working_directory"/DesksReminder/fiware-coachesdesk.py" a.out)
    if [ "$line" == "" ]; then
        (crontab -l; echo "10 7 * * mon-fri "$working_directory"/DesksReminder/fiware-coachesdesk.py") | crontab -l
    fi

    line=$(grep "15 7 * * mon-fri "$working_directory"/DesksReminder/fiware-accountsdesk.py" a.out)
    if [ "$line" == "" ]; then
        (crontab -l; echo "15 7 * * mon-fri "$working_directory"/DesksReminder/fiware-accountsdesk.py") | crontab -l
    fi

    line=$(grep "20 7 * * mon-fri "$working_directory"/DesksReminder/fiware-helpdesk-otherChannels.py" a.out)
    if [ "$line" == "" ]; then
        (crontab -l; echo "20 7 * * mon-fri "$working_directory"/DesksReminder/fiware-helpdesk-otherChannels.py") | crontab -l
    fi

    rm a.out
fi


