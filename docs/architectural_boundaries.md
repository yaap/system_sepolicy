# Architectural Boundaries

When writing or reviewing SEPolicy, syntactic correctness is only half the battle. The policy must
strictly adhere to Android's core architectural isolation boundaries.

## 1. The Treble Boundary (System vs. Vendor)
Strict separation between the framework (`system`) and vendor code (`vendor`) must be maintained.
* **No File-Based IPC:** Platform and vendor processes should never use on-disk files to
  communicate. This breaks the stable ABI. Do not use `data_between_core_and_vendor_violators`.
* **Execution Restrictions:** System domains (except `init` and `shell`) must never execute vendor
  binaries. Dependencies on vendor binaries must be placed behind HIDL/AIDL HALs.
* **Data Isolation:** Vendor code belongs in `/data/vendor`. The system must not use `/data/vendor`,
  and the vendor must not access core `/data` directories.

## 2. The IPC Boundary (Binder & Sockets)
* **Use Standard IPC:** Components should communicate via Binder, HwBinder, or highly scoped UNIX
  domain sockets.
* **System Server Isolation:** Minimize the number of domains that can communicate directly with
  `system_server`. Untrusted apps must have strictly defined and limited binder access. Use
  attributes like `app_api_service` to grant apps access to a new service instead of allowing access
  to the type directly.

## 3. The Global State Boundary (Sysprops)
System properties are global state and easily abused for dirty IPC.
* **Strict Scoping:** Avoid global read access. Properties must be scoped strictly (e.g.,
  `system_restricted_prop`, `vendor_restricted_prop`).
* **Write Restrictions:** `set_prop` access should be severely restricted, usually limited to `init`
  or the single specific daemon responsible for managing that state.

## 4. Device Nodes and HALs
* **No Raw Device Access:** Applications and system processes should rarely, if ever, be granted
  direct read/write access to raw device nodes in `/dev/`.
* **HAL Wrapping:** Hardware interaction must be wrapped in a HAL. Grant the hardware permissions to
  the `hal_server_domain` and provide the client access via the `hal_client_domain` macro.
