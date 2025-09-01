# Note about kubernetes

# What is kubernetes

Kubernetes is an open-source platform for automating deployment, scaling, and managing containerized applications

- If docker runs a single container, kubernetes helps you run and manage hundreds or thousands of containers across many machines

# Key concepts in kubernetes

- Cluster: A groups of machine(nodes) working together
- Node: A single machine(physical or virtual) inside the cluster
- Pod: The smallest unit in kubernetes. It contains one or more containers that run together
- Deployment: Defines how to run pods(number of replicas, update strategy)
- Service: Exposes application so they can be accessed inside or outside the cluster
- Ingress: Manages external access(http/https)
- ConfigMap & Secret: store configuration data and sensitive information like passwords, secretkey
- Namespace: divide resources into isolated groups inside the same cluster

# Kubernetes architecture

## 1. Control plane(master components)

The control plane manages the whole cluster. It makes global decisions(scheduling, scaling, health checking)

### Main components

### 1. Api server(kube-apiserver)
- The entry point for all commands(from `kubectl`, UI, other apps)
- Acts as a `REST API` server
- All components talk to each other through it
- How it works under the hood:

    - Runs as a RESTful web server.

    - Exposes endpoints like /api/v1/pods or /apis/apps/v1/deployments.

    - All requests (from kubectl, controllers, other components) go through the API server.

    - Validates input (checks YAML is correct, permissions via RBAC).

    - Writes desired state into etcd.

    - Uses watch mechanism (long polling / streaming API) so other components (kubelet, controllers) can subscribe to changes instead of constant polling.


### 2. etcd

- A key-value database that stores the cluster state
- Keeps info like: pods running, configurations, secrets, nodes, etc
- if etcd fails, the cluster "forgets" it state
- How it works:

    - A distributed key-value store (similar to a highly reliable database).

    - Stores data in hierarchical paths (like a filesystem):
    
    ```
    /registry/pods/default/my-pod
    /registry/deployments/my-deployment
    ```

    - Uses Raft consensus algorithm for leader election and replication → ensures consistency across nodes.

    - Every write is committed only when the majority of etcd cluster members agree.
    
    - API server reads/writes here → when etcd changes, API server notifies subscribers


### 3. Scheduler(kube-scheduler)

- Decides which node a pod will run on
- Check CPU, mem, etc
- Ex: Node A is full => it schedules the new pod on Node B
- How it works:

    - Watches for new pods in etcd (via API server).

    - For each unscheduled pod:

        - Filters nodes: removes nodes that don’t have enough CPU, RAM, or fail affinity/taint rules.

        - Scores nodes: ranks candidates based on things like:

        - Resource balance

        - Data locality (near storage)

        - Spread across zones/nodes

        - Assigns node: writes binding object → tells API server "this pod goes to Node X".

    - Doesn’t actually start pods → just decides the best node. The kubelet then executes it.


### 4. Controller manager(kube-controller-manager)

- Run different controllers(small processes that watch and react)
- Examples of controllers:
    - Node controller => watches node status
    - ReplicaSet Controller => ensures the desired number of pods
    - Job controller => manages batch jobs

### 5. Cloud controller manager
- Connects kubernetes with cloud services
- Manages things like load balancers, storage volumes
- How it works:

- Runs many small controllers, each watching specific resources:

    - ReplicaSet Controller: ensures the right number of pods exist.

    - Node Controller: checks node health (via heartbeats).

    - Endpoint Controller: updates service endpoints when pods change.

    - Job Controller: ensures batch jobs complete.

- Mechanism:

    - Watches etcd via API server.

   - Compares desired state vs actual state.

    - If mismatch → takes corrective action (e.g., start a new pod, delete extras).

## 2. Woker nodes(Data plane components)

Worker nodes run the actual applications

### Main component

### 1. Kubelet

- Agent that runs on every node
- Talks to control plane => ensures cntainers in the pod are running
- Example: if a pod should run 3 replicas kubelet checks that they are alive
- How it works:

    - Watches API server for "PodSpecs" assigned to its node.

    - Talks to container runtime (Docker/containerd/CRI-O) using Container Runtime Interface (CRI).

    - Steps:

        - Receives PodSpec → parses YAML into container instructions.

        - Calls container runtime to pull images and start containers.

        - Monitors container health with liveness/readiness probes.

        - Reports pod status back to API server.

    - If a container dies → kubelet restarts it automatically (if policy says so).


### 2. Kube-proxy

- Handles networking inside the node
- Maintains network rules for communication(ClusterIP, NodePort, LocalBalancer)
- Ensures services can talk to pods correctly
- How it works:

    - Watches Services from API server.

    - Creates iptables or IPVS rules on the node:

        - Routes traffic from a Service’s virtual IP (ClusterIP) to actual Pod IPs.

        - Implements load balancing between multiple pods.

    - Example:

        - Service my-app → ClusterIP: 10.96.0.1

        - Backing pods: 10.244.1.2, 10.244.2.3
        
        - Kube-proxy sets rules so traffic to 10.96.0.1 is forwarded to one of the pod IPs.


### Container runtime

- The actual engine that runs container(Docker,containerd)
- Kubernetes itself doesn't run containers directly -> it uses a runtime
- How it works:

    - Kubelet talks to runtime via CRI (gRPC API).

    - Runtime does:

        - Pull image from registry (e.g., Docker Hub).

        - Create namespaces (Linux feature for isolation).

        - Set up cgroups for CPU/memory limits.

        - Start container process.

    - Provides container logs and status back to kubelet.

# Archeticture flow

1. User runs a command → kubectl apply -f app.yaml.

2. API Server receives it → stores in etcd.

3. Scheduler picks a node.

4. Kubelet on that node starts the pod via container runtime.

5. Kube-proxy manages networking so the pod can be reached.

6. Controller Manager watches to ensure the pod stays alive.


# Install

To practice k8s you can use `minikube`:

Minikube is a tool that lets you run a single node k8s cluster on your local machine

- It’s mainly for learning, testing, and development (not production).

- Runs inside a virtual machine or container on your laptop/PC.

- Gives you the same kubectl experience as a real Kubernetes cluster.

Think of it like a sandbox Kubernetes → small, easy to set up, safe to experiment.

## How minikube works

- You install Minikube on your system.

- When you run minikube start:

    - It creates a VM (using VirtualBox, Docker, KVM, Hyper-V, etc.) or runs directly in Docker.

    - Inside that VM, it installs all the Kubernetes components (API server, etcd, kubelet, controller, scheduler).

    - Configures your kubectl tool to talk to this local cluster.

- You now have a single-node Kubernetes cluster where you can deploy apps, services, and experiment.

### Command with minikube

```
# Start cluster (using Docker driver)
minikube start --driver=docker

# Stop cluster
minikube stop

# Delete cluster
minikube delete

# Open Kubernetes dashboard
minikube dashboard

# Get cluster IP
minikube ip

# Enable an addon (e.g., Ingress)
minikube addons enable ingress

# SSH into minikube VM
minikube ssh
```