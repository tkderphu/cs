# This is basic command about linux network

# 1. Ip command

ip is the modern and preferred replacement for ifconfig, route, and more.

Subcommands:
- ip a or ip addr – Show addresses

- ip link – Show/set interface state

- ip route – Show/set routing

- ip netns – Network namespaces

# 2. ip link (Interface control)

Manage physical and virtual interfaces.

```
ip link show                     # List interfaces
ip link set eth0 up             # Enable eth0
ip link set eth0 down           # Disable eth0
ip link add br0 type bridge     # Create bridge br0
ip link delete br0              # Delete bridge
```

# 3. ip route (Routing control)

Set or view routing tables.

```
ip route show
ip route add default via 192.168.1.1          # Add default route
ip route add 10.0.0.0/24 via 192.168.1.100    # Route to specific subnet
ip route del default                          # Delete default route
```


# 4. ip netns (Network Namespaces)

In Linux, a network namespace (netns) provides isolation of network environments within the same system. Each network namespace has its own interfaces, routing tables, firewall rules, and more—like having a separate virtual network stack.

- Used to isolate network stacks (often in containers or virtual networks).

# Basic Concepts

- Default namespace: What your system boots with.

- New namespace: You can create a new isolated network environment.

- Veth pair: A virtual cable to connect different namespaces (like plugging a cable between two routers).

- Bridge: Used to connect namespaces together or connect them to the outside world.

- NAT: Needed if you want a namespace to access the internet via the host.

# Basic Commands
1. List all network namespaces

```
ip netns list
```

2. Create a network namespace

```
sudo ip netns add ns1
```

3. Show IP addresses in a namespace

```
sudo ip netns exec ns1 ip a
```

4. Create a veth pair

```
sudo ip link add veth0 type veth peer name veth1
```

5. Connect veth1 to namespace

```
sudo ip link set veth1 netns ns1
```

6. Assign IP addresses

```
sudo ip addr add 10.0.0.1/24 dev veth0
sudo ip link set veth0 up

sudo ip netns exec ns1 ip addr add 10.0.0.2/24 dev veth1
sudo ip netns exec ns1 ip link set veth1 up
sudo ip netns exec ns1 ip link set lo up
```

7. Ping between host and namespace

```
ping 10.0.0.2
sudo ip netns exec ns1 ping 10.0.0.1
```

8. Access to internet from namespaces

- Enable IP forwarding: ```echo 1 > /proc/sys/net/ipv4/ip_forward```
-  Use iptables for NAT: ```iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o eth0 -j MASQUERADE```

9. Clean up

```
ip netns delete ns1
ip netns delete ns2
```


# 5. iptables (Legacy firewall tool)

```iptables``` is a Linux firewall tool used to control network traffic:

- Allow / deny connections

- Do NAT (Network Address Translation)

- Forward packets

- Log, modify, or reject packets

It works using rules organized in tables and chains.

Controls packet filtering, NAT, and port forwarding.

# Structure of iptables

## 1. Tables

Each table has a different purpose:

| Table    | Purpose                                               |
| -------- | ----------------------------------------------------- |
| `filter` | Default. Controls packet **filtering** (ACCEPT, DROP) |
| `nat`    | Used for **NAT (masquerade, port forwarding)**        |
| `mangle` | Modify packet headers (TTL, QoS)                      |
| `raw`    | Disable connection tracking                           |


Usually, you'll use:

- filter → for accepting or rejecting traffic

- nat → for routing and masquerading (NAT)


## 2. Chains

Chains are processing points where rules are applied:

| Chain         | Description                                         | Table           |
| ------------- | --------------------------------------------------- | --------------- |
| `INPUT`       | Traffic **to the host itself**                      | `filter`        |
| `OUTPUT`      | Traffic **sent by the host itself**                 | `filter`        |
| `FORWARD`     | Traffic **routed through the host**                 | `filter`        |
| `PREROUTING`  | Modify packets **before routing**                   | `nat`, `mangle` |
| `POSTROUTING` | Modify packets **after routing** (NAT happens here) | `nat`           |


# Key Concepts

| Term         | Meaning                                |
| ------------ | -------------------------------------- |
| `ACCEPT`     | Allow packet                           |
| `DROP`       | Silently discard packet                |
| `REJECT`     | Drop and send error response           |
| `MASQUERADE` | Source NAT for dynamic IP (e.g., DHCP) |
| `DNAT`       | Destination NAT (port forwarding)      |
| `SNAT`       | Source NAT (static IP)                 |

# Command

Structure:

```
sudo iptables [-t <table>] <command> <chain> [match] [action/target]
```

| Part         | Example                        | Meaning                                       |
| ------------ | ------------------------------ | --------------------------------------------- |
| `-t <table>` | `-t nat`, `-t filter`          | Table to operate on (default: `filter`)       |
| `<command>`  | `-A`, `-I`, `-D`, `-L`, etc.   | What to do (Add, Insert, Delete, List…)       |
| `<chain>`    | `INPUT`, `OUTPUT`, `FORWARD`   | Chain (processing stage)                      |
| `[match]`    | `-p tcp`, `--dport 80`         | What to match (protocol, IP, port, interface) |
| `[target]`   | `ACCEPT`, `DROP`, `MASQUERADE` | What to do when match occurs                  |


| Command | Description                          |
| ------- | ------------------------------------ |
| `-A`    | Append rule to end of chain          |
| `-I`    | Insert rule at top (position 1)      |
| `-D`    | Delete rule (by number or full rule) |
| `-L`    | List rules in a chain                |
| `-F`    | Flush all rules in a chain           |


| Table  | Chains                                |
| ------ | ------------------------------------- |
| filter | `INPUT`, `FORWARD`, `OUTPUT`          |
| nat    | `PREROUTING`, `POSTROUTING`, `OUTPUT` |
| mangle | `PREROUTING`, `POSTROUTING`, etc.     |


# Example

## 1. Allow SSH

```
sudo ip tables  -A INPUT -p tcp --dport 22 -j ACCEPT
```

- -A INPUT: Append to INPUT chain

- -p tcp: Match TCP packets

- --dport 22: Destination port 22

- -j ACCEPT: Allow it


## 2. Drop access to port 8080

```
sudo ip tables -A -p tcp --dport 8080 -j DROP
```

## 3. NAT (Masquerade) for namespace/VM subnet

```
sudo iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o enp2s0 -j MASQUERADE
```

- -t nat: Work in nat table

- POSTROUTING: After routing

- -s 10.0.0.0/24: Source subnet

- -o enp2s0: Going out real NIC

- -j MASQUERADE: Rewrite source IP

## 4. Forward traffic(for router)

```
sudo iptables -A FORWARD -i veth-router1 -o enp2s0 -j ACCEPT
sudo iptables -A FORWARD -i enp2s0 -o veth-router1 -m state --state RELATED,ESTABLISHED -j ACCEPT
```

## 5. List Rules

```
sudo iptables -L -v          # filter table
sudo iptables -t nat -L -v   # nat table
```

# Summary structure

```
sudo iptables -t <table> -A <chain> -p <protocol> -s <src> -d <dst> \
     --sport <src_port> --dport <dst_port> -i <in_iface> -o <out_iface> \
     -j <target>
```
