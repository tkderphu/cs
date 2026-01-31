# 1 What is ci/cd

Cid/cd is a way of working to automatically:

- checking code
- test code
- build app
- deploy it

every time change code

## 1.1. CI

When push code to github:

- code is automatically checked
- tests are run
- build errors are found early

## 1.2. CD

After ci passes:

- We have a artifact of application
- we will deploy(to server, cloud, staging, productio, etc)

# 2. What is github action

Github action is a tool provided by github to implement ci/cd

# 2.1 what can github actions do

- run tests
- build java/node/react/docker apps
- deploy to vps, aws
- run scripts when
    
    - push code
    - open a pull request
    - on a schedule(cron)

# Working with github actions

# Rule #1

GitHub Actions runs when something happens

This “something” is called an event.

Common events:

- push → when you push code

- pull_request → when you open PR

- schedule → cron job (every night)

# Rule #2

Know the magic folder:

```
.github/
 └── workflows/
      └── something.yml
```

If the file is NOT here → GitHub ignores it.

# Create first workflow

## 1. create file

```
.github/workflows/hello.yml
```

## 2. create content

```
name: Hello GitHub Actions

on:
  push:

jobs:
  hello:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Hello GitHub Actions 🚀"
```

# STEP 5 — Checkout your code (VERY COMMON MISTAKE)

By default, GitHub Actions does NOT have your code.

You must add:

```
- uses: actions/checkout@v4
```

Example:

```
steps:
  - uses: actions/checkout@v4
  - run: ls
```

Now your repo code exists on the runner.

# STEP 6 — Use an Action vs run

There are 2 types of steps:

## 🔹 1. run (shell command)

```
- run: npm test
```

## 🔹 2. uses (reusable action)

```
- uses: actions/setup-node@v4
```

Think:

- run → you type command

- uses → someone already made it for you

## STEP 9 — Understand secrets 🔐 (IMPORTANT)

Never hardcode:

- passwords

- tokens

- SSH keys

Use GitHub Secrets.

How:

- Repo → Settings → Secrets → Actions

- Add secret:

    - DB_PASSWORD

    - SSH_KEY

 Use in YAML:
    
```
- run: echo $DB_PASSWORD
  env:
    DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
```

# Practice

## 1. Deploy application with docker

### Docker login with github actions

Login

```
- name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
```

Build and push

```
- name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ secrets.DOCKER_USERNAME }}/hello-node:latest
```

