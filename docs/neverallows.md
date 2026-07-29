# Neverallow Assertions

`neverallow` rules are the platform's primary mechanism to guarantee OEMs and vendors adhere to the
Android security model.

## Evaluation & Exemptions
*   **Do Not Delete:** Never completely remove a `neverallow` restriction just to quickly fix a
    build break.
*   **Narrowing:** If a legitimate platform feature requires an exception, add a less-tight
    `neverallow`. Use attributes to exempt a specific domain or exclude a specific type, leaving the
    broader boundary intact.
*   **Treble Violators:** Pay special attention to Treble violator attributes (e.g.,
    `data_between_core_and_vendor_violators`, `system_executes_vendor_violators`). Do not add these
    to bypass Treble boundaries; fix the underlying IPC mechanism instead.

## Placement
Any `neverallow` assertion should be placed at the **bottom** of the `.te` file. This keeps the
active `allow` rules highly visible at the top of the file.

## CTS Verification
`neverallow` assertions are not just build-time checks; they are automatically translated into CTS
(Compatibility Test Suite) tests to ensure that all Android devices comply with the platform's
security requirements.

*   **Mechanism:** SELinux policy files are compiled into a policy conf file. CTS host-side tests
    (e.g., `SELinuxNeverallowRulesTest`) parse this policy conf file to extract the `neverallow`
    assertions. Each assertion then dynamically becomes a single CTS test case.
*   **Vendor Testing:** Additionally, `SELinuxNeverallowRulesTestVendor` tests vendor SEPolicy rules
    against a frozen set of `neverallow` assertions defined under
    `prebuilts/api/{ver}/{ver}_general_sepolicy.conf`.
*   **Exceptions:** Because of this translation mechanism, when adding an exception to an assertion,
    it is usually required to backport the relaxed neverallow assertion to the current CTS branch as
    well.
