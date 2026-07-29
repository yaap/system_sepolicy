# Feature Flagging

## Philosophy
Flags should be used in SEPolicy primarily when the policy change itself introduces a security risk
(e.g., removing a permission or tightening a domain). Adding `allow` rules rarely changes system
behavior on its own; the behavior change in the C++/Java code should be what is flag-gated.

## Implementation
To guard policy with build flags:
1.  **`Android.bp`:** Add the flag to the `flags` property of an `se_flags` module.
    `se_flags_collector` converts these to M4 macros.
2.  **M4 Macros:** Wrap the policy in the `.te` file using the helper macros:
*   `is_flag_enabled({flag}, \` ... ')`
*   `is_flag_disabled({flag}, \` ... ')`

**Note:** Follow the M4 syntax guardrails carefully (use single backtick and single quote).
