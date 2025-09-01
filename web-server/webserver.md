# Note about Web server

# What is a web server

A web server is both:

1. Software - a program that listens for http/https requests from client(via web browers) and sends back responses

2. Hardware - a machine that runs this software and stores/delivers the website's file or forwards requests to backend applications

# How a web server works

1. You type https://example.com in a browser.

2. DNS translates example.com → server’s IP.

3. The browser sends an HTTP/HTTPS request to the server.

4. The web server software (e.g., Nginx) receives the request.

5. It checks its configuration:

- If the request is for static content (HTML, CSS, images, JS), it serves it directly from disk.

- If the request is for dynamic content (like a Java, Node.js, Python app), it forwards it to the backend application (reverse proxy mode).

6. The response is returned to the browser.

# Main functions of a web server

- Serve Static Content (HTML, CSS, JS, images).

- Reverse Proxy (forward dynamic requests to backend apps).

- Load Balancing (distribute traffic across multiple servers).

- Security (TLS/SSL for HTTPS, request filtering, firewalls).

- Caching (store frequent responses to reduce backend load).

- Logging & Monitoring (record client activity).

# Common web servers

- Nginx
- Apache http server

# Nginx

## What is nginx

Nginx is a high-performance web server and reverse proxy designed for:

- Serving static content
- Acting as a reverse proxy to backend
- Load balancing traffic across multiple servers
- Handling TLS/SSL termination
- Acting as an API gateway or mail proxy

## Nginx core components

## 1. Master & Worker processes

- Master process: starts and manages workers, read config
- Worker processes: handle connection(each worker can handle thousands of requests asynchronously)

## 2. Configuration(nginx.conf)

- Organized into blocks -> `main`, `http`, `server`, `location`

- Hierarchical structure

```
http {
    server {
        listen 80;
        server_name example.com;

        location / {
            root /var/www/html;
        }
    }
}
```

## 3. modules

- static modules: complied into Nginx
- dyamic modules: loadable at run time

Ex: gzip compression, SSL, caching, geoip

## 4. Handlers

- Accepts http requests
- Decides whether to serve static content, proxy to backend, cache, etc

## 5. Buffers & caches

- Buffers requests/responses to handle slowclients efficiently
- Can cache upstream responses

## 6. Reverse proxy & load balancer

- Nginx receives client requests, forward them to backend apps
- Can balance load across multiple upstream servers

## Nginx folder structures

1. `nginx.conf` (main config file)

- Path: `/etc/nginx/nginx.conf`
- This is the entry point for all configs
- structure:

