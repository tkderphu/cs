# 1. Network Interface Card (NIC) Overview

A Network Interface Card (NIC) is the component that makes it possible for a device (PC, server, VM, container, router, switch) to connect to a network.

It exists in two main forms:

- Physical NIC → A real hardware card (Ethernet, Wi-Fi, Fiber).

- Virtual NIC (vNIC) → A software-emulated card used in virtualization or SDN.

Every NIC, whether physical or virtual, works at OSI Layer 2 (Data Link Layer) and has a MAC address (unique identifier).

# 2. Functions of a NIC

1. Data Conversion

- Converts data from the computer into network frames.

- For Ethernet → wraps data into Ethernet frames.

- For Wi-Fi → uses 802.11 wireless frames.

2. Communication

- Transmits and receives frames on the network medium (cable, fiber, wireless, or virtual link).

3. Addressing

- Each NIC has a MAC address.

- This is used for point-to-point delivery in the same LAN.

4. Offloading (modern NICs)

- Offload tasks from CPU (checksum, segmentation, encryption).

- This improves performance in high-speed networks (10G, 40G, 100G).

# 3. Physical NIC vs Virtual NIC (TAP, vNIC, etc.)

| Feature         | **Physical NIC**                                           | **Virtual NIC (vNIC, TAP, etc.)**                                  |
| --------------- | ---------------------------------------------------------- | ------------------------------------------------------------------ |
| **Existence**   | Hardware (chip + port).                                    | Purely software inside OS or hypervisor.                           |
| **MAC Address** | Burned into hardware (but can be overridden).              | Assigned dynamically by software.                                  |
| **Medium**      | Connects to physical medium (Ethernet cable, Wi-Fi radio). | Connects to virtual switches, bridges, tunnels.                    |
| **Usage**       | Real computers, servers, routers.                          | Virtual Machines (VMs), Containers, SDN (e.g., OVS, Linux Bridge). |
| **Examples**    | `eth0`, `wlan0`, `ens33` on Linux.                         | `tap0`, `vnet0`, `veth0` on Linux, VMware vNIC, Hyper-V vNIC.      |


# 4. Special Case: TAP Device (like tap0)

When you run:

```
ip tuntap add dev tap0 mode tap
```

you’re creating a virtual NIC that works at Layer 2 (like an Ethernet card).

TAP = Layer 2 (Ethernet frames).

TUN = Layer 3 (IP packets).

A TAP device:

- Has a MAC address like a physical NIC.

- Can be attached to a bridge/OVS, so it acts like a “cable” connecting a VM to the host.

Allows user-space programs (like QEMU, OpenVPN) to send/receive Ethernet frames directly.

# 5. How They Work Together

Imagine you run a VM with QEMU/KVM:

The VM sees a virtual NIC (e.g., Intel E1000).

That NIC is connected internally to a TAP device (tap0) on the host.

The host attaches tap0 to an OVS bridge (br0), which is connected to the physical NIC (eth0).

So the data path is:

`VM’s virtual NIC → TAP device → OVS bridge → Physical NIC → Outside network`

## So in short:

Physical NIC = real hardware card connecting machine to network.

Virtual NIC (TAP, vNIC) = software NIC for VMs/containers, behaves like real NIC but only inside OS.

Both can be attached to switches/bridges to enable communication.