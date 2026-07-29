# Macros and Attributes

## Using Attributes
Attributes are heavily utilized by the build system for Treble compatibility.
*   **Versioning:** At compile time, platform public types used in vendor policy are automatically
    translated into versioned attributes (e.g., `type_202604`).
*   **Grouping:** Use attributes when multiple types share the same property (e.g., `appdomain`). Do
    not create an `is_an_app()` macro for every type.
*   **Service Access Control:** Use predefined attributes (e.g., `app_api_service`,
    `vendor_service`) to grant access to services instead of granting permissions to concrete types.
    This centralizes access control and makes it easier to audit.
*   **Public Attributes Caution:** Permissions granted to a public attribute automatically apply to
    all types mapped to it. Audit public attribute modifications heavily.

## Using Macros
*   **Shorthand Permissions:** Always use standard `*_file_perms` macros (e.g., `rw_file_perms`,
    `r_file_perms`) instead of manually listing raw permissions. This prevents missing necessary
    secondary permissions like `open` or `getattr`.
*   **Custom Macros:** No new custom M4 macro should be added unless highly compelling. Macros hide
    the effective access being granted.
*   **Explicit Arguments:** When defining a macro, only accept the *complete* type as an argument.
    Do not use partial string manipulation (e.g., `hal_attribute(foo)` expanding to `hal_foo`), as
    it breaks code searchability.
