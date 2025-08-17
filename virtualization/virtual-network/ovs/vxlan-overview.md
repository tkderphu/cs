# Tunneling / Overlay Networking

`Tunneling / Overlay Networking is a core concept in modern networking—especially in cloud computing, containers, SDN (Software Defined Networking), and data centers. It allows communication across different networks (or over the internet) as if they were directly connected—even when the underlying infrastructure doesn't support such communication directly.`

# What is Tunneling

Tunneling is the technique of encapsulating one network protocol within another. The idea is to send packets from one network through another network as if it were a private connection, even though it may go over public infrastructure.

Example:

- A private IP packet from 10.0.0.1 to 10.0.0.2 is encapsulated inside a UDP or GRE packet and sent over the internet.

# Example

Let’s say VM-A (10.0.0.1) on Host A sends a packet to 10.0.0.2(VM on Host B):

```
[VM-A]
    sends → Ethernet frame (src 10.0.0.1, dst 10.0.0.2)
        ↓
[br0] on Host A
        ↓
[vxlan0] → encapsulates into UDP/IP (outer src 192.168.100.1, dst 192.168.100.2)
        ↓
Over physical network to Host B
        ↓
[vxlan0] on Host B decapsulates
        ↓
[br0] forwards to vmtap0 → [VM-B]
```

Ethernet frame is sent from VM-A will go to bridge(OVS), OVS look up dst MAC-ADDRESS and then know it on different host then send to remote HOST with protocol UDP at port ... 

# What is Overlay Networking

`Overlay networking builds virtual networks on top of physical (underlay) networks. This is achieved using tunnels, where virtual links are created between endpoints, allowing the communication of VMs or containers across different hosts as if they were on the same LAN.`

Think of overlay as:
- “I create a network on top of another network by wrapping/encapsulating my data to cross boundaries.”


# Data Flow Example (Using VXLAN):

VM1 (10.0.0.1) → VM2 (10.0.0.2) over hosts:

```
VM1
 ↓
[Original Ethernet Frame]
 ↓
[Encapsulated in VXLAN over UDP/IP]
 ↓
Sent from Host A (192.168.1.10) to Host B (192.168.1.20)
 ↓
Host B decapsulates
 ↓
Delivered to VM2
```

# Why Use Tunneling/Overlay Networks?

| Purpose                           | Description                                                                     |
| --------------------------------- | ------------------------------------------------------------------------------- |
| 🧩 **Network Abstraction**        | Decouples virtual network topology from physical network.                       |
| 🔐 **Isolation**                  | Tenant isolation in cloud using virtual networks (e.g., OpenStack, Kubernetes). |
| 🌐 **Cross-subnet communication** | Allow VMs/containers in different physical subnets to act as if in same subnet. |
| 📦 **Encapsulation**              | Can carry L2 frames over L3 (e.g., MAC addresses over IP).                      |



# VXLAN 

# 1. What is VXLAN?

`VXLAN (RFC 7348) is a Layer 2 over Layer 3 overlay network protocol. It allows you to create a virtual L2 network across physical L3 networks, useful for connecting VMs or containers on different hosts as if they’re on the same Ethernet broadcast domain.`

- It encapsulates L2 Ethernet frames inside UDP packets, using port 4789 by default.

# 2. Why VXLAN?

| Feature                     | Benefit                                                                   |
| --------------------------- | ------------------------------------------------------------------------- |
| Overlay                  | Create isolated virtual networks on top of shared physical infrastructure |
| Encapsulation            | Encapsulates Ethernet frames in UDP for transport over IP                 |
| Scalability              | Supports 16 million VNIs (vs 4096 VLANs)                                  |
| Inter-host communication | Seamlessly connect VMs/containers across hosts and networks               |


# 3. VXLAN Components

| Component                          | Description                                                                                  |
| ---------------------------------- | -------------------------------------------------------------------------------------------- |
| **VNI** (VXLAN Network Identifier) | 24-bit ID that identifies the VXLAN segment (like VLAN ID, but much larger range)            |
| **VTEP** (VXLAN Tunnel Endpoint)   | Responsible for encapsulating and decapsulating VXLAN traffic. Typically, each host has one. |
| **Underlay Network**               | The physical L3/IP network connecting the hosts                                              |
| **Overlay Network**                | The virtual L2 network connecting VMs via VXLAN tunnels                                      |
| **UDP Port 4789**                  | Default port used to carry VXLAN packets                                                     |


# 4. VXLAN Packet Format (Encapsulation)

A packet from a VM (e.g., ARP, ICMP) is encapsulated like this:

```
+---------------------+
| Outer Ethernet/IP   | → Source: Host A IP, Dest: Host B IP
| Outer UDP (port 4789)|
| VXLAN Header (VNI)   |
| Inner Ethernet       | → Source: VM A MAC, Dest: VM B MAC
| Payload              |
+---------------------+
```

# Practice with OVS

We’ll use ovs-vsctl to configure VXLAN between Host A and Host B.

Goal

```VM-A on Host A: IP 10.0.0.1
VM-B on Host B: IP 10.0.0.2
Physical host IPs:
Host A: 192.168.1.10
Host B: 192.168.1.20
VNI: 1000
```

# On Host A

```
sudo ovs-vsctl add-br br0 #create bridge
sudo ip netns add vm0
sudo ip link add vnet-vm0 type veth peer name vnet0
sudo ip link set vnet-vm0 netns vm0
sudo ip link set vnet0 up
sudo ip netns exec vm0 ip link set vnet-vm0 up
sudo ip netns exec vm0 ip address add 10.0.0.1/8 dev vnet-vm0
sudo ovs-vsctl add-port br0 vnet0 #add vm interface to switch

sudo ovs-vsctl add-port br0 vxlan0 -- set interface vxlan0 type=vxlan \
  options:remote_ip=192.168.10.130 options:key=1000 options:dst_port=4789 # Add VXLAN port (remote = Host B)
```

# On Host B(similarly with hostA)

```
sudo ovs-vsctl add-br br0 #create bridge
sudo ip netns add vm0
sudo ip link add vnet-vm0 type veth peer name vnet0
sudo ip link set vnet-vm0 netns vm0
sudo ip link set vnet0 up
sudo ip netns exec vm0 ip link set vnet-vm0 up
sudo ip netns exec vm0 ip address add 10.0.0.2/8 dev vnet-vm0
sudo ovs-vsctl add-port br0 vnet0 #add vm interface to switch

sudo ovs-vsctl add-port br0 vxlan0 -- set interface vxlan0 type=vxlan \
  options:remote_ip=192.168.10.132 options:key=1000 options:dst_port=4789 # Add VXLAN port (remote = Host A)
```

`VNI (key=1000) must match on both sides.`