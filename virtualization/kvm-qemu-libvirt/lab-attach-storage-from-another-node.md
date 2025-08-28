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


# Attach disk to virtual machine

In qemu/libvirt to managing volume using `virsh pool`

## check storage pool

```
virsh pool-list --all
```

- Show all defined pools, including active and inactive ones

## Show detailed infomation about a pool

```
virsh pool-info <pool-name>

##show xml configuration

virsh pool-dumpxml <pool-name>
```

## Start/stop/autostart

```
virsh pool-start <pool-name>
virsh pool-destroy <pool-name>   # stop pool (doesn't delete definition)
virsh pool-autostart <pool-name> # enable autostart on host boot
```

## Create/define/delete

- create temporary pool

```
virsh pool-create pool.xml
```

- define a peristent pool

```
virsh pool-define pool.xml
```

- delete pool definition

```
virsh pool-undefine <pool-name>
```

- delete pool and storage

```
virsh pool-delete <pool-name>
```

## Refresh/build/rebuild

```
virsh pool-refresh <pool-name>   # refresh contents
virsh pool-build <pool-name>     # create storage backend (mkdir, etc.)
```

## Manage volumes in pool

- List volumes

```
virsh vol-list <pool-name>
```

- create avolume

```
virsh vol-create <pool-name> volume.xml
```

- delete volume

```
virsh vol-delete <volume-name> <pool-name>
```

- pool xml:

```
<pool type='netfs'>
  <name>nfs-pool</name>
  <source>
    <host name='192.168.10.135'/> # source
    <dir path='/var/lib/virtual-machine/volumes'/> # share file
    <format type='nfs'/>
  </source>
  <target>
    <path>/var/lib/libvirt/nfs-pool</path>
  </target>
</pool>
```

# Attach new disk to vm

- Command:

```
virsh attach-disk <vm-name> <source-volume> <device name> --persistent --subdriver qcow2
```

- Ex: 

```
virsh attach-disk my-ubuntu-vm /var/lib/libvirt/images/new-disk.qcow2 vdb --persistent --subdriver qcow2
```

- vdb: This is the target device name the disk will have inside the guest operating system. The vd* naming convention is standard for virtio block devices.

- `--persistent`: This crucial flag ensures the disk is not just attached temporarily. 

- `--subdriver qcow2`: This flag explicitly tells libvirt and QEMU the format of the disk image you are attaching

