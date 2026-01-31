# What is ansible

ansible is an it automation tool, is used to automate server setup, configuration, and deployment

# What ansible is used for

Ansible helps you automate things like:

- server configuration(install nginx, nodejs, docker)
- application deployment(deploy backend, frontend)
- repeating admin tasks(create users, update packages)
- cloud & devops work(aws, azure, vps, ...)

# Ansible characteristic

1. Agentless

    - Dont need to install anything on target servers
    - Uses ssh(linux) or winRM(windows)

2. Simple & readble(yml)

```
- hosts: web
  become: yes
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
```

3. Idempotent(safe to run many times)

If nginx is already installed => ansbiel does nothing

You can run it again and again without breadking stuff


# Core concepts

| Term          | Meaning                                                  |
| ------------- | -------------------------------------------------------- |
| **Inventory** | List of servers (IP, hostname)                           |
| **Playbook**  | YAML file with tasks                                     |
| **Task**      | One action (install package, copy file)                  |
| **Module**    | Built-in actions (apt, copy, service, docker_container…) |
| **Role**      | Reusable playbook structure                              |

# Example

## Inventory

```
[vps]
192.168.1.10 ansible_user=root
```

## Playbook

```
- hosts: vps
  become: yes
  tasks:
    - name: Install Docker
      apt:
        name: docker.io
        state: present
```

run: ```ansible-playbook install-docker.yml```


# Ansible scripts and structure

## 1. basic ansible structure

Ansible is built around 4 core things:

```
Inventory  →  Playbook  →  Tasks  →  Modules
```

You don’t write shell scripts most of the time.

You describe state, Ansible does the work.

## 2. Inventory (list of servers)

This tells Ansible where to run

```
inventory.ini
```

```
[vps]
192.168.1.10 ansible_user=root

[web]
web1 ansible_host=192.168.1.11 ansible_user=ubuntu
```

Run test:

```
ansible vps -m ping
```

If you see pong, SSH works.

## 3️. First Playbook (Ansible script)

## playbook.yml

```
- name: Setup web server
  hosts: vps
  become: yes

  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present

    - name: Start nginx
      service:
        name: nginx
        state: started
        enabled: yes
```

Run it:

```
ansible-playbook -i inventory.ini playbook.yml
```

### Important YAML rules

- Use spaces, not tabs

- Indentation matters

- ```-``` means list item

## 4️. Tasks (small actions)

Each task has:

```
- name: Human readable description
  module_name:
    option: value
```

Example:

```
- name: Copy config file
  copy:
    src: nginx.conf
    dest: /etc/nginx/nginx.conf
```

## 5. Most used modules

### Package install

```
apt:
  name: docker.io
  state: present
```

### Run command (last option)

```
command: ls -la
```

### Shell (if you need pipes)

```
shell: docker ps | grep node
```

### Files

```
file:
  path: /app
  state: directory
```

### Services

```
service:
  name: docker
  state: started
```

## 6️. Variables (very important)

```
vars:
  app_name: hello-node
  app_port: 3000
```

Use them:

```
- name: Run container
  docker_container:
    name: "{{ app_name }}"
    published_ports:
      - "{{ app_port }}:3000"
```

## 7️. Handlers (restart only when changed)

```
tasks:
  - name: Update nginx config
    copy:
      src: nginx.conf
      dest: /etc/nginx/nginx.conf
    notify: Restart nginx

handlers:
  - name: Restart nginx
    service:
      name: nginx
      state: restarted
```

Runs only if config changed

## 8️. Real project structure (IMPORTANT)

When projects grow, do NOT put everything in one file.

```
ansible/
├── inventory/
│   └── production.ini
├── group_vars/
│   └── vps.yml
├── roles/
│   ├── docker/
│   │   ├── tasks/main.yml
│   │   └── handlers/main.yml
│   ├── node/
│   │   └── tasks/main.yml
│   └── nginx/
│       ├── tasks/main.yml
│       ├── handlers/main.yml
│       └── templates/nginx.conf.j2
├── playbook.yml
```

## 9️. Roles (clean & reusable)

### roles/docker/tasks/main.yml

```
- name: Install docker
  apt:
    name: docker.io
    state: present

- name: Start docker
  service:
    name: docker
    state: started
    enabled: yes
```

### playbook.yml

```
- hosts: vps
  become: yes
  roles:
    - docker
    - node
    - nginx
```

## 10. Templates (dynamic configs)

Instead of static config:

#### nginx.conf.j2

```
server {
  listen 80;

  location / {
    proxy_pass http://localhost:{{ app_port }};
  }
}
```

Ansible replaces variables automatically.

## 11. Ansible + Docker (VERY common)

```
- name: Run node container
  docker_container:
    name: hello-node
    image: node:18
    ports:
      - "3000:3000"
```