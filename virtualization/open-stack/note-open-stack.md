# Open stack

# Table Content


# 1. What is openstack

OpenStack is an open-source cloud computing platform that allows you to build and manage private and public clouds (IaaS – Infrastructure as a Service).

It provides services similar to AWS (like EC2, S3, etc.) but runs in your own data center or lab.

# 2. Core component of openstack

OpenStack is modular. Each service is a separate component communicating via APIs.

| Component      | Role                                  | Equivalent in AWS |
| -------------- | ------------------------------------- | ----------------- |
| **Nova**       | Compute (Virtual machines)            | EC2               |
| **Neutron**    | Networking (VPC, Router, Floating IP) | VPC, Elastic IP   |
| **Cinder**     | Block Storage (Volumes)               | EBS               |
| **Swift**      | Object Storage (File storage)         | S3                |
| **Glance**     | Image Management (VM templates)       | AMI               |
| **Keystone**   | Identity, Authentication, Roles       | IAM               |
| **Horizon**    | Web Dashboard                         | AWS Console       |
| **Heat**       | Orchestration (IaC)                   | CloudFormation    |
| **Ceilometer** | Telemetry, Metrics                    | CloudWatch        |


# 3. Openstack Architecture diagram

```
     +--------------------+
     |     Horizon (UI)   | ← Web Dashboard
     +--------------------+
              |
     +--------------------+
     |     Keystone       | ← Identity/Auth
     +--------------------+
      /         |        \
     /          |         \
+-------+   +--------+   +-------+
| Nova  |   | Glance |   | Cinder| ← Compute, Images, Volumes
+-------+   +--------+   +-------+
     |           |
     |        +--------+
     |        | Swift  | ← Object Storage
     |        +--------+
     |
+-----------------+
|  Neutron        | ← Networking
+-----------------+
     |
+-----------------+
| Physical/Virtual|
|   Network       |
+-----------------+

```

# 4. Detail about each component

## 4.1 Nova (Compute)

- Manages VM lifecycle: create, delete, pause, resize.

- Works with hypervisors: KVM, QEMU, Xen, VMware.

- Uses Libvirt to control hypervisors.

- Pulls images from Glance and attaches volumes from Cinder.

Workflow:

User requests a VM (via API or Horizon).

Nova talks to:

- Keystone (auth)

- Glance (image)

- Neutron (network)

- Cinder (volume)

Schedules VM on a compute node using filters/weights(check resources usage of node and choose the best node with lowest resources usage).

##  4.2 Neutron (Networking)

Provides network as a service:

- L2 networks (flat, VLAN, VXLAN)

- Routers, DHCP, Floating IP

## What is Floating IP? (NAT)

A Floating IP is a publicly accessible IP address that can be dynamically mapped to an instance (VM) in a private network.

## Why it's called “floating”?

- It is not permanently assigned to one instance.

- You can detach it from one VM and attach it to another, even across networks.

## Use case

```
+---------------------+               +-------------------------+
| External Network    |   Floating IP |      VM (10.0.0.5)      |
| (e.g., 203.0.113.10)| ─────────────▶|  via Virtual Router (SNAT)|
+---------------------+               +-------------------------+

                [Router does SNAT/DNAT between floating and fixed IPs]

```

## How Floating IP Works in OpenStack (step-by-step):
- You create an External Network (shared/public).

- You create a Router that connects:

- Your internal (private) network

- External network (via gateway)

- The router uses NAT (DNAT/SNAT) to map:

- Floating IP → Fixed IP of VM

- You associate a floating IP to a VM (via Neutron).

- You can now access the VM from internet.


## Using linux bridge to achieve that

Uses:

- Open vSwitch or Linux Bridge

- iptables, netns, dnsmasq for routing/NAT


## 4.3 Glance (Image Service)

Stores and serves VM disk images (QCOW2, RAW, VMDK).

Backed by:

- Local file system

- Swift

- Ceph

Nova pulls images from Glance when booting a VM.

## 4.4 Cinder (Block Storage)

Manages block volumes for VM disks.

- Create, delete, attach/detach volumes.

- Backends: LVM, iSCSI, NFS, Ceph RBD.

Volumes can be attached to VMs as virtual disks via Libvirt.

## 4.5 Swift (Object Storage)

- Stores large unstructured data (images, videos, logs).

- RESTful S3-like API.

- Data is replicated and partitioned across nodes.

- Ideal for backups, CDN, and long-term archive.

## 4.6 Keystone (Identity)

Central authentication and token service.

Manages:

- Users, Projects (Tenants), Roles

- Policies for service access

All OpenStack services validate tokens via Keystone.

## 4.7 Horizon (Dashboard)

Web UI to interact with all OpenStack services.

Built with Django (Python web framework).

Uses APIs behind the scenes.

## 4.8 Heat (Orchestration)

- Infrastructure-as-Code (like Terraform or CloudFormation).

- Uses YAML templates to describe resources.

- Can deploy stacks: networks, VMs, volumes, security groups...

## 4.9 Ceilometer (Telemetry)

Collects metrics from OpenStack services.

Monitors usage (CPU, RAM, disk, network).

Used for:

- Billing

- Auto-scaling (with Heat)

- Alerting (with Aodh)