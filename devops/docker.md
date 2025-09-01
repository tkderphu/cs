# Note about docker

# 📑 Table of Contents

- [Note about docker](#note-about-docker)
- [What is docker](#what-is-docker)
- [Docker engine](#docker-engine)
- [Workflow of docker](#workflow-of-docker)
- [Docker under the hood](#docker-under-the-hood)
  - [1. Image](#1-image)
    - [1.1.1. OverlayFS](#111-overlayfs)
    - [1.1.2. Why use OverlayFS](#112-why-use-overlayfs)
    - [1.1.3. Code example](#113-code-example)
  - [1.2: Structure in Docker to build image](#12-structure-in-docker-to-build-image)
  - [1.3: Build ubuntu container without docker](#13-build-ubuntu-container-without-docker)
    - [1. Download ubutun root file system](#1-download-ubutun-root-file-system)
    - [2. Create an isolated process with unshare](#2-create-an-isolated-process-with-unshare)
    - [3. You're inside ubuntu](#3-youre-inside-ubuntu)
  - [2. Network](#2-network)
  - [3. Volume](#3-volume)
    - [Use volume](#use-volume)
    - [Type of volume](#type-of-volume)
    - [Volume under the hood](#volume-under-the-hood)
  - [4. Container](#4-container)
  - [2. Linux features behind containers](#2-linux-featres-behind-containers)
    - [1. Namespaces (process isolation)](#1-namespaces-process-isolation)
    - [2. Cgroups (resource control)](#2-cgroups-resource-control)
  - [3. File system](#3-file-system)
  - [4. Network](#4-network)
    - [1. Bridge network (default)](#1-bridge-network-default)
    - [2. Host network](#2-host-network)
    - [3. Overlay network](#3-overlay-network)
    - [4. Macvlan](#4-macvlan)
    - [5. Process lifecycle](#5-process-lifecycle)
    - [6. How a container is created (under the hood)](#6-how-a-container-is-created-under-the-hood)

- [Docker commands](#docker-commands)
  - [1. Docker system commands](#1-docker-system-commands)
  - [2. Image commands](#2-image-commands)
  - [3. Container commands](#3-container-commands)
  - [4. Volume Commands](#4-volume-commands)
  - [5. Network Commands](#5-network-commands)
  - [6. Dockerfile Instructions (image build)](#6-dockerfile-instructions-image-build)
  - [7. Logs / Debug](#7-logs--debug)
  - [8. Summary of Internals](#8-summary-of-internals)


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

A container is a lightweight, portable enviroment that runs application with:

- Isolated processes
- Separate filesystem
- Isolated network interfaces
- Independent hostname/UTS

| Feature      | VM                        | Container           |
| ------------ | ------------------------- | ------------------- |
| Kernel       | Separate (full OS)        | Shared with host    |
| Size         | Large (GBs)               | Small (MBs)         |
| Startup time | Slow (seconds to minutes) | Fast (milliseconds) |
| Isolation    | Full hardware virtual     | Namespace + cgroups |

Containers share the host kernel but isolate everything else.

## 2. Linux featres behind containers

Docker (and most container runtimes) rely on two main kernel features:

### 1. Namespaces (process isolation)

- pid → process IDs inside container

- mnt → mount points (rootfs)

- net → network interfaces

- uts → hostname and domain

- ipc → interprocess communication

- user → UID/GID mapping

- cgroup → resource limitation

### 2. Cgroups (resource control)

- Limit CPU, memory, IO usage

- Track container resource usage

- Prevent one container from starving others

## 3. File system

Containers use a copy-on-write (CoW) filesystem:

- OverlayFS is most common

    - Base layers come from images (read-only)

    - Container layer is read-write, on top

- Benefits:

- Lightweight → multiple containers can share same base image

- Efficient → only changes are stored in container layer

Optional volumes for persistent data:

    - Mounted outside overlayfs

    - Direct host access

    - Shared between containers

## 4. Network

Containers can have:

### 1. Bridge network (default)

- Each container gets a veth interface

- Connected to host bridge (like docker0)

- Host NAT provides internet access

### 2. Host network

- Container shares host’s network stack

- No isolation

### 3. Overlay network

- Used in multi-host Docker swarm

- Encapsulated traffic via VXLAN

### 4. Macvlan

- Each container gets a unique MAC/IP on LAN

### 5. Process lifecycle

- Container runs processes like a normal Linux process, but in isolated PID namespace

- The first process (PID 1) in the container is special:

    - Handles signals (like Ctrl+C, termination)

    - If PID 1 dies, the container exits

- Processes cannot see host processes (unless using host PID namespace)

### 6. How a container is created (under the hood)

Simplified steps:

- Pull an image (tarball with layers)

- Create a container layer on top (read-write)

- Create namespaces:

    - PID, mount, network, UTS, IPC, user

- Mount overlayfs (image layers + container layer) as rootfs

- Setup network namespace + interfaces

- Setup cgroups (CPU, memory, blkio limits)

- Launch init process (e.g., /bin/bash or your app) in the namespaces


# Docker commands

# 1. Docker system commands

| Command               | Usage                                | Details / Under the Hood                                                                                                                             |
| --------------------- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `docker version`      | Shows Docker client & server version | Queries Docker daemon via API, returns info about versions of components.                                                                            |
| `docker info`         | Shows system-wide info               | Returns info about images, containers, volumes, networks, storage driver (overlayfs), cgroup info, kernel version.                                   |
| `docker system df`    | Shows disk usage                     | Shows space used by images, containers, volumes, and build cache.                                                                                    |
| `docker system prune` | Deletes unused objects               | Cleans up dangling containers, images, networks, and optionally volumes. Docker removes overlayfs layers, deletes mount points, and cleans metadata. |

## 2. Image commands

| Command                       | Usage                        | Under the Hood                                                                                                                                 |
| ----------------------------- | ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `docker pull <image>`         | Download image from registry | Docker pulls image layers (tarballs) from registry. Layers are stored in `/var/lib/docker` and indexed by content hash.                        |
| `docker images`               | List local images            | Queries Docker’s local storage driver (overlayfs layers + metadata) to display available images.                                               |
| `docker rmi <image>`          | Remove image                 | Deletes image metadata and layer references. Layers are only deleted if no container uses them.                                                |
| `docker build -t <name> .`    | Build image from Dockerfile  | Docker parses Dockerfile, executes each instruction in a temporary container, stores changes as **layer** (overlayfs), commits layer to image. |
| `docker tag <image> <newtag>` | Retag image                  | Updates image metadata. No copy of filesystem layer; only new reference.                                                                       |
| `docker push <image>`         | Push image to registry       | Pushes image layers (tarballs) to registry, layer-by-layer, only new layers sent.                                                              |


Under the hood:

- Docker image = stacked overlayfs layers

- Each Dockerfile instruction (RUN, COPY) creates a new read-only layer

- Container adds read-write layer on top when running

## 3. Container commands

| Command                             | Usage                        | Under the Hood                                                                                                                                                            |
| ----------------------------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `docker run <image>`                | Create and start container   | Docker creates container namespace (PID, mount, network, UTS, IPC, user), allocates overlayfs writable layer, sets up network, cgroups, mounts volumes, and starts PID 1. |
| `docker ps`                         | List running containers      | Queries Docker daemon, displays container ID, name, status, ports, network, image.                                                                                        |
| `docker ps -a`                      | List all containers          | Includes stopped containers, info comes from Docker metadata.                                                                                                             |
| `docker stop <container>`           | Stop container               | Sends SIGTERM to PID 1, waits, then SIGKILL. Overlayfs layer remains; container paused.                                                                                   |
| `docker start <container>`          | Start stopped container      | Restores namespace, mounts overlayfs, reattaches network, restarts PID 1.                                                                                                 |
| `docker restart <container>`        | Stop + start                 | Combines stop/start sequence.                                                                                                                                             |
| `docker rm <container>`             | Remove container             | Deletes container overlayfs layer, unmounts volumes, removes metadata.                                                                                                    |
| `docker exec -it <container> <cmd>` | Run command inside container | Docker enters container namespaces (PID, mount, net, etc.) and executes command in running container.                                                                     |
Namespaces and overlayfs are key:

- Overlayfs = container layer

- Namespaces = isolation

- cgroups = resource limits

## 4. Volume Commands

| Command                        | Usage                       | Under the Hood                                                                                                   |
| ------------------------------ | --------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `docker volume create <name>`  | Create volume               | Creates directory in `/var/lib/docker/volumes/<name>/_data` with metadata `config.json`.                         |
| `docker volume ls`             | List volumes                | Shows Docker-managed volumes.                                                                                    |
| `docker volume inspect <name>` | Show volume info            | Returns mount path and container references.                                                                     |
| `docker volume rm <name>`      | Delete volume               | Deletes volume directory and metadata. Data inside host filesystem is gone.                                      |
| `docker run -v <volume>:/path` | Mount volume into container | Uses **bind mount** under the hood: host path `/var/lib/docker/volumes/<volume>/_data` → container path `/path`. |

## 5. Network Commands

| Command                                           | Usage                       | Under the Hood                                                       |
| ------------------------------------------------- | --------------------------- | -------------------------------------------------------------------- |
| `docker network create <name>`                    | Create network              | Creates Linux bridge or overlay network, sets up subnet, gateway.    |
| `docker network ls`                               | List networks               | Shows Docker-managed networks.                                       |
| `docker network inspect <name>`                   | Network info                | Returns container attachments, IPAM config, bridge info.             |
| `docker network connect <network> <container>`    | Attach container to network | Creates veth pair, attaches container namespace interface to bridge. |
| `docker network disconnect <network> <container>` | Detach container            | Removes veth interface from container network namespace.             |


## 6. Dockerfile Instructions (image build)


| Instruction        | Usage                     | How it works under the hood                                                           |
| ------------------ | ------------------------- | ------------------------------------------------------------------------------------- |
| `FROM <image>`     | Base image                | Pulls base layers, sets initial rootfs.                                               |
| `RUN <cmd>`        | Execute command           | Runs command inside temporary container, commits overlayfs layer.                     |
| `COPY <src> <dst>` | Copy files                | Adds files from build context into temporary container layer.                         |
| `ADD <src> <dst>`  | Like COPY + tar/extract   | Adds and optionally unpacks archives.                                                 |
| `CMD`              | Default container command | Stored in image metadata, executed by default if no command provided in `docker run`. |
| `ENTRYPOINT`       | Fixed container command   | Image metadata, always executed (can combine with CMD arguments).                     |
| `WORKDIR`          | Set working directory     | Mounts and sets container current working dir.                                        |
| `EXPOSE`           | Document ports            | Metadata only; does not open firewall.                                                |

## 7. Logs / Debug

| Command                      | Usage                        | Details                                                       |
| ---------------------------- | ---------------------------- | ------------------------------------------------------------- |
| `docker logs <container>`    | Show container stdout/stderr | Docker attaches to container’s stdout/stderr pipes.           |
| `docker attach <container>`  | Connect to running container | Connects terminal to container namespace TTY.                 |
| `docker inspect <container>` | Low-level metadata           | Shows overlayfs mount, namespaces, cgroups, network, volumes. |

## 8. Summary of Internals

- Images: stacked overlayfs layers

- Containers: namespaces + cgroups + overlayfs + volumes + network

- Volumes: bind mounts from host, persistent storage

- Network: network namespaces, veth pairs, bridges, NAT

- Runtime: Docker daemon + containerd + runc (creates Linux process with isolation)