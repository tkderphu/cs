# Note about file systems

# / - Root Directory

- The top-level directory in Linux.

- Every single file or directory starts from here.

- Only the root user has full write permissions here.

- The entire Linux filesystem is organized under this root.


# /bin — Essential User Binaries

Contains basic system commands needed for all users.

Available in single-user mode, used for repair and boot.

Common binaries:

- ls (list files)

- cp (copy files)

- mv (move/rename files)

- rm (remove files)

- cat (concatenate files)

- bash (Bourne Again Shell)

# /sbin — System Binaries

Contains system administration commands, primarily used by root.

Used for booting, repairing, recovering, or mounting filesystems.

Common binaries:

- fsck (filesystem check)

- reboot

- shutdown

- mount, umount

- iptables

- ifconfig (deprecated but still found)

# /boot — Boot Loader Files
Stores the kernel, initramfs, and bootloader (e.g., GRUB) config.

Essential for system startup.

Example files:

/boot/vmlinuz-* → compressed Linux kernel

/boot/initrd.img-* → initial RAM disk image

/boot/grub/ → GRUB config files

# /dev — Device Files
Contains special files that represent hardware devices.

Linux treats everything as a file, including devices.

Managed by udev dynamically.

Examples:

/dev/sda1 → first partition of first disk

/dev/tty → terminal interface

/dev/null, /dev/zero, /dev/random

# /etc — Configuration Files

Contains system-wide config files and shell scripts.

Should not contain binaries.

Common files/directories:

- /etc/passwd → user accounts

- /etc/fstab → filesystem mount table

- /etc/hosts → hostname-IP mapping

- /etc/ssh/sshd_config → SSH server config

- /etc/network/interfaces or /etc/netplan/ → networking config (distro-dependent)

# /home — User Home Directories

Each user has a personal directory under /home/username.

Example: /home/alice, /home/bob

Contains user files, settings (like .bashrc, .profile, etc.)

Users have full control over their home directories.

# /media — Removable Media Mount Point

Temporary mount point for automatically mounted devices like:

- USB drives

- CD/DVDs

When you plug in a drive, it might mount at /media/username/device-label.

# /mnt — Mount Point for Manual Mounting

Used by system administrators to manually mount temporary filesystems.

Example:
```
sudo mount /dev/sdb1 /mnt
```
Not used automatically by the system like /media.

# /opt — Optional Application Software Packages

Third-party applications install here (outside of package manager control).

Example:

/opt/google/chrome/

/opt/vmware/

Often used for commercial or proprietary software.

# /proc — Virtual Filesystem for Kernel & Process Info

Doesn’t contain real files; data is read directly from the kernel.

Used to get info about:

- CPU, memory, hardware

- Running processes (/proc/[PID])

Examples:

- /proc/cpuinfo

- /proc/meminfo

- /proc/uptime

- /proc/[PID]/status

# /run — Runtime Variable Data

Contains info about the current running system.

Created at boot and stored in RAM.

Files disappear on reboot.

Examples:

- /run/lock → lock files

- /run/user/1000 → runtime data for user with UID 1000

# /srv — Service Data
Used to store data served by the system (web, FTP, etc.).

Example:

- /srv/www/ → web server data (e.g., Apache or Nginx)

- /srv/ftp/ → FTP server data

# /sys — System Information Virtual Filesystem

Like /proc, provides hardware and kernel info via a virtual interface.

Interacts with devices, drivers, kernel modules.

Examples:

- /sys/class/net/ → network interfaces

- /sys/block/ → block devices

- /sys/module/ → loaded kernel modules

# /tmp — Temporary Files

Used to store temporary files by apps or users.

Cleared on reboot or periodically.

Anyone can write to /tmp, but files must be secured by ownership/permissions.


# /usr — User Programs and Data

Stands for Unix System Resources.

Contains read-only data, shared across users.

Subdirectories:

- /usr/bin → general user commands (e.g., gcc, vim, python)

- /usr/sbin → admin tools (not for regular users)

- /usr/lib → libraries

- /usr/share → shared data like docs, icons, man pages

- /usr/local/ → user-installed software (not managed by package manager)- 

# /var — Variable Data Files

Contains files that change often, like:

- Logs

- Caches

- Spools

- Temp mail, print jobs

Subdirectories:

- /var/log/ → system and application logs

- /var/spool/ → print queue or mail queue

- /var/cache/ → cached package files (e.g., from APT)

- /var/tmp/ → temporary files that persist across reboots