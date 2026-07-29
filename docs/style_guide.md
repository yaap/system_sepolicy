# Style Guide

Consistent formatting reduces review friction.

## Commenting
*   **The "What":** Provide a one-sentence comment at the top of a `.te` file explaining the
    domain's purpose.
*   **The "Why":** Comments above `allow` rules must explain *why* the rule is needed for a specific
    feature, not translate *what* the rule does. Reference issue/bug tracker numbers.

## Formatting
*   **Line Lengths:** If many types are referenced in a single rule, place one type per line.
*   **Braces:** Use braces `{ }` **only** when a set of multiple permissions or types is required.
    Do not use braces for a single item.
*   **Grouping:** Group related rules logically (e.g., block all network rules together, all file
    rules together).
