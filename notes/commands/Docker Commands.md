# Docker Commands

- Installation, can be found [`here`](https://github.com/cyberwr3nch/hackthebox/blob/master/notes/commands/softwareInstalltion/docker.md)

- Building a docker file
```bash
# When a Dockerfile is found in a repository, build the docker image
docker build -t <tagname> .
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

##### Resources:
- Docker Chear Sheet by [wsargent](https://github.com/wsargent/docker-cheat-sheet/blob/master/README.md)
