# Iptables

## What is iptables?

iptables is a Linux firewall tool used to:

- Allow traffic

- Block traffic
- Control how packets move through your server

It works inside the Linux kernel using the Netfilter framework.

```
Internet → Your Server → Decision (Allow or Drop)
```

## Understanding Tables

iptables has multiple tables:

```
| Table  | Purpose                          |
| ------ | -------------------------------- |
| filter | Filtering traffic (ALLOW/DROP)   |
| nat    | Network address translation      |
| mangle | Modify packets                   |
| raw    | Special packet handling          |
```

## chains in filter table

Filter table has 3 chains:

```
| Chain   | What it handles                |
| ------- | ------------------------------ |
| INPUT   | Traffic going INTO server      |
| OUTPUT  | Traffic going OUT from server  |
| FORWARD | Traffic passing THROUGH server |
```

## INPUT

Traffic from outside → your server

Example:

- SSH from your laptop to server

- HTTP request to web server

```
Client → Server (INPUT)
```

## OUTPUT

Traffic from server → outside

Example:

- Server downloads updates

- Server connects to database

```
Server → Internet (OUTPUT)
```

## FORWARD

Traffic passing through server

Example:

- Server acts as router

- Compute node forwarding traffic to VM

- NAT gateway

```
Client → Server → VM
```

That middle server uses FORWARD.

## Basic Commands

## Show rules

```
iptables -L
```

More detailed:

```
iptables -L -v -n
```

- -L → list

- -v → verbose (packet count)

- -n → no DNS resolve (faster)

## Default Policy (-P)

```
iptables -P INPUT DROP
```

-P = Policy

This mean: 

```
If no rule matches → DROP everything
```

Very important concept.

## Rule Structure (Core Understanding)

Ex:

```
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```

Break it:

| Part       | Meaning                    |
| ---------- | -------------------------- |
| -A INPUT   | Append rule to INPUT chain |
| -p tcp     | Protocol TCP               |
| --dport 22 | Destination port 22        |
| -j ACCEPT  | Jump to ACCEPT action      |

## 6. First Real Firewall (Beginner Safe Config)

```
# Reset everything
iptables -F

# Default deny
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow loopback
iptables -A INPUT -i lo -j ACCEPT

# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow HTTP
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
```

Why ESTABLISHED is Important?

When you SSH into server:

- Laptop → Server (NEW)

- Server → Laptop (ESTABLISHED)

If you block ESTABLISHED, replies won't work.

## 7. Intermediate Level – Match Extensions

iptables can match many conditions.

## Match by Source IP

```
iptables -A INPUT -s 192.168.1.10 -j ACCEPT
```

## Block specific IP

```
iptables -A INPUT -s 1.2.3.4 -j DROP
```

## Match by Interface

```
iptables -A INPUT -i eth0 -p tcp --dport 22 -j ACCEPT
```

## Match by State (Connection Tracking)

```
-m conntrack --ctstate ESTABLISHED,RELATED
```

## 8️. Advanced Concepts

## 8.1 Packet Flow in Filter Table

Order of processing:

For traffic entering server:

```
1. PREROUTING (nat/mangle)
2. INPUT (filter) ← here
```

For traffic forwarded:

```
1. PREROUTING
2. FORWARD ← here
3. POSTROUTING
```

For outgoing traffic:

```
1. OUTPUT ← here
2. POSTROUTING
```

Filter table only affects:

- INPUT
- OUTPUT
- FORWARD

## 8.2 Rule Order Matters (VERY IMPORTANT)

iptables reads from top → bottom.

First match = stop.

Example:

```
iptables -A INPUT -j DROP
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```


SSH will NEVER work ❌

Because DROP is first.

Correct:

```
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -j DROP
```

## 8.3 Custom Chains (Professional Setup)

Create your own chain:

```
iptables -N SSH_CHECK
```

Jump to it:

```
iptables -A INPUT -p tcp --dport 22 -j SSH_CHECK
```

Inside SSH_CHECK:

```
iptables -A SSH_CHECK -s 192.168.1.0/24 -j ACCEPT
iptables -A SSH_CHECK -j DROP
```

This makes firewall clean and modular.

## 8.4 Logging Before Drop

Production best practice:

```
iptables -A INPUT -j LOG --log-prefix "DROP_INPUT: "
iptables -A INPUT -j DROP
```

Now you can monitor in:

```
/var/log/syslog
```

## 8.5 Rate Limiting (Anti-Brute Force)

```
iptables -A INPUT -p tcp --dport 22 -m limit --limit 5/min -j ACCEPT
```

Limit SSH attempts.

More advanced:

```
-m recent
```

## 8.6 Firewall in Virtualization

If you have:

Compute node → VM via OVS

Then:

- INPUT → traffic to compute node

- FORWARD → traffic to VM

- OUTPUT → traffic from compute node

If VM has duplicate IP in different subnet:

Firewall decision depends on:

- Interface

- Routing table

- Conntrack

iptables does not care about duplicate IP if:

- They are on different bridges

- Kernel routing separates them

## 9. Debugging Filter Table

See packet counters

```
iptables -L -v -n
```

Look at:

- pkts

- bytes

If rule counter = 0 → rule not matching.

## Trace packet

```
iptables -t raw -A PREROUTING -j TRACE
```

Check:

```
dmesg
```

Advanced debugging tool.

## 10. Production Best Practices

- Default DROP on INPUT
- Allow ESTABLISHED first
- Use specific rules
- Log before DROP
- Avoid too many rules
- Use custom chains
- Save config with:

    - iptables-save
- Restore:

    - iptables-restore