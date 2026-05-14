# MOUNTING_NFS.md - Mounting NFS Shares in Linux with Aliases

This document explains how to manually mount NFS (Network File System) shares on a Linux system (including TrueNAS SCALE's underlying Linux environment) and how to create convenient aliases for mounting and unmounting these shares.

## Prerequisites

* You have an NFS server configured and sharing directories on your network.
* You know the NFS server's IP address or hostname and the exported share path (e.g., `192.168.1.100:/export/data`).
* The `nfs-common` package is installed on your Linux system. You can install it using:

    ```bash
    sudo apt update -y && sudo apt install nfs-common -y
    ```

* You have created a local mount point directory on your Linux system where you want to access the NFS share (e.g., `/mnt/nfs_share`).

## Steps to Mount an NFS Share Manually

1.  **Open a Terminal:** Access the command line on your Linux system.

2.  **Create a Local Mount Point (if it doesn't exist):**

    * Choose a directory where you want to mount the NFS share. If it doesn't exist, create it using `mkdir`:

        ```bash
        sudo mkdir -p /mnt/nfs_share
        ```

        * Replace `/mnt/nfs_share` with your desired local mount point. The `-p` flag creates parent directories if needed.

3.  **Mount the NFS Share using the `mount` command:**

    * Use the following command to mount the NFS share:

        ```bash
        sudo mount -t nfs <nfs_server_ip_or_hostname>:<exported_path> /mnt/nfs_share
        ```

        * **Replace the placeholders with your actual information:**
            * `<nfs_server_ip_or_hostname>`: The IP address or hostname of the NFS server.
            * `<exported_path>`: The path to the shared directory on the NFS server (e.g., `/export/data`).
            * `/mnt/nfs_share`: The local mount point directory on your Linux system.

    * **Example:**

        ```bash
        sudo mount -t nfs 192.168.1.100:/shared_files /mnt/my_nfs_data
        ```

4.  **Verify the Mount:**

    * After running the `mount` command, verify the mount using `df -h` or by listing the contents of the mount point:

        ```bash
        df -h | grep /mnt/nfs_share
        ls /mnt/nfs_share
        ```

        * If successful, `df -h` will show the mounted NFS share, and `ls` will display its contents.

## Creating Aliases for Mount and Unmount

To simplify the process of mounting and unmounting specific NFS shares, you can create aliases in your shell configuration file (e.g., `.bashrc` or `.zshrc`).

1.  **Open your Shell Configuration File:**

    * Use a text editor to open your shell configuration file. For Bash, this is typically `~/.bashrc`. For Zsh, it's `~/.zshrc`.

        ```bash
        nano ~/.bashrc  # For Bash
        nano ~/.zshrc  # For Zsh
        ```

2.  **Add the Mount Alias:**

    * Add a line to define an alias for mounting your NFS share. Choose a descriptive name for your alias:

        ```bash
        alias mntnfs='sudo mount -t nfs <nfs_server_ip_or_hostname>:<exported_path> /mnt/nfs_share'
        ```

        * **Replace the placeholders** with your actual NFS server address, exported path, and local mount point.

    * **Example:**

        ```bash
        alias mntdata='sudo mount -t nfs 192.168.1.100:/shared_files /mnt/my_nfs_data'
        ```

3.  **Add the Unmount Alias:**

    * Add a line to define an alias for unmounting the same NFS share:

        ```bash
        alias umntnfs='sudo umount /mnt/nfs_share'
        ```

        * **Replace the placeholder** with your actual local mount point.

    * **Example:**

        ```bash
        alias umntdata='sudo umount /mnt/my_nfs_data'
        ```

4.  **Save and Close the File:**

    * Save the changes you made to your shell configuration file and close the editor.

5.  **Apply the Changes to Your Current Session:**

    * To use the newly created aliases in your current terminal session, you need to source your shell configuration file:

        ```bash
        source ~/.bashrc  # For Bash
        source ~/.zshrc  # For Zsh
        ```

## Using the Aliases

Now you can easily mount and unmount your NFS share using the aliases you created:

* **To mount:**

    ```bash
    mntnfs  # Or your chosen mount alias (e.g., mntdata)
    ```

* **To unmount:**

    ```bash
    umntnfs # Or your chosen unmount alias (e.g., umntdata)
    ```

## Important Considerations

* **Permissions:** File permissions on the mounted NFS share are managed by the NFS server's configuration.
* **Network Connectivity:** Ensure your Linux system has reliable network connectivity to the NFS server.
* **Persistent Mounts:** For NFS shares that you want to be automatically mounted at boot, you should configure the `/etc/fstab` file instead of relying solely on manual mounts or aliases.
* **Security:** Ensure your NFS server is properly configured with appropriate export options and security measures.
* **Alias Scope:** Aliases are typically user-specific and defined within the user's shell configuration file.