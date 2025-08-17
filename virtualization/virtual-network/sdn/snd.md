# What is SDN(software defined network)

SDN is a way of designing and managing networks when the `control` of the network is seperated from the `devices that actually move the packets`

Instead of each switch or router making its own forwarding decisions, you have:

# 1. Three layers in SDN

| Layer                 | Role                                               | Example                                                  |
| --------------------- | -------------------------------------------------- | -------------------------------------------------------- |
| **Application Layer** | Apps that define what you *want* the network to do | Firewall app, load balancer, routing policy              |
| **Control Layer**     | The brain — decides how packets should flow        | SDN controllers like ONOS, OpenDaylight, Ryu, Floodlight |
| **Data Layer**        | The muscle — actually forwards packets             | Open vSwitch, hardware switches that support OpenFlow    |

# 2. Key idea

## Traditional networking:

- Each switch/router has its own control plane (decides where packets go) and data plane (moves packets).

- To change behavior, you log into each device and configure it.

## SDN:

- Control plane is centralized in a controller.

- The switches (like OVS) just do data plane — they forward packets according to flow rules sent by the controller.

- The controller programs the network dynamically using protocols like OpenFlow.

# 3. How SDN works

1. A packet arrives at an OVS switch.

2. OVS checks if it has a matching flow rule.

    - If yes → forward the packet immediately.

    - If no → send the packet to the SDN controller.

3. The controller decides what to do (e.g., route it, drop it, tag it) and sends back a new flow rule.

4. OVS installs that rule and uses it for similar packets in the future.

# Example how SDN work in real world

First i will set up so:

- HostA = VLAN 10 network (192.168.10.0/24)

- HostB = VLAN 20 network (192.168.20.0/24)

- Goal = Let controller handle inter-VLAN communication.

`In this example i will not use controller, i will write directly rules in ovs`

