# Note about docker

# What is docker

Docker is platform(app) using api from `docker engine` to mange images, networks, containers, volumes

# Docker engine

The core service(`daemon process dockerd`) serves `api` to manage containers, networks, ...etc

# Workflow of docker

1. Docker is like app(client) is used to talks `Docker engine` via rest api is exposed by `Docker engine`

```
[You / CLI]  --->  [Docker Engine API]  --->  [dockerd daemon]  --->  [containers/images]
```

2. Docker engine api

- Rest api running on `/var/run/docker.sock`
- Handles request for:
    - containers management
    - images management
    - volumes/networks management

- Ex: `POST /containers/create`

# Docker under the hood

## 1. Image

- Docker images are made of layers
- It uses `OverlayFS` to stack multiple layers
- Example:
    - Base layer = Ubuntu filesystem
    - Layer 2 = Python installed
    - Layer 3 = your application

## 1.1.1. OverlayFS

- A Linux filesystem that lets you stack directories on top of each other.

- Files are read from the lower layer(s) (read-only), and modifications go to the upper layer (writable).

- The merged view is exposed as a single filesystem.

- Example:

```
mkdir lower upper work merged

# Put something in lower (like base image)
echo "from base layer" > lower/hello.txt

# Mount overlay
mount -t overlay overlay -o lowerdir=lower,upperdir=upper,workdir=work merged

# See merged view
cat merged/hello.txt   # shows "from base layer"

# Modify file in merged
echo "changed in container" > merged/hello.txt

# Now upper has a copy
cat upper/hello.txt
```

- Explain:
    - file `hello.txt` inside lower layer, when it is modified in `merged` folder then that file will be copied to `upper` folder when edit it will edit in `upper` folder

## 1.1.2. Why use OverlayFS

- If you dont use OverlayFS, for every container docker would need to:
    - Crete a full root filesystem(Ubuntun ~200MB) `file system`
    - Copy all files from base image to container
    - Mount it as the root of the processs
- With OverlayFS:
    - Base image layers = read-only(can't be modified(all containers can use it)), stored one
    - Each contain gets a tiny writable layer on top:
        - Ex: You create a new file on `/var/lib`
        - Upper layer will copy the folder of read-only layer in this case upper layer will copy `/var/lib` then when user create new file then it will be stored in `/var/lib` of upper layer and in lower layer it doesn't change(That while lower layer it is used for serving all containers when they need base image)

## 1.1.3. Code example

```
# Assume that this are base folder(image layers)
mkdir -p /tmp/layer1 /tmp/layer2 /tmp/layer3

# Create some files in side image layers

echo "Hello from Layer1" > /tmp/layer1/file1.txt
echo "Hello from Layer2" > /tmp/layer2/file2.txt
echo "Modified in Layer3" > /tmp/layer3/file3.txt

# Now we have 3 read-only files(layers)

# Prepare writable container layer
mkdir -p /tmp/container/upper /tmp/container/work /tmp/container/merged

# Mount overlayFS
sudo mount -t overlay overlay \
  -o lowerdir=/tmp/layer3:/tmp/layer2:/tmp/layer1,upperdir=/tmp/container/upper,workdir=/tmp/container/work \
  /tmp/container/merged

# Look inside

ls /tmp/container/merged
cat /tmp/container/merged/file1.txt
cat /tmp/container/merged/file2.txt

# make change inside container
echo "New file inside container" > /tmp/container/merged/new.txt

ls /tmp/container/upper
cat /tmp/container/upper/new.txt
```

- Explain:
    - `upper`: writable layers(when container create,edit then container will go here)
    - `work`: required by overlayfs
    - `merged`: where final unified view will appear(container will see file system)

- Snapshot(commit as new image layer): `cp -a /tmp/container/upper /tmp/layer`'



## 1.2: Structure in Docker to build image:

```
FROM ubuntu:20.04
RUN apt-get update && apt-get install -y nginx
COPY index.html /var/www/html/
CMD ["nginx", "-g", "daemon off;"]
```

- `FROM`: base layer(read-only)
- `RUN`: executes commands(update repository of container), produces a new layer
- `COPY`: copies files into a new layer(create folder and copy file from host to container)
- `CMD`: metadata only, no layer

- Above set of instructions will be served by docker to build an image

## 1.3: Build ubuntu container without docker

### 1. Download ubutun root file system

```
mkdir -p /tmp/ubuntu
cd /tmp/ubuntu
curl -L http://cdimage.ubuntu.com/ubuntu-base/releases/20.04/release/ubuntu-base-20.04.5-base-amd64.tar.gz -o ubuntu-base.tar.gz
tar -xzf ubuntu-base.tar.gz
```

### 2. Create an isolated process with `unshare`

```
sudo unshare --fork --pid --mount --uts --ipc --net --user --map-root-user chroot /tmp/ubuntu /bin/bash
```

Explaination:

- unshare → create new namespaces

- --pid → new process table (your bash sees only itself)

- --mount → private mount space

- --uts → private hostname

- --net → new empty network stack

- --ipc → private IPC

- --user --map-root-user → makes you root inside the namespace

- chroot /tmp/ubuntu /bin/bash → changes root to Ubuntu filesystem and starts bash

### 3. You're inside ubuntu

Now you’re inside a minimal Ubuntu environment, isolated from host, running from /tmp/ubuntu.

```
cat /etc/os-release
hostname
ps aux
```

- You’ll see only Ubuntu files

- `ps` shows very few processes (your bash only)

- Host processes are invisible

## 2. Network

Docker used `netns, veth, linux bridge, iptables/nftables` for managing network accross container and isolated each of them

When docker create new network then it will create a linux bridge:
- A new interface(port) will be of docker attached to host
- When new container is created and use that network then docker will create a virtual cable to connect container to that linux bridge
- To create network namespace it used `netns` for container
- Linux bridge is running dhcp server for assign ip to vm when it is created
- To host can communicate with container it using `iptables/nftables` to forwarding port
- Docker persists container config in `/var/lib/docker`, when host reboot so `dockerd` recreates the bridge, veth, iptables and namespaces from stored data



```
[Container1 eth0] <-> vethA ---+
                               |--- docker0 (bridge) --- Host eth0
[Container2 eth0] <-> vethB ---+
```

Full:

```
[Container eth0: 172.17.0.2] 
        | 
     vethA
        |
   +------------+
   |  docker0   | (bridge, IP 172.17.0.1)
   +------------+
        |
   Host eth0 (192.168.1.100)
        |
   Internet
```

## 3. Volume

Volume is a persistent storage for storing data, volumes are:
- exist outside the container union filesystem
- store independent of container lifecycle
- are optimized for performance and sharing between containers

### Use volume

```
docker volume create mydata
docker run -v mydata:/data ubuntu
```

- `mydata` → Docker-managed volume on the host

- `/data` → path inside the container

### Type of volume

| Type             | Description                                                                       |
| ---------------- | --------------------------------------------------------------------------------- |
| **Volumes**      | Managed by Docker, stored in `/var/lib/docker/volumes/` (default)                 |
| **Bind mounts**  | Maps a host directory into a container directly (`-v /host/path:/container/path`) |
| **tmpfs mounts** | In-memory filesystem inside container (`--tmpfs`)                                 |

### Volume under the hood

Docker using `mount`, `mount --bind` to persistent data inside of containers by mount it in host machine:

```
# Create mount point inside Ubuntu rootfs
mkdir -p /tmp/ubuntu/data

# Mount host folder into Ubuntu rootfs
mount --bind /tmp/host-data /tmp/ubuntu/data
```
## 4. Container
