# What is vnc

vnc(virtual network computing) is a protocol that allows:

Remote viewing and controlling another computer's screen over a network

it sends:

- screen pixels
- keyboard events
- mouse events

=> intead of monitor and keyboard are plugged into vm we get remote monitor + keyboard over TCP

# How vnc works internally

```VM side```

When a VM starts:

```
QEMU/KVM
 ├─ CPU
 ├─ RAM
 ├─ Disk
 └─ Virtual GPU (framebuffer)
```

QEMU:

- Captures screen pixels

- Opens TCP port (5900+)

- Streams framebuffer

- Receives keyboard/mouse

## Client side

A VNC client:

- connects to TCP

- decodes framebuffer

- displays screen

- sends input back

## Default port:

```
Display :0 → 5900
Display :1 → 5901
Display :2 → 5902
```

# Problems with pure VNC    

browser can't speak vnc

browser support:

- http
- websocket

Browsers do not support:

- raw tcp

But vnc = raw tcp, as a result can't open vnc in browser directly

# What is noVNC 

noVNC is a browser-based VNC client written in JS

it allow broswer can open VNC

```
Browser → WebSocket → websockify → TCP → VNC
```

## What is websockify

websockify is protocol which convert websocket data to tpc data.

```
Browser → WebSocket
websockify → TCP
QEMU → VNC
```

## Responsibilities

websockify:

- accepts WebSocket

- unwraps frames

- forwards to VNC port

- returns responses

It’s just a translator, not a renderer.

architecture:

```
Browser
   ↓
noVNC (JavaScript)
   ↓ WebSocket
websockify (6080)
   ↓ TCP
QEMU VNC (5900+)
   ↓
VM screen
```

# Security practices

Bind VNC locally

```
listen=127.0.0.1
```

Never expose 5900 publicly.

Use tokens

```
token: host:port
```

Never direct access.

HTTPS

Use Nginx:

```
https://console.example.com
```

Expire tokens

```
5–10 minutes.
```

# Setup NoVNC step by step

## 1. confirm vnc works in vm

```
virsh vncdisplay <vm-id>
127.0.0.1:0

ss -lntp | grep 5900
```

## 2. install noVNC + websockify

on compute server:

```
apt update
apt install -y novnc websockify

//it's file will be located at
ls /usr/share/novnc
```

## 3. quick test

```
websockify \
  --web /usr/share/novnc \
  6080 \
  127.0.0.1:5900
```

open browser:

```
http://SERVER_IP:6080/vnc.html
```

if you see vm console  => success

# 4. secure with token auth

never expose raw console publicly

## 4.1 create token directory

```
mkdir -p /etc/novnc/tokens
chmod 700 /etc/novnc/tokens
```

## 4.2 create token file

```
nano /etc/novnc/tokens/console.token
```

example:

```
vm-101:127.0.0.1:5900
```

no spaces

## 4.3 start websockify with tokens

```
websockify \
  --web /usr/share/novnc \
  --token-plugin TokenFile \
  --token-source /etc/novnc/tokens/console.token \
  6080
```

## 4.4 open secure console

```
http://SERVER_IP:6080/vnc.html?token=vm-101
```

# 5. run as system service

create service:

```
nano /etc/systemd/system/novnc.service
```

paste:

```
[Unit]
Description=noVNC Console Gateway
After=network.target

[Service]
ExecStart=/usr/bin/websockify \
  --web /usr/share/novnc \
  --token-plugin TokenFile \
  --token-source /etc/novnc/tokens/console.token \
  6080
Restart=always
User=root

[Install]
WantedBy=multi-user.target
```

Enable:

```
systemctl daemon-reexec
systemctl enable novnc
systemctl start novnc
```

# 6 firewall

allow only web port:

```
ufw allow 6080/tcp
```

never open port: 5000-59999 those must stay in local