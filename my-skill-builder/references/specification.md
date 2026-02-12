# Agent Skills Specification

## Directory Structure

```
skill-name/
├── SKILL.md          # Required
├── scripts/          # Optional
├── references/       # Optional
└── assets/          # Optional
```

## Frontmatter Fields

| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | Yes | Max 64 chars. Lowercase letters, numbers, hyphens only. Must not start/end with hyphen. |
| `description` | Yes | Max 1024 chars. Must describe what skill does and when to use it. |
| `license` | No | License name or reference to bundled file. |
| `compatibility` | No | Max 500 chars. Environment requirements (product, packages, network). |
| `metadata` | No | Key-value mapping for additional metadata. |
| `allowed-tools` | No | Space-delimited list of pre-approved tools (experimental). |

## Name Field Rules

- Must be 1-64 characters
- Only lowercase letters (a-z), numbers (0-9), and hyphens (-)
- Must not start or end with hyphen
- No consecutive hyphens (--)
- Must match parent directory name

**Valid**: `my-skill`, `pdf-processor`, `data-analyzer-2`
**Invalid**: `My-Skill`, `-skill`, `skill--name`, `PDF_Processor`

## Description Field Guidelines

- Must be 1-1024 characters
- Describe both what the skill does AND when to use it
- Include specific keywords for agent matching

**Good**:
```
Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs.
Use when working with PDF documents or when user mentions PDFs, forms, or document extraction.
```

**Poor**:
```
Helps with PDFs.
```

## Progressive Disclosure Strategy

1. **Metadata** (~100 tokens): Loaded at startup for all skills
2. **Instructions** (<5000 tokens recommended): Full SKILL.md loaded on activation
3. **Resources** (as needed): Reference files loaded on demand

## Best Practices

- Keep SKILL.md under 500 lines
- Move detailed reference material to references/
- Use relative paths from skill root for file references
- Keep reference chains shallow (one level deep preferred)
- Keep individual reference files focused
