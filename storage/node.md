# Storage

# What is storage

Storage is a processing for store data so that users can use after that

# What type of storage

# 1. Block storage

- Sector is a smallest unit is stored on disk

- Block is a smallest unit(of filesystem) used  reading and writing data and manage by OS

- Each block is fixed size, different OS can use different size, common size are usually 4KB, 8KB

- Data is devided small and store on disk

- Example a file have 10 kb => OS will be devided that file to 3 block: 4 + 4 + 2, but 2kb of that block will be wasted(internal fragmentation)

- Each block has its number then  OS calculate address of that block and can access(reading, writing that block): block_number * block_size

- Summary: 

    - Block = many sector
    - File = many block

# 2. LVM(Logical volume manager)

LVM is a powerful storage management technology in Linux that allows flexible management of disk space using logical volumes instead of traditional partitions.

# 3. Key Concepts

## 1. Physical Volume (PV)

Underlying physical storage devices (e.g., /dev/sda1, /dev/nvme0n1)

Can be entire disks or partitions

Initialized with pvcreate

## 2. Volume Group (VG)

A pool of storage made by combining multiple PVs

Created using vgcreate

Example: vgcreate my_vg /dev/sda1 /dev/sdb1

## 3. Logical Volume (LV)

Virtual block devices carved from a VG

Created using lvcreate

Used like regular partitions (can be formatted with ext4, xfs, etc.)

Example: lvcreate -L 10G -n my_lv my_vg

## 4. Snapshots

Point-in-time copies of an LV

Useful for backups or testing

Example: lvcreate --snapshot --name my_snapshot -L 1G /dev/my_vg/my_lv


<!-- - Object storage

    -  Dữ liệu lưu dưới dạng đối tượng kèm metadata (VD: Amazon S3, OpenStack Swift). Dùng cho lưu trữ lớn, backup.

    
- File storage -->