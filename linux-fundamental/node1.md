# Vocabulary
1. concise(kənˈsīs): rõ ràng(vắn tắt rõ ràng)


# Systemd

Systemd is the init system used by most modern Linux distributions (Ubuntu, Debian, Fedora, Arch, etc.). It:

- Boots your system

- Starts/stops services

- Manages system states

- Handles logging via journald

## Key Concepts

| Term        | Description                                                |
| ----------- | ---------------------------------------------------------- |
| **Unit**    | A configuration file (like a service, mount, socket, etc.) |
| **Service** | A background process (like `ssh`, `nginx`)                 |
| **Target**  | A group of units (like `multi-user.target`)                |

## Common Systemd Commands

### 1. Check status, start, stop, restart service
```
sudo systemctl status nginx # check nginx status
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
```

### 2. Enable/Disable service at boot

```
sudo systemctl enable apache2
sudo systemctl disable apache2
```

### 3. Check if service is enabled

```
systemctl is-enabled docker
```

### 4. List of running services

```
systemctl --type=service
```

### 5. List failed services

```
systemctl --failed
```

## Systemd Unit Files

Located in:

- /etc/systemd/system/ – for custom user/system overrides

- /lib/systemd/system/ – system-provided unit files

A typical .service file:

```
[Unit]
Description=My Custom App
After=network.target

[Service]
ExecStart=/usr/bin/myapp
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

To use it:

```
sudo systemctl daemon-reexec       # if systemd itself updated
sudo systemctl daemon-reload       # reload unit files
sudo systemctl enable myapp
sudo systemctl start myapp
```

## Journal Logs with Systemd

Systemd uses journald for logging.

### View logs for a service:

```
journalctl -u nginx
```

### Show real-time logs (like tail -f)

```
journalctl -u nginx -f
```

### View logs since boot:

```
journalctl -b
```

# Archives and compression

# 1. tar – Tape Archive (archiving only)


- Use: Combines multiple files into a single archive file (not compressed by default).

- Common extension: .tar

```
# Create archive
tar -cvf archive.tar file1 file2 dir/

# Extract archive
tar -xvf archive.tar

# List contents
tar -tvf archive.tar
```


- c: create

- x: extract

- v: verbose(show detail output about operation)

- f: file (specifies the archive file name)


# 2. gzip – Compression (often used with tar)

- Use: Compresses a single file using .gz format.

- Common extension: .gz

```
# Compress a file
gzip file.txt     # Creates file.txt.gz and deletes original

# Decompress a file
gunzip file.txt.gz
```

## Tip

- To archive and compress with tar and gzip:

```
tar -czvf archive.tar.gz file1 dir/
tar -xzvf archive.tar.gz       # extract
```

- z: use gzip compression

# 3. zip – Archive + Compression (Windows-compatible)

- Use: Archives and compresses files into .zip. Popular on Windows.

```
# Create a zip archive
zip archive.zip file1 file2 dir/

# Extract a zip archive
unzip archive.zip
```

# 4. xz – High-ratio compression

- Use: Compresses single files with better compression than gzip.

- Common extension: .xz

```
# Compress a file
xz file.txt      # Creates file.txt.xz and deletes original

# Decompress a file
unxz file.txt.xz
```

## Tip

To use tar with xz:

```
tar -cJvf archive.tar.xz dir/
tar -xJvf archive.tar.xz       # extract
```

- J: use xz compression


# Mount

