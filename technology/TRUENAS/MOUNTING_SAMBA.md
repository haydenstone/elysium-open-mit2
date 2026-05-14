# MOUNTING A SAMBA SHARE ON TRUENAS SCALE VIA COMMAND LINE

This guide explains how to manually mount a Samba (SMB/CIFS) share to a local directory on your TrueNAS SCALE system using the `mount -t cifs` command. This can be useful for temporary access, scripting, or specific use cases.

**Prerequisites:**

* You have a Samba share available on another server or device on your network.
* You know the network path to the Samba share (e.g., `//server_ip_or_hostname/share_name`).
* You have the necessary username and password (if required) to access the Samba share.
* You have installed the `cifs-utils` package on your TrueNAS SCALE system. TrueNAS SCALE usually has this installed by default, but if not, you can install it via the command line:

    ```bash
    sudo apt update
    sudo apt install cifs-utils
    ```

* You have created a local directory on your TrueNAS SCALE system where you want to mount the Samba share (e.g., `/mnt/smb_mount`).

**Steps:**

1.  **Open the TrueNAS SCALE Shell:**
    * Log in to your TrueNAS SCALE server via SSH or open the Shell from the web interface.

2.  **Create a Local Mount Point (if it doesn't exist):**
    * Choose a directory where you want to mount the Samba share. If the directory doesn't exist, create it using the `mkdir` command:

    ```bash
    sudo mkdir -p /mnt/smb_mount
    ```

    * Replace `/mnt/smb_mount` with your desired local mount point. The `-p` flag creates parent directories if they don't exist.

3.  **Mount the Samba Share using `mount -t cifs`:**
    * Use the following command to mount the Samba share:

    ```bash
    sudo mount -t cifs "//server_ip_or_hostname/share_name" /mnt/smb_mount -o username=your_username,password=your_password
    ```

    * **Replace the placeholders with your actual information:**
        * `"//server_ip_or_hostname/share_name"`: The network path to your Samba share. Replace `server_ip_or_hostname` with the IP address or hostname of the server hosting the share, and `share_name` with the name of the shared folder.
        * `/mnt/smb_mount`: The local directory on your TrueNAS SCALE system where you want to mount the share.
        * `your_username`: The username you use to access the Samba share.
        * `your_password`: The password for the specified username.

    * **Handling Spaces in Share Names or Paths:** If your share name or the local mount point path contains spaces, you might need to enclose them in quotes.

    * **Mounting Without Password Prompt (Not Recommended for Security):** If the Samba share allows guest access or you've configured other authentication methods, you might be able to mount without specifying a password directly in the command:

    ```bash
    sudo mount -t cifs "//server_ip_or_hostname/share_name" /mnt/smb_mount -o guest
    ```

    * **Specifying User ID and Group ID:** To control the ownership and permissions of the mounted files on your local system, you can use the `uid` and `gid` options:

    ```bash
    sudo mount -t cifs "//server_ip_or_hostname/share_name" /mnt/smb_mount -o username=your_username,password=your_password,uid=$(id -u),gid=$(id -g)
    ```

    * This will set the owner and group of the mounted files to the current user's ID and group ID.

4.  **Verify the Mount:**
    * After running the `mount` command, you can verify if the Samba share has been successfully mounted by using the `df -h` command or by listing the contents of the local mount point directory:

    ```bash
    df -h | grep /mnt/smb_mount
    ls /mnt/smb_mount
    ```

    * If the mount was successful, `df -h` will show the mounted Samba share, and `ls` will display the files and folders within the share.

**Unmounting the Samba Share:**

When you no longer need access to the Samba share, you can unmount it using the `umount` command:

```bash
sudo umount /mnt/smb_mount