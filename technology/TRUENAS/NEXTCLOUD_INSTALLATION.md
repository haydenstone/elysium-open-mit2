# Installing Nextcloud on TrueNAS SCALE

[Setting Up Your Own Cloud: A Guide to Nextcloud on TrueNAS SCALE](https://www.youtube.com/watch?v=8Cxg1mAYtL8)
[Nextcloud url keeps redirecting to Truenas server](https://help.nextcloud.com/t/nextcloud-url-keeps-redirecting-to-truenas-server/201851/5)

This guide outlines the steps to install Nextcloud on TrueNAS SCALE, allowing you to create your own personal cloud storage solution.

## Prerequisites

* A running TrueNAS SCALE instance.
* Basic understanding of TrueNAS SCALE datasets and applications.

## Creating Datasets for Nextcloud

Before installing Nextcloud, it's recommended to create dedicated datasets for its configuration and data. This helps in organizing your storage and makes backups and restores easier.

1.  **Access the TrueNAS SCALE web interface.**
2.  Go to **Datasets**.
3.  Select the "Apps" pool where you want to store your Nextcloud data.
4.  Click **Add Dataset**.
5.  Create two datasets:
    * **Nextcloud Configuration Dataset:**
        * **Name:** `Nextcloud_Database` (or any name you prefer)
        * **Preset:** Generic
        * Purpose: This dataset will store Nextcloud's configuration files.
6.  Select the "/" pool where you want to store your Nextcloud data.
    * **Nextcloud Data Dataset:**
        * **Name:** `Nextcloud_Data` (or any name you prefer)
        * **Preset:** Apps
        * **Owner:** www-data
        * **Group:** www-data
        * Apply recursive
        * Purpose: This dataset will store your Nextcloud files.
7.  Install Collabora
    * **Download and run docker container from app store**
        * **Defaults:** There are no special requirements
        * **Name:** Match the ip address of your TrueNAS server
        * **Resource Configuration:** Scale appropriately to your environment

## Installing Nextcloud

There are multiple ways to install Nextcloud on TrueNAS SCALE, including using the official app or Docker. Here's a general guide, and you should refer to the video "[Setting Up Your Own Cloud: A Guide to Nextcloud on TrueNAS SCALE](https://www.youtube.com/watch?v=8Cxg1mAYtL8)" by Lawrence Systems for a detailed walkthrough.

1.  **Access the TrueNAS SCALE web interface.**
2.  Go to **Apps**.
3.  Search for "Nextcloud".
4.  Click **Install**.
5.  Configure the Nextcloud app settings:
    * **Application Name:** Choose a name for your Nextcloud instance.
    * **Data Storage:** Select the `Nextcloud_Data` dataset you created earlier.
    * **Database Storage:** Select the `Nextcloud_Database` dataset you created earlier.
    * **Network Settings:** Configure the port and any necessary network settings.
    * **Admin Credentials:** Set the administrator username and password.
    * **Cron Jobs:** Enable cronjobs.
    * **URL Rewrites:** Enabled to 30027.
6.  Click **Install**.
7.  Wait for the app to deploy. This may take several minutes.
8.  Once the app is running, access the Nextcloud web interface using the configured URL.
9.  Log in with the administrator credentials you set during installation.

## Post-Installation

* Configure Nextcloud settings, such as storage quotas, user management, and external storage connections.
* Install any desired Nextcloud apps, such as Collabora Online for document editing.
* Set up backups for your Nextcloud data and configuration.

## Creating Datasets for Applications

When installing applications on TrueNAS SCALE, it is recommended to create separate datasets for each application. This practice offers several advantages:

* **Isolation:** Each application has its own dedicated storage space, preventing conflicts and ensuring that one application's issues don't affect others.
* **Security:** You can apply specific permissions and access controls to each application's dataset, enhancing security.
* **Management:** Managing backups, snapshots, and other storage-related tasks becomes easier when applications have their own datasets.
* **Resource Allocation:** You can set quotas and reservations for each dataset, ensuring that applications have the necessary storage resources.

To create a dataset for an application:

1.  Go to **Storage** \> **Pools**.
2.  Select the desired pool.
3.  Click **Add Dataset**.
4.  Enter a descriptive name for the dataset (e.g., `nextcloud_data`, `plex_config`).
5.  Choose a **Dataset Preset**. For most applications, the "Generic" preset is suitable. If you are creating a dataset for the application itself, choose "Apps".
6.  Configure any other desired settings, such as compression, encryption, or quotas.
7.  Click **Save**.

By following these guidelines, you can ensure a well-organized and efficient storage setup for your applications on TrueNAS SCALE.
