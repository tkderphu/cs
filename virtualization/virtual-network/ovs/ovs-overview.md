# Note about Open Virtual Switch



# What is ovs



Open vSwitch (OVS) is an open-source, multilayer virtual switch designed to enable programmable network automation in virtualized environments. It is commonly used in cloud computing platforms such as OpenStack, Kubernetes, and VMware NSX. OVS can run on standard Linux systems and supports technologies like SDN (Software-Defined Networking) and NFV (Network Functions Virtualization).



# Overview



OVS provides switching and routing functions for virtualized environments, allowing VMs and containers to communicate internally and with external networks. It supports:



- Layer 2 switching (MAC-based forwarding)



- Layer 3 forwarding



- VLANs and tunneling (GRE, VXLAN)



- OpenFlow and OVSDB protocols for SDN control



# Components



## ovs-vswitchd



- Description: The main userspace daemon. It controls the switching logic and manages flows, forwarding rules, and interface configuration.



- Role: Receives commands from ovsdb-server, applies flow rules to kernel datapath or userspace fallback.



## ovsdb-server



- Description: The Open vSwitch Database (OVSDB) server.



- Role: Stores configuration data (like bridges, ports, interfaces) and provides a management interface (via JSON-RPC).



- Database Schema: Uses a schema called Open_vSwitch to store bridge info, port config, QoS, etc.



## ovs-dpctl (Optional)



- Description: Tool to query and control the kernel datapath.



- Role: Mainly used for debugging and inspecting kernel flow tables.



## ovs-vsctl



- Description: CLI tool to interact with ovsdb-server.



- Role: Adds/removes bridges, ports, and manages configuration.



## Kernel Module (openvswitch.ko)



- Description: The datapath module installed in the Linux kernel.



- Role: Fast packet forwarding. Acts like a high-speed switch in the kernel space.



## ovs-ofctl



- Description: CLI tool for managing OpenFlow flows in OVS.



- Role: View, add, and remove OpenFlow rules manually.





# Userspace in OVS



In OVS, userspace refers to the userspace components of the system that run outside the Linux kernel. These components handle high-level control logic, flow setup, and communication with management systems like OVSDB or OpenFlow controllers.



## Main Userspace Components in OVS

| Component      | Description                                                                                       |
| -------------- | ------------------------------------------------------------------------------------------------- |
| `ovs-vswitchd` | The main Open vSwitch daemon. Handles switch logic, installs flow rules into the kernel datapath. |
| `ovsdb-server` | A database server for storing configuration (bridges, ports, interfaces, etc).                    |
| `ovs-ofctl`    | CLI tool for managing OpenFlow rules manually.                                                    |
| `ovs-vsctl`    | CLI tool for managing OVSDB configuration (bridges, ports, etc).                                  |



## What Does Userspace Do?



When a packet arrives at OVS and there's no matching rule in the kernel datapath, the flow goes to userspace:



###  Packet Flow



1. VM sends packet → tap interface → OVS kernel module



2. Kernel has no matching flow rule, so:



3. Packet sent to userspace (ovs-vswitchd)



4. ovs-vswitchd:



 	- Looks up MAC address, port, or VLAN



 	- Queries OVSDB (e.g., bridge configuration)



 	- Applies logic (e.g., OpenFlow rules, VXLAN encapsulation)



5. Installs flow rule in kernel



6. Packet is now processed and forwarded



## Userspace Handles:



- Initial packet classification



- OpenFlow control plane



- VXLAN / Geneve / GRE tunnel setup



- Learning MAC addresses



- ARP responses if needed



- Interacting with SDN controllers



- Updating flow tables in the kernel



## Example



Imagine Host A has a VM with MAC `aa:bb:cc:dd:ee:ff` sending a packet to a VM on Host B.



First packet: goes to userspace (no rule yet).



ovs-vswitchd:



- Looks up destination MAC.



- Learns it should go via vxlan0.



- Installs rule in kernel:



```

in_port=1, dl_dst=aa:bb:cc:dd:ee:ff → output:vxlan0

```



Next packets: handled 100% by kernel, no userspace interaction (fast path).



