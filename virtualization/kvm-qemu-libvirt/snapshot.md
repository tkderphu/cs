# Note about snapshot

A snapshot is a point-in-time-copy of the state of a resource(VM, volume, or filesystem). It lets you roll back or create new resources from that exact state later

Think of it like a "save game" in a video game

# Type of snapshots

## 1. VM snapshot(via hypervior/libvirt)

- Captures the state of a virtual machine:
    - Disk state(qcow2 backing file or overlay)
    - Optional: Memory(RAM) + CPU(state) so vm can resume exectly where it was
- Example(libvirt):
    - virsh snapshot-create-as --domain vm1 snap1
- Use case:
    - Before upgrading OS, take a snapshot => if upgrade fails, revert