
# What is dynamic routing

Dynamic routing in Linux means automatically learning and updating routes (instead of static routes) using routing protocols like OSPF, BGP, RIP, IS-IS. Normally, Linux uses a static routing table (ip route show), but with dynamic routing daemons, it can exchange routes with routers or other Linux hosts.


# 1. Static vs Dynamic Routing

## Static routing:

You manually add routes:

```
ip route add 10.0.2.0/24 via 192.168.1.1
```

Changes in the network (e.g., link down) are not automatically updated.

## Dynamic routing:

- Linux uses a routing daemon (like FRR, Quagga, Bird) to talk with other routers and automatically learn routes.

- If a path goes down, new routes are learned without manual intervention.


# 2. Linux Routing Table Recap

View routing table

```
ip route show
```

# 3. How to enable dynamic routing on Linux

Linux by itself doesn’t implement routing protocols. You need a routing suite:

## Popular routing daemons

- FRRouting (FRR) – Modern, widely used. Supports OSPF, BGP, RIP, IS-IS.

- Quagga – Older, now replaced by FRR.

- BIRD – Lightweight, good for BGP-heavy setups.

- OpenBGPD / OpenOSPFD – Minimal, OpenBSD-style.

# 4. Example: FRR with OSPF

## Step 1: Install FRR
On Ubuntu/Debian:

```
sudo apt update
sudo apt install frr frr-pythontools
```

Enable OSPF and BGP daemons in /etc/frr/daemons:

```
ospfd=yes
bgpd=no
```

Start the service:

```
sudo systemctl enable frr
sudo systemctl start frr
```

## Step 2: Configure OSPF

Open FRR shell:

```
sudo vtysh
```

Configure OSPF:

```
configure terminal
router ospf
 network 192.168.1.0/24 area 0
 network 10.0.1.0/24 area 0
exit
write
```

This tells Linux to advertise and learn routes for those networks using OSPF.

## Step 3: Check learned routes

```
ip route show
```

You will see new routes with proto ospf:

```
10.0.2.0/24 via 192.168.1.2 dev eth0 proto ospf
```

# Practice about dynamic routing

# 1. Lab Setup
We will create two routers (R1 & R2) and two subnets, using Linux ip netns and veth pairs.

```
[netns R1]----veth----[netns R2]
   |                        |
  net1 (10.0.1.0/24)       net2 (10.0.2.0/24)
```

- R1 connects to network 10.0.1.0/24

- R2 connects to network 10.0.2.0/24

- They will run OSPF using FRR to learn each other's subnet.


# 2. Create netns and interfaces

```
# Create namespaces
sudo ip netns add R1
sudo ip netns add R2

# Create veth pair to connect R1 <-> R2
sudo ip link add veth1 type veth peer name veth2

# Assign veth ends to namespaces
sudo ip link set veth1 netns R1
sudo ip link set veth2 netns R2

# Assign IPs
sudo ip netns exec R1 ip addr add 192.168.0.1/24 dev veth1
sudo ip netns exec R2 ip addr add 192.168.0.2/24 dev veth2

# Bring interfaces up
sudo ip netns exec R1 ip link set lo up
sudo ip netns exec R1 ip link set veth1 up
sudo ip netns exec R2 ip link set lo up
sudo ip netns exec R2 ip link set veth2 up
```

# 3. Install and enable FRR inside each namespace

## Create FRR configs for R1

`In /etc/frr/R1/frr.conf:`


```
hostname R1
log stdout
!
router ospf
 network 192.168.0.0/24 area 0
 network 10.0.1.0/24 area 0
!
```

Enable OSPF in /etc/frr/R1/daemons:

```
ospfd=yes
```

Run FRR in namespace:

```
sudo ip netns exec R1 /usr/lib/frr/frrinit.sh start
```

## Create FRR configs for R2

`In /etc/frr/R2/frr.conf:`

```
hostname R2
log stdout
!
router ospf
 network 192.168.0.0/24 area 0
 network 10.0.2.0/24 area 0
!
```

Enable OSPF in /etc/frr/R2/daemons:

```
ospfd=yes
```

Run FRR in namespace:

```
sudo ip netns exec R2 /usr/lib/frr/frrinit.sh start
```

# 4. Add internal networks (for dynamic learning)

Let's attach each router to a LAN that the other should learn:

```
# R1 LAN
sudo ip netns exec R1 ip addr add 10.0.1.1/24 dev lo

# R2 LAN
sudo ip netns exec R2 ip addr add 10.0.2.1/24 dev lo
```

# 5. Check dynamic routing

From R1, check OSPF neighbors and routes:

```
sudo ip netns exec R1 vtysh -c "show ip ospf neighbor"
sudo ip netns exec R1 vtysh -c "show ip route"
```

You should see:

```
O>* 10.0.2.0/24 [110/10] via 192.168.0.2, veth1
```