# Kernel datapath



The kernel datapath in Open vSwitch (OVS) is a high-performance packet processing engine implemented as a Linux kernel module (openvswitch.ko). It’s the component that actually forwards packets at line rate (high speed), based on flow rules installed by OVS.



# What is the Kernel Datapath?



It’s the "fast path" for packet forwarding in OVS. When a packet arrives:



1. The OVS bridge checks whether a matching flow rule exists in the kernel datapath.



2. If a rule exists, the kernel immediately forwards the packet.



3. If no rule exists, the packet is sent to userspace (ovs-vswitchd) for processing.



    - ovs-vswitchd then decides what to do, and installs a new flow rule in the kernel.



    - Future packets of the same kind follow this new kernel flow rule, fast and directly.



This architecture allows OVS to handle millions of packets per second without userspace overhead for each one.





# Where does the kernel datapath live?



The kernel module is called openvswitch.ko.



You can view datapaths with:



```

sudo ovs-dpctl show

```



You can see kernel flows with:



```

sudo ovs-dpctl dump-flows

```



# Kernel Datapath Flow Example



Let’s say a VM A sends a packet to VM B:



1. VM A sends a packet to its tap interface.



2. The packet reaches the OVS bridge (in the kernel).



3. The kernel datapath checks flow rules:



    - Match: `in_port=1, dl_dst=MAC_B → output: 2`



4. If rule found → packet forwarded immediately.



5. If no rule → sent to userspace (ovs-vswitchd), which:



    - Looks at OVSDB and MAC tables.



    - Decides the output port (e.g., VXLAN, tap interface).



    - Installs rule into kernel datapath.





# OVS Example Workflow



- VM sends a packet → virtual NIC.



- The packet is passed to the OVS bridge.



- OVS matches the packet against flow rules.
    - If rule exists: forwards based on action.

    - If not: sends to userspace for decision (like OpenFlow controller).



- Packet is forwarded to the correct interface (another VM, a physical NIC, or a VXLAN tunnel).





# OVS in Virtualization



In KVM-based virtualization:



- VMs are attached to virtual bridges (e.g., br-int).



- OVS handles traffic between VMs, external interfaces, and tunnels.



- Can create VXLAN tunnels to other OVS instances on different hosts.





# Common commands of OVS

## Install OVS

```
sudo apt update
sudo apt install openvswitch-switch -y

```

## 1. Show OVS Configuration



```

ovs-vsctl show

```



Shows all bridges, ports, and interfaces managed by OVS.



## 2. Create / Delete Bridge



```

ovs-vsctl add-br br0

ovs-vsctl del-br br0

```



## 3. Add / Remove Ports



```

ovs-vsctl add-port br0 eth1

ovs-vsctl del-port br0 eth1

```



Or add a port with a specific name:



```

ovs-vsctl add-port br0 veth1 -- set Interface veth1 type=internal

```



## 4. View Flow Rules (OpenFlow)



```

ovs-ofctl dump-flows br0

```



## 5. Add / Delete Flow Rules



```

ovs-ofctl add-flow br0 "in_port=1,actions=output:2"

ovs-ofctl del-flows br0

```



## 6. Trace Packet Through OVS



```

ovs-appctl ofproto/trace br0 "in_port=1,dl_dst=aa:bb:cc:dd:ee:ff"

```



## 7. Kernel Datapath Tools



Show datapaths:



```

ovs-dpctl show

```



Show datapath flows (kernel):



```

ovs-dpctl dump-flows

```





## 8. Create VXLAN Tunnel Port



```

ovs-vsctl add-port br0 vxlan0 

&nbsp; -- set interface vxlan0 type=vxlan 

&nbsp; options:remote_ip=192.168.1.2 

&nbsp; options:key=flow

```



## 9. Set Controller (SDN)



```

ovs-vsctl set-controller br0 tcp:192.168.1.100:6633

```



## 10. List Interfaces



```

ovs-vsctl list interface

```



## 11. Clear All Configs (Caution!)



```

ovs-vsctl del-br br0

ovs-vsctl --all destroy bridge

```







