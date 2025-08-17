# Note about VPN

# 1. What is VPN

A VPN is a technology that:

- Encrypts your internet traffic,

- Tunnels it securely through the public internet,

- And routes it via a remote server.

- You appear to be browsing from the VPN server, not your own device, and no one between your device and the server can read your traffic.

# 2. Core Functions of VPN

| Function           | Description                                                  |
| ------------------ | ------------------------------------------------------------ |
| **Encryption**     | Scrambles data so others can’t read it.                      |
| **Tunneling**      | Encapsulates private traffic within a public protocol.       |
| **Authentication** | Ensures only authorized users can connect.                   |
| **IP Masking**     | Hides your real IP address, provides a new one.              |
| **Data Integrity** | Protects against tampering (via HMAC or digital signatures). |
| **Secure Routing** | Routes traffic through a trusted server.                     |


#  3. Core Components

| Component                 | Role                                                                                 |
| ------------------------- | ------------------------------------------------------------------------------------ |
| **VPN Client**            | The software on your device that initiates the VPN connection.                       |
| **VPN Server**            | The endpoint that decrypts traffic and sends it to the internet or internal network. |
| **VPN Protocol**          | The set of rules used to establish the secure connection.                            |
| **Tunneling Mechanism**   | Wraps private packets inside a public protocol (e.g., TCP/UDP).                      |
| **Encryption Algorithm**  | Ensures data confidentiality (e.g., AES, ChaCha20).                                  |
| **Authentication Method** | Ensures only verified users can connect (certs, keys, passwords).                    |


# 4. VPN Architecture

## 1. Client-to-Site VPN (Remote Access)
Used when individuals connect to a company/private network from anywhere.

```
[User Device] ⇄ [Encrypted Tunnel] ⇄ [VPN Server] ⇄ [Internal Network]
```

## 2. Site-to-Site VPN

Used when two offices or networks are connected over a secure VPN tunnel.

```
[Office A Network] ⇄ [VPN Gateway A] ⇄ [Tunnel] ⇄ [VPN Gateway B] ⇄ [Office B Network]
```

## 3. Internet Privacy 

Used by individuals to access the internet anonymously or bypass censorship.
    
```
[User Device] ⇄ [VPN Server in another country] ⇄ [Internet]
```

# 5. VPN Protocols

| Protocol              | Description                                  | Strength                      | Weakness                                  |
| --------------------- | -------------------------------------------- | ----------------------------- | ----------------------------------------- |
| **OpenVPN**           | Open-source, uses TLS/SSL                    | Very secure, widely supported | Moderate speed                            |
| **WireGuard**         | New protocol using modern crypto             | Extremely fast and simple     | Still maturing, limited in some platforms |
| **IPSec**             | IP-layer security (often with L2TP or IKEv2) | Very secure, stable           | Complex to set up                         |
| **IKEv2/IPSec**       | Great for mobile (reconnects fast)           | Secure and fast               | Limited support in Linux                  |
| **SSTP**              | Tunnels via HTTPS (TCP 443), Microsoft       | Good for bypassing firewalls  | Windows-centric                           |
| **PPTP** (Deprecated) | Fast but insecure                            | Legacy only                   | Weak encryption, easily broken            |
| **SSL VPN**           | Runs over HTTPS, browser-friendly            | Clientless access possible    | Mostly for web apps                       |


# 6. VPN Use Cases 

## 1. Privacy & Anonymity

- Problem: ISPs log your browsing.

- Solution: VPN encrypts traffic; no one sees what sites you visit.

## 2. Bypass Censorship

- Problem: Government blocks Facebook/YouTube.

- Solution: Use a VPN server outside the country.

## 3. Access Geo-blocked Content

- Problem: Netflix US not available in Vietnam.

- Solution: VPN to a US server lets you access US content.

## 4. Remote Work

- Problem: Employee needs to access office intranet.

- Solution: VPN connects securely to company network.

## 5. Secure Cloud Access

- Problem: Connect to AWS VPC privately.

- Solution: Cloud VPN gateways like AWS Client VPN, OpenVPN Access Server.

# 7. How VPN Works

## 1. Handshake (Initial Contact & Authentication)

## 1.1: Client initiates connection

The VPN client (e.g., OpenVPN) reads the config file (e.g., client.ovpn) which contains:

- Server address

- Port (e.g., UDP 1194 or TCP 443)

- Protocols supported (e.g., TLS 1.2, 1.3)

- It opens a TCP or UDP socket to the server IP and port.

- It initiates a TLS handshake by sending a ClientHello message.

ClientHello Message Contains:

| Field                        | Description                                                  |
| ---------------------------- | ------------------------------------------------------------ |
| 🗓 **Client random**         | A 32-byte random number (used in key derivation).            |
| 🔐 **Supported ciphers**     | List of encryption algorithms (e.g., AES-256-GCM, ChaCha20). |
| 🔑 **Key exchange methods**  | ECDHE, DHE, etc.                                             |
| 🔐 **Signature algorithms**  | e.g., RSA, ECDSA                                             |
| 🔄 **Compression methods**   | Usually none for VPNs                                        |
| 📜 **Supported TLS version** | e.g., TLS 1.2 or 1.3                                         |
| 🆔 **Optional extensions**   | Server name (SNI), supported groups, ALPN                    |



This is the client saying:
```
"Hello, I want to start a secure session. Here are the algorithms I support and some random data for key generation."
```

## 1.2: Server responds

Once the server receives the ClientHello, it sends:

## 1. X.509 Certificate

- Contains:

    - Server's public key.

    - Server's identity (CN = Common Name like vpn.example.com).

    - Signed by the CA.

    - Expiration date, algorithms, and other metadata.

- Used to prove server's identity and deliver its public key.


## 2. Server Random

- Another 32-byte random number.

- Combined with the client random later to derive symmetric session keys.

## 3. Chosen Cipher & Parameters

- The server picks one cipher suite from the list provided by the client.

Example:

```
TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
```
- ECDHE: Ephemeral Elliptic Curve Diffie-Hellman key exchange

- RSA: used to verify server’s identity (sign the certificate)

- AES-256-GCM: symmetric encryption

- SHA384: hashing/integrity check

## 4. Key Exchange Public Value

If using ECDHE or DHE: the server sends its public Diffie-Hellman (DH) or elliptic curve (EC) key.

## 1.3: Client authenticates the server

The client now receives the server’s certificate and begins verifying it.

Certificate Validation Steps:

## 1. Signature Verification

- Uses the CA’s public key (ca.crt) to verify the digital signature on the server's certificate.

- This proves the cert was issued by a trusted CA.

## 2. Validity Period

- Check that the certificate is not expired and not yet valid.

## 3. Revocation Check (optional)

- Check if the certificate is in a CRL (Certificate Revocation List) or via OCSP.

- Not commonly done in OpenVPN unless explicitly configured.

## 4. Hostname/Identity Match (if SNI is used)

- Verify that the certificate's Common Name (CN) or SAN (Subject Alternative Name) matches the expected server name.

    - e.g., vpn.example.com

If All Checks Pass:

- Client trusts the server.

- TLS handshake continues to key exchange and tunnel creation.

## Diagram overview

```
[Client] ──(ClientHello: ciphers, key methods, client_random)──▶ [Server]
        ◀─(ServerHello: cert, server_random, cipher, public key)──

            [Client]
           - Verifies cert:
               - Signed by CA?
               - Not expired?
               - CN matches?
           - If OK → Proceed
```