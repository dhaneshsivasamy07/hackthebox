# Docker Commands

- Installation, scripts can be found [`here`](https://github.com/cyberwr3nch/hackthebox/tree/master/scripts/installation)

- Building a docker file
```bash
# When a Dockerfile is found in a repository, build the docker image
docker build -t <tagname> .
```

- Downloading a docker file
```bash
# pull the latest version
docker pull <container name>
# pull a specific version
docker pull <container name>:<verion>
```

- Running a docker
```bash
# listing the docker images 
docker images 

# running the container
docker run -it <dockername>
```

- Removing the container
```bash
# list the images to find the image ID
docker rmi <imageID> -f
```

- List running docker instances
```bash
docker ps
```

- Update the Docker when its contents have been altered
```bash
docker update
```

- Run a docker with ports open
```bash
docker run --rm -it -p <port on docker container>:<port on docker host> -p <port start>-<port end>:<port start>-<port end> <imageName>
# single port 
docker run --rm -it -p 21:21 <imageName>
# continuous multiple ports
docker run --rm -it -p 21:21 -p 4559-4564:4559-4564 <imageName>
```


##### Resources:
- Docker Chear Sheet by [wsargent](https://github.com/wsargent/docker-cheat-sheet/blob/master/README.md)
