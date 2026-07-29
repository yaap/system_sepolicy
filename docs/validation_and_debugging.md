# Validation & Debugging

## Analyzing Denials (audit2allow)
**Never blindly copy `audit2allow` output into policy.** It suggests rules to make the denial go
away, not to make the system secure.
*   **Generic Labels:** If a denial shows `tcontext=u:object_r:device:s0` (or `tmpfs`,
    `system_data_file`), do not write an `allow` rule for `device`. The correct fix is to label the
    specific file or node in `file_contexts`.
*   **dac_override:** If a `dac_override` denial occurs, do NOT grant the capability. The proper
    solution is to fix the underlying UNIX permissions (user/group/world) of the file or process.

## Permissive vs. Enforcing
*   Run in permissive mode (`androidboot.selinux=permissive`) only during early device bring-up to
    gather a comprehensive list of denials.
*   Switch back to enforcing mode as early as possible to prevent permissive mode from masking
    subsequent denials.

## Capturing Call Chains (simpleperf)
If `dmesg` logs are insufficient to locate the root cause of an AVC denial, capture the
kernel/userspace call chain using `simpleperf` (requires Linux >= 5.10):
```shell
adb shell -t "cd /data/local/tmp && su root simpleperf record -a -g -e avc:selinux_audited"
# Trigger the denial, stop the record, then:
adb shell -t "cd /data/local/tmp && su root simpleperf report -g --full-callgraph"
```
