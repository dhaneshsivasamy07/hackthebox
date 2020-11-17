### Docker Installation
<p align="center">
  <img src="https://github.com/cyberwr3nch/hackthebox/blob/master/scripts/files/docker.png" >
</p>

#### Linux

<p align="center">
  <img height=300 width=300 src="https://upload.wikimedia.org/wikipedia/commons/6/66/Openlogo-debianV2.svg" >
</p>

Installing the **docker.io**:
`sudo apt-get install docker.io`
>docker.io provided by debian might lag behind

Installing the docker **community edition**:
```bash
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -

echo 'deb [arch=amd64] https://download.docker.com/linux/debian buster stable' | sudo tee /etc/apt/sources.list.d/docker.list

sudo apt update

sudo apt remove docker docker-engine docker.io -y

sudo apt install docker-ce -y
```
or this can be simplified by the following script

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

#### Parrot OS

<p align="center">
  <img width=300 height=300 src="https://github.com/cyberwr3nch/hackthebox/blob/master/scripts/files/parrotOs.png" >
</p>

Installing the **docker.io**:
`sudo apt-get install docker.io`
>docker.io provided by debian might lag behind

Installing the docker **community edition**:
```bash
sudo apt-get remove docker docker-engine docker.io containerd runc

sudo apt-get update

sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -

# editing the /etc/apt/sources.list file
sudo vi /etc/apt/sources.list

# adding the docker repository in the sources.list file
deb [arch=amd64] https://download.docker.com/linux/debian buster stable

# save and exit the /etc/apt/sources.list file
sudo apt-get update
# now newly two repos will show up for docker

sudo apt-get install docker-ce docker-ce-cli containerd.io
```

#### Windows

<p align="center">
  <img width=300 height=300 src="https://github.com/cyberwr3nch/hackthebox/blob/master/scripts/files/windows.png" >
</p>

- For windows the executable file can be obtained from [here](https://hub.docker.com/editions/community/docker-ce-desktop-windows/)
