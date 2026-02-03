# What is ssl/tls

TLS is protocol that encrypts network communication

used for:

- https
- wss(websocket secure)
- ftps
- stmp tls

why need:

if we dont use ssl so when data is transfered via network they actually is plain text as a result hacker can know about the information.

# Tls handshake

When you open and write a url like this: https://example.com

## Step 1 client send message to server

```
Hi
I support TLS 1.3
Here are my ciphers
Here is random number A
```

## step 2 server replies

```
Hi
I support TLS 1.3
Here are my ciphers
Here is random number A
```

## step 3 certificate verification

```
Browser checks:

✔ Domain match?

example.com ?

✔ Trusted CA?

Let's Encrypt trusted?

✔ Expired?
✔ Revoked?
```

If fail:  ```⚠️ Not Secure```

## step 4 Key exchange

browser:

```
create session key
encrypt with server public key
send
```

server:

```
decrypt with private key
```

Now both of them share the same secret key

## Step 5 — Real communication begins

now both use:

```
AES(random_key)
```

for everything else like cookie, json, password, ...etc



# Setup ssl/tls with certbot

## Install dependencies

```
sudo apt update
sudo apt install certbot python3-certbot-nginx
```

## Nginx before https

```
server {
    listen 80;
    server_name api.phu.dev;

    location / {
        proxy_pass http://localhost:3000;
    }
}
```

## Run certbot

```
sudo certbot --nginx -d api.phu.dev
```

## What happen internally

## step 1: Certbot talks to Let’s Encrypt

Certbot says:

```
“Hey Let’s Encrypt, I want a cert for api.phu.dev”
```

## Step 2: Domain ownership challenge (HTTP-01)

Let’s Encrypt replies:

```
“Prove that you control api.phu.dev”
```

Certbot:

- Creates a temporary file:

```
/.well-known/acme-challenge/XYZ123
```

- Modifies Nginx config temporarily

Let’s Encrypt checks:

```
http://api.phu.dev/.well-known/acme-challenge/XYZ123
```

If Let’s Encrypt can access it → you own the domain

This is real TLS authentication in action

## Step 3: Certificate is issued


Let’s Encrypt generates:

- Server certificate

- Intermediate certificate

Certbot stores them in:

```
/etc/letsencrypt/live/api.phu.dev/
```

Files:

```
fullchain.pem  → server cert + chain
privkey.pem    → PRIVATE KEY (SECRET!)
cert.pem
chain.pem
```

## Nginx after certbot

```
server {
    listen 443 ssl;
    server_name api.phu.dev;

    ssl_certificate /etc/letsencrypt/live/api.phu.dev/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.phu.dev/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
    }
}
```

Also adds:

```
server {
    listen 80;
    server_name api.phu.dev;
    return 301 https://$host$request_uri;
}
```

## Browser connection (real TLS flow)

When user opens:

```
https://api.phu.dev
```

Browser does:

- TLS handshake

- Receives certificate

Verifies:

- Domain matches

- Signed by Let’s Encrypt

- Chain is trusted

- Not expired

## Renew certificates

```
sudo certbot renew --dry-run
```