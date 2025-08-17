# What is iSCSI

iSCSI is a block-level storage protocol that allows SCSI commands to be sent over a TPC/IP network

- SCSI(small computer system interface) is the command set used for talking to storage devices
- iSCSI encapsulates SCSI commands inside TCP packets and sends them over an IP network

- In short: It makes remote storage appear to client as if it's a locally attached disk

# Components

iSCSI has two main components:

1. Initiator(client)

    - Sends SCSI commands over IP to the target
    - Can be:
        - Software initiator
        - Hardware initiator
2. Target(server/storage)
    - Listens for connections and responds to SCSI commands
    - Can be:
        - Dedicated storage appliance
        - Software target

# How iSCSI works

The flow is:

```
[Application] → [File System] → [iSCSI Initiator] → [TCP/IP Network] → [iSCSI Target] → [Block Storage Device]
```

Steps:

1. Initiator connects to target over TCP/IP(usually port 3260)
2. Target authenticates initiator
3. Initiator sends SCSI commands inside TCP packets
4. Target processes commands and returns responses
5. OS treats target's block device as a local disk

# Protocol & Ports

- Transport protocol: TCP
- Default port: 3260
- Encapsulation:
    - SCSI command -> iSCSI PDU -> TCP -> IP -> Ethernet

# Authentication and Security

iSCSI can be secured with:

1. CHAP(Challenge-handshake authnetication protocol)

    - One-way chap: target authenticates initiator
    - Mutual chap: both authenticates each other

2. IPSec for encryption at the ip layer

3. Access control lists on the target

# Addressing & Naming

- iSCSI uses IQNs(iSCSI qualified names) for unique identification

- Format

    ```
    iqn.yyyy-mm.<reversed-domain-name>:optional-string
    ```
- Example:

    ```
    iqn.2025-08.com.example:storage.disk1
    ```
# Key terms

| Term                      | Meaning                                           |
| ------------------------- | ------------------------------------------------- |
| LUN (Logical Unit Number) | A block device exposed by the target              |
| Session                   | Connection between initiator and target           |
| Discovery                 | Process of finding available targets              |
| Multipath I/O (MPIO)      | Multiple network paths for redundancy/performance |

# Multipathing & High availability

- iSCSI supports MPIO to:

    - Increase bandwidth(load balancing)
    - Provide fault tolerance

- Example: Two network initerfaces connected to different switches leading to same storage

# Performace consideration

- Jumbo Frames (9000 bytes MTU) → reduce CPU load & increase throughput.

- Dedicated storage network → avoids competition with normal LAN traffic.

- TCP Offload Engine (TOE) in NIC → offloads iSCSI/TCP processing from CPU.

- Link aggregation (LACP) for higher bandwidth.


# Advantages

- Uses standard Ethernet infrastructure (no need for expensive Fibre Channel).

- Can work over existing IP networks.

- Flexible — supports long distances (over WAN).

- Software-based implementation possible (no special hardware required).

# Disadvantages

- Higher latency than Fibre Channel (due to TCP/IP overhead).

- More CPU usage if not offloaded to hardware.

- Performance depends heavily on network quality.

- Vulnerable to network congestion.

# Example setting

