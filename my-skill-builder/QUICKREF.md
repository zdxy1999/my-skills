# Skill Creator - Quick Reference

## Frontmatter Template

```yaml
---
name: skill-name
description: What it does and when to use it (max 1024 chars).
license: MIT           # Optional
metadata:              # Optional
  version: "1.0"
  author: name
---
```

## Name Rules
- Lowercase letters, numbers, hyphens only
- 1-64 characters
- No start/end hyphen
- No consecutive hyphens

## Description Format
```
[What it does]. Use when [user mentions X, Y, or Z].
```

## Directory Structure

```
skill-name/
├── SKILL.md          # Required
├── references/        # Optional: detailed docs
├── scripts/          # Optional: executable code
└── assets/           # Optional: templates, data
```

## Content Guidelines

| Component | Token Budget | When to Use |
|-----------|--------------|-------------|
| Metadata | ~100 | Always (name + description) |
| Instructions | <5000 | Core workflow in SKILL.md |
| Resources | As needed | references/ for details |

## Validation Checklist

- [ ] SKILL.md exists
- [ ] Frontmatter has name + description
- [ ] name matches directory name
- [ ] name follows rules (lowercase, no underscores)
- [ ] description is 1-1024 chars
- [ ] description includes keywords
- [ ] SKILL.md under 500 lines (recommended)
- [ ] Relative paths used for references

## Quick Commands

```bash
# Validate
skills-ref validate ./skill-name

# Generate prompt XML
skills-ref to-prompt ./skill-name

# Test structure
find ./skill-name -name "SKILL.md"
```
