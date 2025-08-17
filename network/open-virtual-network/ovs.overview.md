# What is ovn

OVP is open-source network virtualization system built on top of OVS

It provides logical networking for VMs, containers, and bare metal - Handling switching, routing, ACLs, more...

### Core idea

- You describe your network in an abstract, logical way(logical switches, routers, acls)

- OVN maps that to physical flows in OVS on each host automatically.

# OVN components

## Control plane

- OVN Northbound database(NB) - high-level intent:

    - Logical switches
    - Logical routers
    - Ports, security groups, ACLs

- OVN Southbound database(SB) - low-level state

    - Chassis(hosts)
    - datapaths
    - encapsulation(vxlan, geneve)
    - mac/ip bindings
- ovn-northd - daemon that translates NB -> SB

- ovn-controller - runs on each compute node, applies SB flows to local OVS

## Data plane

- Uses OVS to handle actual packet forwarding
- Encapsulation between nodes(geneve, vxlan)
- flows programmed automatically via SB DB


# OVN networking features

- L2 switching - Logical switches connecting VMs/containers

- L3 routing - Logical routers for inter-subnet communication

- Distributed routing - Routing done on each compute node

- Security groups/acls - statefull firewall rules

- Locad balancing - layer 4 virtual ips
- NAT - snat/dnat for internet access ort external exposure

- DHCP - integrated logical dhcp

- Multicast/IGMP snooping

- QoS - bandwidth limits, priority queues
- Geneve - based tunneling with metadata

# OVN architecture

```
+-------------------+        +----------------------+
|   Your App / CLI  |        |   Orchestration      |
| (ovn-nbctl, API)  |        | (OpenStack, K8s, etc)|
+--------+----------+        +-----------+----------+
         |                               |
         v                               v
  +--------------+       +--------------------------+
  | OVN NB DB    | <---- |    OVN Northbound Client  |
  +--------------+       +--------------------------+
         |     (ovn-northd)
         v
  +--------------+
  | OVN SB DB    |
  +--------------+
         |
         v
+--------+---------+   +--------+---------+
| ovn-controller  |   | ovn-controller   |
| (Node 1)        |   | (Node 2)         |
+-----------------+   +------------------+
       | OVS Flows          | OVS Flows
       v                    v
  Packets Forwarding   Packets Forwarding
```

# APIs and Integration

- Native API: OVSDB JSON-RPC to NB/SB DB.

- CLI tools: ovn-nbctl, ovn-sbctl.

- Orchestration integration:

    - OpenStack Neutron (via networking-ovn plugin).

    - Kubernetes (via OVN-Kubernetes CNI).

    - Custom apps (connect directly to NB DB).


# Common commands

```
# Show all logical switches
ovn-nbctl show

# Create a logical switch
ovn-nbctl ls-add sw0

# Add a logical port
ovn-nbctl lsp-add sw0 port1
ovn-nbctl lsp-set-addresses port1 "aa:bb:cc:dd:ee:ff 192.168.1.10"

# Show chassis
ovn-sbctl show

# Show all flows in SB
ovn-sbctl list Datapath_Binding
```

# Deployment Models

- Single-node test: all components on one VM.

- Multi-node: central DB servers, compute nodes running ovn-controller.

- Containerized: via Kubernetes pods.

- Cloud-managed: via OpenStack Neutron.



sudo ip netns exec netns1 ip route add default via 192.168.1.1
sudo ip netns exec netns2 ip route add default via 192.168.1.1