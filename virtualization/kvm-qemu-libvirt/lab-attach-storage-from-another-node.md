# Lab attach volume from another server to compute server

# Options 1: Using NFS

# What is NFS

Nfs is a distributed file system protocol that lets a client access files over a network as if they are on local storage. It is widely used in Linux/Unix environments for sharing files between servers and clients

# How NFS works

Nfs uses a client-server architecture:

- NFS server: exports(shares directories to clients)
- NFS client: mounts the exported directories and interacts with files.

# Workflow

1. Server exports a directory using /etc/exports
2. Client amounts the directory over the network
3. The client can perform file operations as if the directory is local
4. Server enforces access permissions

# 4. NFS protocol concepts

1. Export directoris: Server defines which directories are shared

- Configured in `/etc/exports/` on linux
- Example:

    ```
    /srv/nfs_share 192.168.1.0/24(rw,sync,no_root_squash)
    ```

    - rw: read/write access
    - sync: write operations are synchronous
    - no_root_squash: root user on client retains root privileges

2. Mounting directories: client accesses shared folders

- Command:

```
sudo mount -t nfs 192.168.1.100:/srv/nfs_share /mnt
```

3. Access control: nfs can use

- Host based controll(ip)
- User mapping(root_suqash, all_squash)
- Kerberos for authentication

4. File locking: support locking to avoid conflicts when multiple clients access the same file.
