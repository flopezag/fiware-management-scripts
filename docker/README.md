# Supported tags and respective `Dockerfile` links

-	[`latest`, `1.3.0`](https://github.com/flopezag/fiware-management-scripts/docker/Dockerfile)

# Quick reference

-	**Where to get help**:  
	[the Docker Community Forums](https://forums.docker.com/), [the Docker Community Slack](https://blog.docker.com/2016/11/introducing-docker-community-directory-docker-community-slack/), or [Stack Overflow](https://stackoverflow.com/search?tab=newest&q=docker)

-	**Where to file issues**:  
	[https://github.com/flopezag/fiware-management-scripts/issues](https://github.com/flopezag/fiware-management-scripts/issues)

-	**Maintained by**:  
	[the FIWARE Foundation Operative Office](https://github.com/flopezag)

-	**Published image artifact details**:  
	[repo-info repo's `fiware-management-scripts` directory](https://github.com/flopezag/fiware-management-scripts/repo-info) ([history](https://github.com/flopezag/fiware-management-scripts/repo-info))  
	(image metadata, transfer size, etc)

-	**Image updates**:  
	[official-images PRs](https://github.com/flopezag/fiware-management-scripts/pulls?q=is%3Apr+is%3Aclosed)  
	[official-images repo's `fiware-management-scripts` file](https://github.com/flopezag/fiware-management-scripts/...) ([history](https://github.com/flopezagfiware-management-scripts/...))

-	**Source of this description**:  
	[docs repo's `fiware-management-scripts/` directory](https://github.com/flopez/fiware-management-scripts/docker/tree/master) ([history](https://github.com/flopez/fiware-management-scripts/docker/commits/master))

# What is JIRA Management Script Server?

This README will guide you through running Jira Management Script Server with Docker Containers. This script was 
developed in order to facilitate the diary operations of the Jira and the synchronization with different tools. The 
Purpose is to check if there are issues open and send reminder to the owners in order to resolve them and synchronize 
Jira issues with the data from Askbot and StackOverFlow.

# QuickStart with JIRA Management Script Server and Docker

Here is how to get a JIRA Management Script Server running on Docker containers:

**Step - 1 :** Make a copy of the example [configuration file](https://github.com/flopezag/fiware-management-scripts/blob/develop/Config/management.ini) and complete the information. Keep in mind that the docker compose use this local file to mount a volume in order to proper configure the server.

**Step - 2 :** Run Jira Management Script docker container through Docker Compose

`docker-compose up`

# Creation of docker images

In order to create the corresponding docker image, you can execute the command:

```console
docker build --rm -t docker-jira-mgmt .
```

It will create the corresponding image based on the last version of master. Nevertheless if you want to create a image
based on other branch, you can specify the BRANCH argument variable during the creation process with the following
command:

```console
docker build --rm --build-arg BRANCH=develop -t docker-jira-mgmt .
```


# License

Jira Management Script Server is licensed under APACHE License 2.0


