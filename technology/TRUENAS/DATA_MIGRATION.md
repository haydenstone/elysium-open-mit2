# DATA_MIGRATION.md - TrueNAS SCALE Data Migration Procedure

**Goal:** To safely and efficiently migrate existing data to the TrueNAS SCALE storage server.

**Current Situation:**

* Experiencing permissions issues preventing direct data migration.
* Utilizing a Docker container with `--privileged` mode as a temporary workaround for accessing external drives.

**Recommended Data Migration Approach (Review and Improve Security):**

The current Docker container method using `--privileged` poses significant security risks and should be considered a temporary and last resort. Explore alternative, more secure methods for data migration.

**Alternative Data Migration Methods (Preferred):**

1.  **Network Shares (SMB/CIFS or NFS):**
    * **Prerequisites:** Ensure the source of your data (e.g., another computer, external drive connected to another computer) can share data via SMB or NFS.
    * **Steps:**
        * **Share Data Source:** Configure SMB or NFS sharing on the source device.
        * **Mount Remote Share on TrueNAS SCALE:** Use the TrueNAS SCALE web interface or command line to temporarily mount the remote share.
            * **Web Interface (SMB/CIFS):** Go to **Shares** -> **Windows (SMB) Shares** -> **Add**. In the "Auxiliary Parameters," you can attempt to mount a remote share using `mount -t cifs //remote_server/share /mnt/temp_mount -o username=...,password=...`. This is not a standard TrueNAS feature for persistent mounts, but can be used for temporary access.
            * **Command Line (SMB/CIFS):** `mount -t cifs //remote_server/share /mnt/temp_mount -o username=...,password=...`
            * **Web Interface (NFS):** Go to **Shares** -> **Unix (NFS) Shares** -> **Add**. Configure an NFS share on the source and then on TrueNAS SCALE, you can attempt to mount it temporarily via the command line: `mount -t nfs remote_server:/share /mnt/temp_mount`.
        * **Transfer Data:** Use `rsync` or `cp` to transfer data from the mounted temporary location (`/mnt/temp_mount`) to your TrueNAS SCALE datasets (`/mnt/your_pool/your_dataset`).
        * **Unmount:** Unmount the temporary share after the transfer: `umount /mnt/temp_mount`.

2.  **Directly Attached Storage (USB - Use with Caution):**
    * **Prerequisites:** Connect the external drive directly to the TrueNAS SCALE server via USB.
    * **Steps:**
        * **Identify Drive:** Use `lsblk` or the TrueNAS SCALE web interface (Storage -> Disks) to identify the device path of the external drive (e.g., `/dev/sdb1`).
        * **Mount Drive (Command Line):** Create a temporary mount point and mount the drive. You may need to install file system utilities (e.g., `apt install ntfs-3g` for NTFS).
            ```bash
            mkdir /mnt/external_drive
            mount -t <filesystem_type> /dev/sdb1 /mnt/external_drive
            ```
        * **Transfer Data:** Use `rsync` or `cp` to transfer data from `/mnt/external_drive` to your TrueNAS SCALE datasets (`/mnt/your_pool/your_dataset`).
        * **Unmount Drive:** `umount /mnt/external_drive`.

**Data Migration using Docker Container (Temporary and High-Risk - Use with Extreme Caution):**

**Warning:** This method uses `--privileged` mode, granting the container full access to the host system. This is a significant security risk and should only be used as a last resort when other methods are not feasible.

**Steps:**

1.  **Access the TrueNAS SCALE Shell:**
    * Log in as root.

2.  **Run the Ubuntu Container:**
    ```bash
    docker run -it --rm --privileged \
      --device /dev/<external_drive_device>:/dev/<external_drive_device> \
      -v /mnt/<your_pool_name>:/storage \
      ubuntu:latest bash
    ```
    * **Replace:**
        * `<external_drive_device>`: The actual device path of your external drive (e.g., `sdb1`).
        * `<your_pool_name>`: The name of your TrueNAS SCALE storage pool (e.g., `tank`).

3.  **Install Necessary Packages:**
    * Inside the container's shell:
        ```bash
        apt update -y
        apt install ntfs-3g rsync -y
        ```

4.  **Mount the External Drive:**
    * Create a mount point and mount the external drive:
        ```bash
        mkdir /mnt/external
        mount -t <filesystem_type> /dev/<external_drive_device> /mnt/external
        ```
        * **Replace:** `<filesystem_type>` with the actual file system of your external drive (e.g., `ntfs-3g`, `ext4`).

5.  **Transfer Data:**
    * Use `rsync` to transfer data:
        ```bash
        rsync -avh --progress /mnt/external/ /storage/<your_dataset>/
        ```
        * **Replace:** `<your_dataset>` with the target dataset in your TrueNAS SCALE pool (e.g., `share`).

6.  **Unmount and Exit:**
    ```bash
    umount /mnt/external
    exit
    ```

**Important Considerations for All Migration Methods:**

* **Permissions:** Carefully manage permissions on the destination datasets in TrueNAS SCALE to ensure proper access for users and services. Investigate and resolve existing permission issues.
* **Device Paths:** Double-check all device paths to avoid data loss or targeting the wrong storage.
* **Security:** Prioritize secure data transfer methods. Avoid `--privileged` Docker containers if possible.
* **Integrity:** Verify data integrity after transfer using checksums or other verification methods.
* **Large Transfers:** For large datasets, consider running `rsync` in stages or using tools designed for large file transfers.
* **Testing:** Test the migration process with a small subset of data first to ensure it works as expected.

**Next Steps for Data Migration:**

1.  **Investigate and Resolve Permissions Issues:** Focus on understanding and fixing the current permissions problems preventing standard data access.
2.  **Attempt Preferred Migration Methods:** Try using network shares or directly attached storage (without Docker) for data transfer.
3.  **Use Docker Container (with extreme caution) as a Last Resort:** If other methods fail, use the Docker container method, being fully aware of the security implications.
4.  **Verify Data Integrity:** After any migration, thoroughly verify that all data has been transferred correctly.