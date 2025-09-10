# Note about lab

# 1. On a single host we will using vlan

Each virtual machine when attach interface to ovs will give which vlan:

```
ovs-vsctl set port veth1-br tag=10
```

Only the same subnet and vlan can be interact with each other

# 2. On multiple host we will use vxlan

When we have multiple hosts and across virtual machine in the same subnet and vlan can comminucate we will use vxlan:

Ex:

- HostA: 192.168.10.135
    - vm1: 192.168.1.1 #vxlan 100
    - vm2: 192.168.2.1 #vxlan 200
- HostB: 192.168.1.3
    - vm1: 192.168.1.4 #vxlan 100
    - vm2: 192.168.2.2 #vxlan 200


In hostA we will configure like this:

```
ovs-vsctl add-port br0 vxlan1001 \
    -- set interface vxlan1001 type=vxlan options:remote_ip=192.168.1.3 options:key=1001
```

In hostB we will configure like this:

```
ovs-vsctl add-port br0 vxlan1002 \
    -- set interface vxlan1002 type=vxlan options:remote_ip=10.0.1.2 options:key=1002
```

# 3. comminucate among subnet

- Each machine create router to route between subnet(vlan) in that machine
- add interface that among host commincate to birdge and add trunk

```
ovs-vsctl add-port br0 eth0 trunk=100,200
```
