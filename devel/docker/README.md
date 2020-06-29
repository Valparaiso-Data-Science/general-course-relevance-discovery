# How to run this docker file

First you need to make sure that you have docker installed.

macOS people:
* Follow the guide [here](https://docs.docker.com/docker-for-mac/install/)

Linux people:
* Use your package manager or your distribution's documentation on docker.

Windows pro, enterprise, or education people:
* Follow the guide [here](https://docs.docker.com/docker-for-windows/install/)

Windows Home People:
* Follow the guide [here](https://docs.docker.com/docker-for-windows/install-windows-home/)

**NOTE**: Window's home people will need to do more work, because docker on that platform is fairly new.

Next you need to make sure that you are in this directory on a terminal emulator of some sort, for macs that would be the terminal, and for windows people you should use the fancy new [windows terminal](https://github.com/microsoft/terminal/releases/latest).


'cd' into this directory and run the following commands:
```
docker build -t gcrd .
docker run -it --rm --name gcrd gcrd /bin/bash
```
After running those commands, you should be in a terminal session inside of the docker container. Think of it like 'ssh-ing' into a server.

To leave the container, just type:
```
exit
```
Like you would if you were leaving ssh.

If you want to run the docker file again, just run:
```
docker run -it --rm --name gcrd gcrd /bin/bash
```
again, and it will start the container again (you will need to pull any updates on it though, because it does not save any changes that you make inside of the container)


To remove the image (if you want to rebuild it) the command you would run is:
```
docker rmi gcrd:latest
```
And to rebuild, you run:
```
docker build -t gcrd .
```

Also note that you should **ONLY** do this if there is a known problem with the upstream repo where 'git pull' doesn't work.

## Getting files from inside the docker container

In the circumstance that you need to get files that are generated inside of the docker container, here is the command:
```
docker cp gcrd:/usr/src/app/general-course-relevency-discovery/path/to/file /path/on/host/
```


