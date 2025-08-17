
# Core concept

# 1. Network Module

This module allow user(tenant) can control their network on their cloud:

- Manages networks for instances(VMs, containers, ...etc).

- It allows users to create their own networks, control IP addressing, configure routing, NAT, floating IPs, and apply security rules.

- Using some technology such as Linux Bridge, OVS, VXLan, ...etc

# 2. Core concept

- Network: A virtual Layer 2 domain (like a VLAN).

- Subnet: An IP range associated with a network (like a CIDR).

- Port: An attachment point to a network. Instances get virtual NICs via ports.

- Router: Connects multiple networks and provides Layer 3 routing + NAT.

- Floating IP: Public IP that maps to an instance's private IP.

- Security Groups: Firewall rules applied to instance ports.

# 3. Architecture

Network module is divided to two submodule:

- Network plugin:
    
    - Provides Rest Api for managing networks, subnets, ports, routers, ...etc.

    - Using database for storing resources like networks, subnets, ports, routers, ...etc


- Network agents:

    Agents are deployed on each compute/network node and implement networking functionality: 

    - L2 Agent (e.g., OVS Agent): Manages the virtual switch (bridges, ports, VLANs, tunnels).

    - DHCP Agent: Manages DHCP servers for tenant networks.

    - L3 Agent: Provides routing, NAT, and floating IP services.

    - Metadata Agent: Provides metadata service for instances.



# How design database

# 1. High-Level Design Principles

- Every Neutron resource = a table (or related tables)
e.g., networks, subnets, ports, routers.

- Uses UUIDs as primary keys for all resources (ensures uniqueness across the cloud).

- Stores tenant/project ownership in almost every table.

- Uses relationships (one-to-many, many-to-many) between resources.

# 2. Core Tables

## 2.1 networks

Represents a virtual L2 domain.

| Column           | Type      | Notes                                |
| ---------------- | --------- | ------------------------------------ |
| id               | UUID (PK) | Unique network ID                    |
| name             | VARCHAR   | Human-readable name                  |
| tenant\_id       | VARCHAR   | Project/tenant that owns the network |
| admin\_state\_up | BOOLEAN   | Is network administratively up?(does switch on/off)      |
| shared           | BOOLEAN   | Is it shared between tenants?        |
| status           | VARCHAR   | ACTIVE/DOWN      (is used by network agents or not)                    |


## 2.2 subnets

Represents an IP subnet in a network.

| Column           | Type      | Notes                               |
| ---------------- | --------- | ----------------------------------- |
| id               | UUID (PK) | Unique subnet ID                    |
| network\_id      | UUID (FK) | References `networks.id`            |
| cidr             | CIDR      | Subnet range (e.g., 192.168.1.0/24) |
| gateway\_ip      | INET      | Gateway IP address(usually use the first ip address of subnet such as: `192.168.1.1)`                  |
| ip\_version      | INT       | IPv4 (4) or IPv6 (6)                |
| dhcp\_range     | String   | Range dhcp with format like this: `192.168.1.10, 192.168.1.200`. In case dhcp_range is empty(null) then this subnet will not support dhcp                       |
| dns\_nameservers | ARRAY     | DNS servers list                    |


## 2.3 ports

Represents a connection point (like a virtual NIC).

| Column           | Type      | Notes                                     |
| ---------------- | --------- | ----------------------------------------- |
| id               | UUID (PK) | Port ID                                   |
| network\_id      | UUID (FK) | References `networks.id`                  |
| device\_id       | VARCHAR   | Instance/Router ID using this port        |
| device\_owner    | VARCHAR   | What owns the port (e.g., `compute:nova, network:dhcp, network:router_gateway, network:router_interface`) |
| mac\_address     | MAC       | MAC address of port                       |
| admin\_state\_up | BOOLEAN   | Admin up?                                 |
| status           | VARCHAR   | ACTIVE/DOWN                               |


## 2.4 ipallocations

Stores actual IP addresses allocated to a port.

| Column      | Type      | Notes                   |
| ----------- | --------- | ----------------------- |
| port\_id    | UUID (FK) | References `ports.id`   |
| subnet\_id  | UUID (FK) | References `subnets.id` |
| ip\_address | INET      | Allocated IP            |


Relationship:

- One port can have multiple IP addresses (one-to-many).

- Links ports and subnets.

# Flow when attach network to VM

1. Users create their new network include `networks`, `subnets`

    - In server side `network-node` will store info about `networks, subnets` of that users

2. Users go to launch VM page for creating new VM:

    - Users choose their network attach to their new VM

3. In server side:

    - `Netword-Plugin` will  store information about VM and its network

    - After store to database then `compute-node` will use `Network-Agent` which use for creating actual network. 

    - In case have many `compute-node` we must create VNXLAN across `compute-node`.


# 3. Router Tables

## 3.1 routers

Represents a logical router.

| Column           | Type      | Notes             |
| ---------------- | --------- | ----------------- |
| id               | UUID (PK) | Router ID         |
| tenant\_id       | VARCHAR   | Project owner     |
| name             | VARCHAR   | Name              |
| admin\_state\_up | BOOLEAN   | Is router active? |


# 4. Security and Policy Tables

## 4.1 securitygroups

Stores security group information

| Column      | Type      | Notes             |
| ----------- | --------- | ----------------- |
| id          | UUID (PK) | Security group ID |
| tenant\_id  | VARCHAR   | Project owner     |
| name        | VARCHAR   | Name              |
| description | TEXT      | Description       |


## 4.2 securitygrouprules

Stores firewall rules inside a security group.

| Column              | Type      | Notes                          |
| ------------------- | --------- | ------------------------------ |
| id                  | UUID (PK) | Rule ID                        |
| security\_group\_id | UUID (FK) | References `securitygroups.id` |
| direction           | VARCHAR   | ingress/egress                 |
| ethertype           | VARCHAR   | IPv4/IPv6                      |
| protocol            | VARCHAR   | tcp/udp/icmp                   |
| port\_range\_min    | INT       | Start port                     |
| port\_range\_max    | INT       | End port                       |
| remote\_ip\_prefix  | CIDR      | Allowed source/destination     |


# Network segment

## network_segments

Stores VXLAN segment details for networks, when have many `compute-node`:

| Column              | Type      | Notes                          |
| ------------------- | --------- | ------------------------------ |
| id                  | INT | ID ID                        |
| compute\_node\_ip | VARCHAR | Compute node ip |
| remote\_compute\_node\_ip           | VARCHAR   | Remote compute node(@compute_node_ip will connect @remote_compute_node_ip)                 |
