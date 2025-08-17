# Note about create VPN server

In this practice i will demonstrate how create VPN and use it for accessing to website which is blocked by ISP(or accessing to website which rejected your ip)

# Preparing

I will use two VPS for demonstration:

- VPS1: 103.109.37.70
    
    - This VPS will run nginx and anyone can access to this site exclude this IP: 27.71.120.58(this is my public IP)

To drop request from IP: 27.71.120.58 to VPS1, inside VPS1 I will use this commad:

```
iptables -I INPUT -p tcp -s 27.71.120.58 --sport 80 -j DROP
```

Ok this will be done, so when my laptop access to website nginx of VPS1 i will be rejected.


```
curl http://103.109.37.70 #It's waiting too long
```


- VPS2: 27.71.120.58

    - This VPS i will use for creating a VPN server uses OpenVPN

This is all command for creating VPN server uses OpenVPN:

## 1. Set Up OpenVPN Server

Note: Only for Ubuntu >= 22.04 

Use the official OpenVPN installation script:

```
wget https://git.io/vpn -O openvpn-install.sh
chmod +x openvpn-install.sh
sudo ./openvpn-install.sh
```

The script will ask:
- Protocol: UDP (recommended)

- Port: 1194 (default)

- DNS resolver: Use default (e.g., 1.1.1.1 or Google)

- Name for first client: e.g., client1

It will generate a .ovpn config file in your home directory.

 - Example: /root/client1.ovpn

## 2. Transfer VPN Config File to Client

Use scp or download via SFTP:

```
scp root@your_server_ip:/root/client1.ovpn .
```

## 3. Connect from Client (Windows/Linux/Android/macOS)

In this practice i'm using linux so i will use this command for downloading OpenVPN client and connect OpenVPN server.

```
sudo apt install openvpn #install openvpn client
sudo openvpn --config client1.ovpn # connect to server
```

## 4. Final

You will be able to access blocked websites, because your traffic is tunneled through the VPN server(which isn't blocked by VPS1).

So you can try to access nginx of VPS1 and giving result:

```
curl http://103.109.37.70
```