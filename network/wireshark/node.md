# Note about wireshark

Wireshark is a powerful open-source network protocol analyzer used to inspect data flowing through a network in real-time. Here's a detailed tutorial that walks you through its installation, interface, capture filters, analysis techniques, and usage scenarios.


## 1. Installation

```
sudo apt update
sudo apt install wireshark
```


Allow non-root users to capture:

```
sudo usermod -aG wireshark $USER
```

Launch wireshark

```
wireshark
````


## 2. Interface Overview


| Area                    | Description                          |
| ----------------------- | ------------------------------------ |
| **Menu Bar**            | File, Edit, Capture, Analyze, etc.   |
| **Main Toolbar**        | Start/Stop capture, open/save files  |
| **Filter Bar**          | Apply filters to narrow down packets |
| **Packet List Pane**    | Summary of all captured packets      |
| **Packet Details Pane** | Expandable view of a selected packet |
| **Packet Bytes Pane**   | Hex + ASCII representation           |
