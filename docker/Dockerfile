FROM python:3.7-alpine

LABEL com.jira-management.version="2.0.0" \
      vendor="FIWARE Foundation, e.V." \
      com.jira-management.release-date="2021-06-03" \
      com.jira-management.version.is-production="yes" \
      com.jira-management.maintainer="Fernando López <fernando.lopez@fiware.org>"

# Install dependencies
RUN apk update && \
    apk add --no-cache git gcc musl-dev libffi-dev openssl-dev python3-dev && \
    pip install --no-cache-dir -Iv configparser==3.8.1 && \
    pip install --no-cache-dir -Iv jira==2.0.0 && \
    apk del gcc musl-dev libffi-dev openssl-dev python3-dev

# Define the default BRANCH to get the code
ARG BRANCH=master

# Create a group and user
RUN addgroup -S mgmt && adduser -S mgmt -G mgmt

# Define the working directory
WORKDIR /home/mgmt

# Get the python code of the service
RUN git clone -b $BRANCH https://github.com/flopezag/fiware-management-scripts.git && \
    apk del git && \
    rm -f /var/cache/apk/* && \
    chown -R mgmt:mgmt fiware-management-scripts/

# Tell docker that all future commands should run as the appuser user
USER mgmt

# Define the ENV variable
ENV CONFIG_FILE /home/mgmt/fiware-management-scripts/Config/management.ini

# Execute the service
CMD [ "python", "/home/mgmt/fiware-management-scripts/management.py" ]