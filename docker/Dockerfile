FROM python:3.7-alpine

LABEL com.jira-management.version="1.3.0" \
      vendor="FIWARE Foundation, e.V." \
      com.jira-management.release-date="2019-08-20" \
      com.jira-management.version.is-production="yes" \
      com.jira-management.maintainer="Fernando López <fernando.lopez@fiware.org>"

# Install the git package
RUN apk --no-cache add git gcc musl-dev libffi-dev openssl-dev python3-dev

RUN apk update && \
    apk add --no-cache git gcc musl-dev libffi-dev openssl-dev python3-dev && \
    pip install --no-cache-dir -Iv configparser==3.8.1 && \
    pip install --no-cache-dir -Iv jira==2.0.0 && \
    apk del gcc musl-dev libffi-dev openssl-dev python3-dev && \
    rm -f /var/cache/apk/*

# Define the default BRANCH to get the code
ARG BRANCH=master

# Create a group and user
RUN addgroup -S management && adduser -S management -G management

# Tell docker that all future commands should run as the appuser user
USER management

# Define the working directory
WORKDIR /home/management

# Get the python code of the service
RUN git clone -b $BRANCH https://github.com/flopezag/fiware-management-scripts.git

# Define the ENV variable
ENV CONFIG_FILE /home/management/fiware-management-scripts/Config/management.ini

# Execute the service
CMD [ "python", "/home/management/fiware-management-scripts/management.py" ]