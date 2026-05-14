# TrueNAS SCALE Data Recovery Procedure

**Scenario:**

* TrueNAS SCALE system fails to boot or becomes inaccessible due to a hardware or software issue.
* Data needs to be recovered from the 4 x 4TB hard drives configured in a ZFS RAIDZ2 pool.

**Recovery Steps:**

1.  **Prepare a Recovery Environment:**
    * Obtain a separate computer with a compatible operating system (e.g., Linux, TrueNAS SCALE).
    * Ensure the recovery environment has enough SATA ports to connect all 4TB drives.
    * Install necessary ZFS tools (e.g., `zfsutils-linux` on Linux).
2.  **Connect the Drives:**
    * Power down the recovery environment.
    * Connect the 4 x 4TB drives to the SATA ports.
    * Power on the recovery environment.
3.  **Identify the ZFS Pool:**
    * Open a terminal or command prompt.
    * Use the command `zpool import` to list available ZFS pools.
    * Identify the pool corresponding to the 4TB drives.
4.  **Import the ZFS Pool:**
    * Use the command `zpool import <pool_name>` to import the ZFS pool. Replace `<pool_name>` with the actual pool name.
    * If the pool is encrypted, provide the encryption keys when prompted.
5.  **Mount the Datasets:**
    * Once the pool is imported, mount the datasets containing the data you need to recover.
    * Use the command `mount -t zfs <pool_name>/<dataset_name> /mnt/<mount_point>`. Replace `<pool_name>`, `<dataset_name>`, and `<mount_point>` with the appropriate values.
6.  **Copy the Data:**
    * Use standard file copy commands (e.g., `cp`, `rsync`) to copy the data from the mounted datasets to a safe location.
    * Example: `rsync -av /mnt/<mount_point>/ /recovery_destination/`
7.  **Verify Data Integrity:**
    * After copying, verify that the data has been transferred correctly.
    * Use checksums or other methods to ensure data integrity.
8.  **Export the ZFS Pool:**
    * Once the data recovery is complete, export the ZFS pool using the command `zpool export <pool_name>`.
9.  **Power Down the Recovery Environment:**
    * Power down the recovery environment.
    * Disconnect the 4TB drives.

**Important Notes:**

* **Encryption Keys:** If the pool is encrypted, having the encryption keys is essential for data recovery.
* **Hardware Compatibility:** Ensure the recovery environment has compatible hardware to connect the 4TB drives.
* **ZFS Version Compatibility:** If possible, use a recovery environment with a ZFS version compatible with the original TrueNAS SCALE installation.
* **Data Integrity:** Prioritize data integrity during the recovery process.
* **Backups:** Regular backups are the most reliable method for data recovery.
* **Testing:** Test this recovery procedure on a regular basis.


# TrueNAS SCALE System and Data Recovery Procedure

This document outlines the procedures for recovering both the TrueNAS SCALE system configuration and the data stored on ZFS pools in the event of a system failure.

## Part 1: Backing Up the TrueNAS SCALE System Configuration

It is crucial to regularly back up the TrueNAS SCALE system configuration to facilitate a quicker recovery in case of system instability or failure.

1.  **Log in to the TrueNAS SCALE Web Interface.**
2.  Navigate to **System** in the left-hand menu.
3.  Click on **General**.
4.  Scroll down to the **Manage Configuration** section.
5.  **Download Configuration:**
    * Click the **Download File** button.
    * A `.tar.gz` archive containing your system configuration will be downloaded. Store this file securely in a separate location (e.g., external drive, cloud storage).
    * **Export Password Secret Seed (if applicable):** If your system uses encryption with a passphrase, it is vital to also export the Password Secret Seed. This is often found in a separate option within the **Manage Configuration** section or during the initial setup. Store this seed securely alongside your configuration file.
6.  **Upload Configuration (Restoration):**
    * After a fresh installation of TrueNAS SCALE, or in a recovery scenario, navigate to **System > General > Manage Configuration**.
    * Click the **Upload File** button.
    * Browse to and select the previously downloaded `.tar.gz` configuration file.
    * Click **Upload**. The system will prompt you to reboot after the configuration is uploaded.
    * **Important:** If your storage pools are encrypted with a passphrase, you will likely be prompted to enter the passphrase or upload the Password Secret Seed during the pool import process (see Part 2).

