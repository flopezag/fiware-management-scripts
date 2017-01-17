#!/usr/bin/env bash

# List of files to modify
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

# 1) Install virtualenv
# 2) source env/bin/activate
# 3) pip install -r requirements.txt


result=${PWD}

result=$(echo $result | sed 's@/@\\/@g')

# 4) configure files


for i in "${array_desk[@]}"; do   # The quotes are necessary here
    filename=$(find . -name $i)
    sed -i -e "s/$STRING_DESKSREMINDER/$result/" $filename
    rm $filename'-e'
done


for i in "${array_help[@]}"; do   # The quotes are necessary here
    filename=$(find . -name $i)
    sed -i -e "s/$STRING_HELPDESK/$result/" $filename
    rm $filename'-e'
done


# 5) configure crontab