```
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
    worker_connections 768;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

- Key sections:

    - user → defines Linux user (usually www-data) under which worker processes run.

    - worker_processes → how many worker processes to run (often auto).

    - events {} → controls connection handling (worker_connections).

    - http {} → the main block for web traffic configs.

        - Includes MIME types.

        - Defines logging.

        - Loads configs from conf.d/ and sites-enabled/.

2. `conf.d`(general configs)

- Path: `/etc/nginx/conf.d/`
- Contains `.conf` files that are included automatically by `nginx.conf`
- Used for global configs, not tied to specific domain

3. `sites-available`(available virtual hosts)

- Path: `/etc/nginx/sites-available/`
- Each file here defines a server block (virtual host = a website)
- But just putting a file here does not make it active
- Ex: `/etc/nginx/sites-available/example.com`

```
server {
    listen 80;
    server_name example.com www.example.com;

    root /var/www/example.com/html;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

- This config:
    - Listens on port 80
    - Servers files from `/var/www/example.com/html`
    - falls back to 404 if file not found

4. `sites-enabled/`(active virtual hosts)

- Path: `/etc/nginx/sites-enabled/`
- `Contains `symlinks` to `sites-avaiable/`
- `Nginx` loads all files here on startup
- ex enable site: `sudo ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/`
- Disable site: `sudo rm /etc/nginx/sites-enabled/example.com`

5. `modules-available` and `modules-enabled`

6. `mime.types`

- Path: `/etc/nginx/mime.types`
- Maps file extensions -> mime type

```
types {
    text/html  html htm;
    text/css   css;
    application/javascript  js;
    image/png  png;
    image/jpeg jpg jpeg;
}
```

- Without this, browsers may treat files incorrectly (e.g., showing CSS as plain text).

7. `/var/www/`
- Default document root(where web files live)
- Ex: `/var/www/html/index.html` => default nginx webcome page
- Each site usually gets its own folder  under `/var/www/`

8. `/var/log/nginx`
- Logs directory
- `access.log` => http requests
- `error.log` => errors during request handling
- ex:

```
192.168.1.5 - - [29/Aug/2025:12:45:32 +0000] "GET /index.html HTTP/1.1" 200 612 "-" "Mozilla/5.0"
```

9. `/usr/share/nginx/`

- May contain default html files
- Not always used in custom deloyments

## Workflow of config loading

1. Nginx starts → reads /etc/nginx/nginx.conf.

2. Loads global settings (user, worker_processes).

3. Includes configs from:

    - conf.d/*.conf

    - sites-enabled/*

4. Each active server block (sites-enabled) defines how requests are handled.

5. MIME types, fastcgi, and snippets are included as needed.

## Nginx syntax

1. Directives

- A directive is a single instrcution in Nginx
- Written as:
    
    ```
    directive_name value;
    ```

Ex: 

```
worker_processes 4;
```

2. Blocks(Context)

- Some directives have a block `{ ... }` containing more directives
- These blocks defines context(like `http`, `server`, `location`)

Ex:

```
http {
    server {
        listen 80;
        server_name example.com;
    }
}
```

3. Hierarchy(context level)

Nginx config has a hierarchy of contexts

1. Main context => top level(outside any block)
    - Ex: `worker_processes`, `error_log`
2. http context => inside `http {}`(for each domain/website)
3. server context => inside `server {}`
4. location context => inside `location {}` (for url matching)

```
worker_processes auto;   # Main context

http {
    server {
        listen 80;                       # server context
        server_name example.com;

        location / {
            root /var/www/html;          # location context
            index index.html;
        }
    }
}
```

4. Comment

```
#this is comment
```

5. Variables

- Nginx has built-in variable like

    - $host => requested host name
    - $remote_addr => client's IP
    - $uri => requested URI

```
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
```

- Some variable commons:

| Variable           | Meaning                                               |
| ------------------ | ----------------------------------------------------- |
| `$host`            | Host header from request (e.g., `example.com`).       |
| `$remote_addr`     | Client’s IP address.                                  |
| `$remote_port`     | Client’s source port.                                 |
| `$server_addr`     | Server’s IP address.                                  |
| `$server_name`     | Name of the virtual host.                             |
| `$server_port`     | Port the request was received on (80, 443).           |
| `$request_uri`     | Full original request URI (e.g., `/index.php?id=10`). |
| `$uri`             | Normalized URI (no args, processed).                  |
| `$args`            | Query string (e.g., `id=10&name=test`).               |
| `$query_string`    | Same as `$args`.                                      |
| `$request_method`  | HTTP method (`GET`, `POST`, etc.).                    |
| `$scheme`          | Request scheme (`http` or `https`).                   |
| `$http_user_agent` | Client’s User-Agent header.                           |
| `$http_referer`    | Referrer URL.                                         |


- Proxy/upstream

| Variable                     | Meaning                                     |
| ---------------------------- | ------------------------------------------- |
| `$proxy_add_x_forwarded_for` | Appends client IP to `X-Forwarded-For`.     |
| `$upstream_addr`             | Address of upstream server (when proxying). |
| `$upstream_response_time`    | Time it took upstream to respond.           |


- Request/response

| Variable           | Meaning                                          |
| ------------------ | ------------------------------------------------ |
| `$request_time`    | Time (in seconds) Nginx took to process request. |
| `$status`          | Response status code (200, 404, 500).            |
| `$body_bytes_sent` | Number of bytes sent to client.                  |
| `$request_length`  | Request size (headers + body).                   |




6. Include directive

- Reuse configs by including other files.

```
include /etc/nginx/conf.d/*.conf;
```

## Nginx detail context

### 1. `server` block

- The `server {}` block defines a virtiual server(a site or application)
- You can have multiple `server` blocks in `/etc/nginx/sites-available/`(or directly in `nginx.conf`)
- Each `server` block listens on one or more ip adadress/ports and handles requests for one or more domain names

```
server {
    listen 80;
    server_name example.com www.example.com;

    root /var/www/example;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### 2. Common  directive of server {}

1. `listen` => defines which ip address and port the server should listen on

```
listen 80;              # listen on port 80 (HTTP)
listen 443 ssl;         # listen on port 443 (HTTPS)
listen 127.0.0.1:8080;  # only localhost on port 8080
listen [::]:80;         # IPv6
```

2. `server_name` => defines which domain names(hostnames) this server block responds to

```
server_name example.com www.example.com;
server_name _;
server_name *.example.com;
```

3. `root`

Specifies the root directory for serving files.

```
root /var/www/example;
```

If a request is for /about.html, Nginx will look for /var/www/example/about.html

4. `index`

Defines which file to serve when the request is a directory.

```
index index.html index.htm index.php;
```

Request: `http://example.com/` → will try `index.html` → then `index.htm `→ then` index.php.`

5. `error_page`

Customizes error responses (like 404, 500).

```
error_page 404 /custom_404.html;
error_page 500 502 503 504 /50x.html;
```

If a page isn’t found (404), Nginx serves /custom_404.html

6. `location`

Defines how Nginx processes requests for certain paths or patterns.

```
location /images/ {
    root /data;
}
```

Request: /images/logo.png → /data/images/logo.png.

Types of location:

- Prefix match (/path/)

- Exact match (= /exactpath)

- Regex match (~ for case-sensitive, ~* for case-insensitive)

7. `try_files`

Checks multiple files/URIs in order, serving the first found.

```
location / {
    try_files $uri $uri/ /index.html;
}
```

If request /foo → Nginx tries:

- /foo (file)

- /foo/ (directory)

- /index.html (fallback)

8. `proxy_pass`

(Used in reverse proxy setups) — forwards requests to a backend server.

```
location /api/ {
    proxy_pass http://127.0.0.1:3000;
}
```

Requests `/api/users` → forwarded to backend app at `127.0.0.1:3000.`

9. `rewrite`

Changes the request URI (with regex).

```
rewrite ^/old$ /new permanent;
```

`/old`→ redirected to `/new` (301 redirect).

10. `access_log / error_log`

Define log files for requests & errors.

```
access_log /var/log/nginx/example.access.log;
error_log  /var/log/nginx/example.error.log warn;
```

11. `ssl_certificate / ssl_certificate_key`

(Used for HTTPS/TLS)

```
listen 443 ssl;
ssl_certificate /etc/ssl/certs/example.crt;
ssl_certificate_key /etc/ssl/private/example.key;
```

Full

```
server {
    listen 80;
    server_name example.com www.example.com;

    root /var/www/example;
    index index.html index.htm;

    access_log /var/log/nginx/example.access.log;
    error_log  /var/log/nginx/example.error.log warn;

    error_page 404 /custom_404.html;

    location / {
        try_files $uri $uri/ =404;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Nginx logs

In nginx it have two type of logs:

1. Access log => records every request from clients

    - Hepls you answer:
        - Which pages are most visited
        - where traffic is coming from
        - how many requests per seconds
        - are bots or attackers hammering your server

2. Error log => records problems nginx encounters

    - Helps you debug:
        - Why are users getting 404 or 500 errors
        - did nginx fail to connect to upstream(nodejs, java)
        - are permissions or config broken

## Config logs

- Config global: all virtual site will be logs in center place

```
http {
    access_log /var/log/nginx/access.log;
    error_log  /var/log/nginx/error.log warn;
}
```

=> put inside http block of `nginx.conf` file

- Config isolated which mean each site has it own log:

```
server {
    server_name test.example;
    access_log off;
    error_log  /var/log/nginx/test_error.log;
}
```

=> put access_log and error_log inside server
