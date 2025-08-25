# Note about vm work with ovs

1. Create bridge from ovs: br1

```
ovs-vsctl add-br br1
```

2. Define a libvirt network for OVS

Libvirt doesn’t directly manage OVS like Linux bridges. Instead, we define a network XML that tells libvirt to use br0.

Create ovs-net.xml:

```
<network>
  <name>ovs-net</name>
  <forward mode='bridge'/>
  <bridge name='br1'/>
  <virtualport type='openvswitch'/>
</network>
```

Define and start it:

```
sudo virsh net-define ovs-net.xml
sudo virsh net-start ovs-net
sudo virsh net-autostart ovs-net
```

3. Create vm

```
virt-install \
  --name ubuntu-vm \
  --memory 2048 \
  --vcpus 2 \
  --disk size=20,path=/var/lib/libvirt/images/ubuntu-vm.qcow2 \
  --cdrom /var/lib/libvirt/imges/ubuntu-vm-seed.iso \
  --os-variant ubuntu24.04 \
  --network network=ovs-net,model=virtio \
  --graphics vnc
```

4. verify the VM port on OVS

```
sudo ovs-vsctl show
```

You should see a port like `vnet0` attached to `br1`.

<a href='https://chatgpt.com/c/68a720a6-8f90-8320-ac93-bf697075d1c4'>Link chatgpt</a>

# Attach new port to virtual machine

When attach new interface to vm so interface in vm it is not assigned ip address, to solve this we reload `cloud-init`

To attach new interface we use below commands:

1. Attach interface to available vm:

```
virsh attach-interface --domain ubuntu-vm \
    --type network \
    --source ovs-net \
    --model virtio \
    --mac 52:54:00:aa:bb:cc \
    --live --config
```
- attach to network which is defined in libvirt: `ovs-net`
- `mac 52:54:00:aa:bb:cc`: assign mac to interface
- --live: attaches immediately
- --config: persists after reboot

To see all interface of virtual machine using this command: `virsh domiflist <your_vm_name>`

2. edit file `network-config`:

```
version: 2
ethernets:
  ens3:
    match:
      macaddress: "52:54:00:aa:bb:cc"
    set-name: ens3
    addresses:
      - 192.168.50.101/24
    gateway4: 192.168.50.1
    nameservers:
      addresses: [8.8.8.8, 8.8.4.4]

  ens4:
    match:
      macaddress: "52:54:00:dd:ee:ff"
    set-name: ens4
    addresses:
      - 192.168.50.102/24
```

3. Generate new iso(cloud-init):

```
cloud-localds --network-config=network-config ${VM_NAME}-seed.iso user-data meta-data
```

- Replace the old seed.iso attached to the VM with this new one (can override).

4. Reboot vm

When vm restart then it will run cloud-init.service add find mac address to assign ip

# Remove port from virtual machine