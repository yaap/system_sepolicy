# Contexts Files Mapping

When a new type is created, it must be associated with the appropriate object in a contexts file.

*   **`file_contexts`:** Regular files and directories (supports regex). Requires rebuilding the
    filesystem image or running `restorecon` to apply.
*   **`genfs_contexts`:** Virtual filesystems like `/proc`, `/sys`, or `vfat` that do not support
    extended attributes. (Does *not* support regex).
*   **`property_contexts`:** Maps Android system property prefixes (e.g., `ro.`, `persist.`,
    `vendor.`) to SELinux types.
*   **`service_contexts`:** Maps Android Binder service names to SELinux types (read by
    `servicemanager`).
*   **`seapp_contexts`:** Maps app processes and `/data/data` directories to domains, usually based
    on `seinfo` tags.
*   **`mac_permissions.xml`:** Assigns `seinfo` tags to apps based on their cryptographic
    signatures.
*   **`keystore2_key_contexts`:** Assigns labels to Keystore 2 namespaces, enforced by the
    `keystore2` daemon.
