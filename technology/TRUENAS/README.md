# TrueNAS SCALE Storage Server Project

**Project Goal:** To build a robust and versatile storage server using TrueNAS SCALE, capable of storing virtual hard disks, supporting multiple storage types (block, object, file), and providing flexible network sharing and cloud compatibility.

## Hardware

* **Motherboard:** Dell Studio XPS 8100
* **CPU:** Intel Core i7 860 @ 2.8 GHz
    * L3 Cache: 8 MB
    * L2 Cache: 1 MB
    * L1 Cache: 256 KB
* **RAM:** 16GB DDR3 @ 1333 MHz
* **Storage:**
    * 4 x 4TB Hard Drives (SATA)
        * Configured in ZFS RAIDZ2, providing 6.92TB usable space.
    * 1 x 16GB SSD (Boot Drive) - *Note: This drive is currently known to be faulty and will be replaced.*
    * 1 x 250GB SSD (SLOG and L2ARC)
        * Partitioned for SLOG and L2ARC.
* **SATA Controller:** 2-port SATA PCI card (6 total SATA ports)
* **Network:** Gigabit Ethernet

## Software

* **Operating System:** TrueNAS SCALE 24.10.2.1

## Storage Configuration

* **RAID:** ZFS RAIDZ2 (4 x 4TB drives)
    * Usable Capacity: 6.92 TB
* **Boot Pool:** 16GB SSD (Faulty - to be replaced)
* **SLOG:** Partitioned 250GB SSD
* **L2ARC:** Partitioned 250GB SSD
* **Datasets:**
    * `/storage/apps`
    * `/storage/backups`
    * `/storage/games`
    * `/storage/home` (SMB Dataset)
    * `/storage/images`
    * `/storage/media`
    * `/storage/programs`
    * `/storage/share`
    * `/storage/users` (and sub-datasets for each user)
    * `/storage/vms` (and sub-datasets for each zvol)
    * `/storage/zvols` (for virtual machine block storage)

## Network Configuration

* **File Sharing:** Samba, NFS, SSHFS
* **Block Storage:** iSCSI
* **Object Storage:** MinIO (S3-compatible)

## Virtualization

* Virtual Hard Disk Storage for VMs

## Initial Setup Steps and Observations

1.  **Downloaded TrueNAS SCALE 24.10.2.1 ISO:** [https://www.truenas.com/download-truenas-scale/](https://www.truenas.com/download-truenas-scale/)
2.  **Created bootable USB drive using Etcher.** (Note: Previous attempts to create a bootable drive using Ventoy failed with "Invalid Magic Number" error.)
3.  **Booted in BIOS (legacy) mode.** (Note: TrueNAS SCALE will use GPT for data drives, allowing 4TB drive usage.)
4.  **Completed TrueNAS SCALE installation and first boot.** (Note: First boot experienced a delay with "job IX-ETC service start running with a timeout of 5 minutes." This delay is likely due to first-time initialization and hardware detection. System also reported "failed to start IX sync DIS" and "sync disc cache table see system control status failed for details," indicating a disk service issue. This may be related to the faulty boot drive.)
5.  **Logged in using the truenas\_admin username and the password set during installation.**
6.  **Determined that the ZFS pool must be created before the creation of user accounts, due to the home directory location.**
7.  **Decided to create an encrypted ZFS RaidZ2 pool.**
8.  **Determined that using ZFS RaidZ2 is better than Hardware raid mirrors, and then ZFS raid0.**
9.  **Determined that the 250 gigabyte drive will be used for the SLOG and L2ARC device.**
10. **Created the ZFS RAIDZ2 pool.**
11. **Verified the pool is online and healthy.**
12. **Created the `/storage/zvols` dataset for virtual machine block storage.**
13. **Created the `/storage/home` dataset as a SMB dataset.**
14. **Created local user with SMB authentication, and home directory within the `/storage/home` dataset.**
15. **Created the following datasets, with varying presets ie. 'SMB', 'Multiprotocol':**

## Current Issues

* System is currently running from a USB boot drive due to the faulty 16GB SSD.

## Next Steps

1.  **Security Configuration:**
    * Configure firewall rules to restrict access.
    * Implement 2FA (Two-Factor Authentication) for enhanced security.
2.  **Configure MinIO:**
    * Set up MinIO for S3-compatible object storage.
    * Define access policies and buckets.
3.  **Virtualization Setup:**
    * Configure virtualization (if needed).
    * Create and manage virtual machines.
4.  **Reporting and Monitoring:**
    * Set up reporting and monitoring.
    * Monitor system health, performance, and storage usage.
5.  **Performance Testing and Optimization:**
    * Test and optimize performance.
    * Identify and address any bottlenecks.
6.  **Replace Faulty Boot Drive:**
    * Install the new, reliable SSDs when they arrive.
    * Migrate the TrueNAS SCALE installation to the new boot drive.