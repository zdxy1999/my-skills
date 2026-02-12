---
name: document-formatter
description: Formats and standardizes document structure. Use when user needs to clean up, reformat, or standardize documents, markdown files, or text files.
metadata:
  version: "1.0"
---

# Document Formatter

## When to use
- User needs to format markdown files
- User wants to standardize document structure
- User mentions cleaning up documents
- User needs consistent formatting across multiple files

## Quick Start
1. Identify the target file(s)
2. Determine the desired format (see `references/format-options.md`)
3. Apply formatting rules
4. Validate the output

## Common Operations

### Markdown Formatting
Use the standard markdown formatter:
```bash
scripts/format-markdown.md [file]
```

### Text Normalization
1. Convert line endings to LF
2. Trim trailing whitespace
3. Ensure single newline at EOF
4. Normalize multiple consecutive newlines

## Format Rules
See `references/format-rules.md` for detailed formatting specifications.

## Examples
- Before/After examples: `examples/`
- Test files: `examples/test-files/`
