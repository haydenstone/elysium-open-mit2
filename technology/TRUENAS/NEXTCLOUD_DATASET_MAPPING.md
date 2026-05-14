# MAPPING EXISTING TRUENAS SCALE DATASETS TO NEXTCLOUD

[External Mappings](https://docs.nextcloud.com/server/20/admin_manual/configuration_files/external_storage/local.html)

This guide explains how to configure Nextcloud on TrueNAS SCALE to directly access data stored in your existing datasets, avoiding the need to migrate data.

**Prerequisites:**

* Nextcloud is successfully installed and running on your TrueNAS SCALE server.
* You have existing datasets on your TrueNAS SCALE pool that you want to access through Nextcloud (e.g., `/storage/backups`, `/storage/games`, `/storage/images`, `/storage/media`, `/storage/share`, `/storage/users`).
* You have administrator access to your TrueNAS SCALE web interface and potentially the Nextcloud admin account.

**Method: Using External Storage in Nextcloud**

Nextcloud provides a powerful "External Storage" feature that allows you to mount various storage backends, including local file systems, directly into your Nextcloud instance. This is the recommended way to access your existing TrueNAS SCALE datasets without moving the data.

**Steps:**

1.  **Access the Nextcloud Web Interface:**
    * Open your web browser and navigate to your Nextcloud URL (e.g., `nextcloud.domain`).
    * Log in with your Nextcloud administrator account.

2.  **Install the "External storage support" App (if not already installed):**
    * Click on your profile icon in the top right corner.
    * Go to **Apps**.
    * In the left sidebar, click on **All apps**.
    * Search for "External storage support".
    * If it's not installed, click **Install**.

3.  **Configure External Storage Mounts:**
    * Click on your profile icon again and go to **Settings**.
    * In the left sidebar, under the "Administration" section, click on **External storage**.
    * You will see a section to "Add storage". Use the dropdown menu labeled "**Add storage**" and select "**Local**".

4.  **Configure the Local Mount:**
    * **Folder name:** Enter a name that will appear in your Nextcloud files for this mounted dataset (e.g., "Backups", "Games", "Images", "Media", "Shared Files", "User Homes").
    * **Configuration \> Local:** In the "**Path**" field, enter the **absolute path** to your existing TrueNAS SCALE dataset on the server. For example:
        * `/mnt/your_pool_name/backups`
        * `/mnt/your_pool_name/games`
        * `/mnt/your_pool_name/images`
        * `/mnt/your_pool_name/media`
        * `/mnt/your_pool_name/share`
        * `/mnt/your_pool_name/users` (you might want to mount individual user sub-datasets here if needed)
        * **Important:** Replace `your_pool_name` with the actual name of your ZFS pool (e.g., `tank`).
    * **Applicable for:** You can specify which Nextcloud users or groups should have access to this external storage mount.
    * **Writable:** Check this box if you want users to be able to upload, modify, and delete files within this mounted dataset through Nextcloud. **Exercise caution with write permissions on existing datasets, especially shared ones.**
    * **Allow subfolders:** Enable this if you want Nextcloud to recognize the existing subfolders within your dataset.
    * **Available for:** (User/Groups selection)

5.  **Click the checkmark (✓) or "Save" button** to save the external storage configuration.

6.  **Repeat steps 3-5 for each of your existing TrueNAS SCALE datasets** that you want to access through Nextcloud.

**Accessing Your Data in Nextcloud:**

Once configured, the folders you named in the "Folder name" field will appear in the "Files" section of your Nextcloud interface. Users with the appropriate permissions will be able to browse and interact with the files and folders within these mounted datasets directly.

**Important Considerations:**

* **Permissions:** Ensure that the user running the Nextcloud service (usually `www-data`) has the necessary read and write permissions to the underlying TrueNAS SCALE datasets if you intend to allow modifications through Nextcloud. You might need to adjust the ACLs (Access Control Lists) on your datasets in the TrueNAS SCALE **Storage** settings.
* **Performance:** Accessing data on local storage through external mounts generally performs well.
* **Data Integrity:** Since Nextcloud is directly accessing your existing data, any changes made through Nextcloud will directly affect the files on your TrueNAS SCALE datasets.
* **Backups:** Your existing backup strategies for your TrueNAS SCALE datasets will continue to apply to the data accessed through Nextcloud. You should also consider backing up your Nextcloud configuration.

By using the "External Storage" feature, you can seamlessly integrate your existing TrueNAS SCALE storage with your Nextcloud instance without the need for data migration, making efficient use of your current setup."