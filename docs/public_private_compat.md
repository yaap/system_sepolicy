# Public and Private Separation

## Core Placement Rules
*   **Private by Default:** All new types and attributes MUST be placed in `private/` unless vendor
    access is strictly required.
*   **Rule Restriction:** All `allow`, `neverallow`, and `dontaudit` rules MUST be in `private/`.
    The `public/` directory should only contain type/attribute definitions and necessary
    `typeattribute` statements.

## API Stability & Trunk Stable (The "N" Logic)
When a new type is intended for vendor use at a specific Board API Level (N) (e.g., `202604`):
*   **Dual-Definition:** The type must be defined in BOTH directories to ensure platform private
    policy can use it immediately while respecting board API freezing.
*   In `public/`: Guard with `starting_at_board_api(N, \` ... ')`
*   In `private/`: Guard the EXACT SAME definition with `until_board_api(N, \` ... ')`
*   **M4 Syntax:** Always use exactly one backtick (\`) to open and one single quote-parenthesis (')
    to close. No trailing spaces before the closing quote.

## Compatibility Mapping (The "N-1" Logic)
Public types introduced for API N must be mapped in the N-1 compat files:
*   **`{N-1}.ignore.cil`:** Use for entirely new types with no previous equivalent.
*   **`{N-1}.cil`:** Use if the new type is a specific relabeling of a previously generic label (to
    ensure older vendors maintain access).

## system_ext and product Partitions
`system_ext` and `product` partitions can export public types to the vendor partition. Partners are
responsible for maintaining base mapping files in `system_ext/etc/selinux/mapping/<ver>.cil` and
`product/etc/selinux/mapping/<ver>.cil` if these partitions are updated independently of the vendor
partition.
