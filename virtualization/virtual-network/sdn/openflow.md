# Note about openflow

# 1. What is openflow

Openflow is a network communication protocol that lets a centralized controller(like in SDN) tell networks switch how to forward packets.

Think of it:

`Intead of each switch routes itself, it asks a brain(controller) for instructions.`

# 2. How it works

The main idea:

1. Traditional networks: The switch/router has its own data plane and control plane. They run routing protocols and decide forwarding locally

2. With openflow: The controll plane moves to a controller. The switches become "dump" packet forwarders, following the rules sent by controller

Flow of packets:

- A packet enters a switch.

- The switch checks its flow table for matching rules.

    - If match → forward, drop, or modify as per rule.

    - If no match → send packet (or its header) to the controller via OpenFlow protocol.

- The controller decides what to do and installs a new rule in the switch.

- Future packets matching that flow get processed locally without bothering the controller.

# 3. Key Components

Openflow architecture has three main parts:

## a, controller

- The brain of the network
- Runs network apps(routing, firewall, load balancing)
- Examples: ONOS, OpenDaylight, Ryu, Floodlight

## b, openflow switch

- Can be hardware or software(like ovs, ..etc)
- contains one or more flow tables with entries like:

```
Match: (src IP, dst IP, src port, protocol, VLAN, etc.)
Action: forward to port X, drop, send to controller, modify header
Stats: packet/byte counters for the flow
```

## c, openflow channel

- A secure TCP/TLS connection between controller and switch
- Used to:
    - send flow mod message (controller -> switch)
    - send packet-in events(switch -> controller)
    - get statistics.

# 4. Why use openflow

Openflow is used because its decouple control plane from data plane, enabling:

- Centralized control - Manage the entire network from one place
- Programmability - Change how the network behaves through software, without physically touching devices
- Vendor independence - Works on multiple hardware vendors if they support Openflow
- Dyamic policies - Can install flows on-demand for load balancing, firewall, QoS, ...etc
- Innovation - Enables rapid prototyping of new networking ideas without waiting for hareware vendors

