# How to run this docker file

First you need to make sure that you have docker installed, and you can do that by heading over to their site, they have two guides, one for [windows](https://docs.docker.com/docker-for-windows/install/) and one for [macs](https://docs.docker.com/docker-for-mac/install/).

Note for the windows people: you will need to have pro, enterprise, or education edition of windows ten, as well as have hyperv.

If you are on windows home you can follow the guide [here](https://docs.docker.com/docker-for-windows/install-windows-home/) to get up and running, it will involve a bit more work on your end.


Next you need to make sure that you are in this directory on a terminal emulator of some sort, for macs that would be the terminal, and for windows people you could use either the terminal that comes with git, or the command prompt.

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