## Part 2: Recovering Data from a ZFS Pool (Example: 4 x 4TB RAIDZ2)

This procedure outlines how to recover data from a ZFS RAIDZ2 pool consisting of 4 x 4TB hard drives. This assumes the underlying disks are still functional and the ZFS pool metadata is intact.

**Scenario:**

* TrueNAS SCALE system fails to boot or becomes inaccessible.
* Data needs to be recovered from the 4 x 4TB hard drives configured in a ZFS RAIDZ2 pool.

**Recovery Steps (Using TrueNAS SCALE as the Recovery Environment):**

1.  **Prepare a Recovery TrueNAS SCALE System:**
    * Perform a fresh installation of TrueNAS SCALE on a separate boot device (e.g., new SSD, USB drive).
    * Ensure this recovery TrueNAS SCALE system has enough SATA ports to connect all 4TB drives.
2.  **Connect the Drives:**
    * Power down the recovery TrueNAS SCALE system.
    * Connect the 4 x 4TB drives to the SATA ports. Maintain the original drive order if possible, although ZFS is generally resilient to minor order changes.
    * Power on the recovery TrueNAS SCALE system.
3.  **Import the ZFS Pool:**
    * Log in to the TrueNAS SCALE Web Interface of the recovery system.
    * Navigate to **Storage** in the left-hand menu.
    * Click **Import Pool**.
    * In the **Import a Pool** window:
        * **Select Pool:** The system should automatically detect the available ZFS pool(s) from the connected drives. Select the pool corresponding to your 4TB drives. The pool name will be listed.
        * **Import Options:** Leave the default options selected unless you have specific requirements.
        * **Encryption:** If your pool was encrypted:
            * You will be prompted to **Enter Passphrase** or **Upload Key File**. Provide the correct passphrase or upload the key file you saved.
            * Alternatively, if you backed up your **Password Secret Seed** during the configuration backup, TrueNAS might use this to attempt automatic decryption.
        * Click **Import**.
4.  **Verify Pool and Data Access:**
    * Once the pool is imported, it will appear under the **Storage > Pools** section. Check its status to ensure it is healthy.
    * Navigate to **Shares** (SMB, NFS, etc.) and reconfigure or create new shares pointing to the imported datasets within the pool.
    * Access the data from a client machine to verify that the files are accessible.
5.  **Copy the Data (If Necessary):**
    * If you need to move the data to a new storage location, you can use the TrueNAS SCALE interface (e.g., creating a temporary share and copying files) or command-line tools (`cp`, `rsync`) within the TrueNAS SCALE system.
6.  **Export the ZFS Pool (If Releasing the Drives):**
    * If you need to disconnect the drives from the recovery system, navigate to **Storage > Pools**.
    * Select the imported pool.
    * Click the **three dots** (ellipsis) next to the pool name.
    * Select **Export/Disconnect**. Follow the prompts to safely export the pool.
7.  **Power Down the Recovery TrueNAS SCALE System:**
    * Power down the recovery TrueNAS SCALE system and disconnect the drives.

**Important Notes:**

* **Encryption Keys/Passphrase/Secret Seed:** Having the correct encryption keys, passphrase, or Secret Seed is absolutely critical for recovering encrypted ZFS pools.
* **Hardware Compatibility:** Ensure the recovery TrueNAS SCALE system has compatible hardware to connect the drives.
* **ZFS Version Compatibility:** Using a recovery TrueNAS SCALE system with a ZFS version compatible with the original installation is recommended.
* **Data Integrity:** After importing the pool, it's advisable to run a ZFS scrub to check for any data integrity issues: **Storage > Pools > Select Pool > Three Dots > Scrub**.
* **Regular Backups:** Regular backups to a separate location remain the most reliable method for data recovery.
* **Testing:** Regularly test both the configuration backup and the pool import procedures in a non-production environment if possible.