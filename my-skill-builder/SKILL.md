---
name: my-skill-builder
description: Automatically generates Agent Skills with proper structure, frontmatter, and documentation. Use when user asks to create a skill, make a skill, build a skill, or needs to package instructions as a skill.
---

# My Skill Builder

> Automatically generates Agent Skills following the official specification

## Quick Start

1. Choose a template type (Minimal / Standard / Advanced)
2. Validate your skill name
3. Write your SKILL.md
4. Validate with `skills-ref validate ./your-skill`

## Directory Index

| Resource | Description |
|----------|-------------|
| `references/specification.md` | Complete format rules, field constraints, validation |
| `references/structure.md` | Directory structures and file organization |
| `references/templates.md` | SKILL.md templates (simple, complex, API) |
| `references/sources.md` | Original documentation sources and references |
| `QUICKREF.md` | Single-page quick reference card |
| `examples/minimal-example.md` | Minimal working example |
| `examples/standard-example/` | Full skill with references |

## Creating a Skill

### 1. Choose Template Type
- **Minimal**: Single SKILL.md, no dependencies
- **Standard**: SKILL.md + references/ + assets/
- **Advanced**: Includes extensive references/, assets/, and optional subdirectories

### 2. Validate Name
- 1-64 characters, lowercase letters, numbers, hyphens only
- Must not start/end with hyphen
- No consecutive hyphens
- Must match directory name

**Valid**: `my-skill`, `pdf-tool-2`, `data-analyzer`
**Invalid**: `My-Skill`, `-skill`, `skill--name`, `tool_v2`

### 3. Write Description
Max 1024 characters. Must describe:
- What the skill does
- When to use it (include keywords)

**Good**:
```
Extracts text and tables from PDFs, fills forms, merges documents.
Use when user mentions PDF, forms, document extraction, or PDF manipulation.
```

**Poor**:
```
Helps with PDFs.
```

### 4. Build SKILL.md

**Minimal structure:**
```yaml
---
name: your-skill
description: Your skill description here.
---

# Skill Title

## When to use
Use when...

## Instructions
1. Step one
2. Step two
```

**Full structure options:** See `references/templates.md`

### 5. Validate

```bash
# Validate skill structure
skills-ref validate ./your-skill

# Or manually check:
# - SKILL.md exists
# - Frontmatter is valid YAML
# - name matches directory
# - description is 1-1024 chars
```

## Best Practices

### Progressive Disclosure
Keep context efficient by structuring content:
1. **Metadata** (~100 tokens): name + description loaded at startup
2. **Instructions** (<5000 tokens): SKILL.md body loaded on activation
3. **Resources** (as needed): references/ loaded on demand

### File Organization
- Keep SKILL.md under 500 lines
- Move detailed info to `references/`
- Use relative paths: `See [reference](references/guide.md)`
- Keep reference files focused

### When to Split Content
Move to `references/` when:
- SKILL.md exceeds 500 lines
- Content is reference material, not instructions
- Content is only needed for specific subtasks
- Content is domain-specific details

Keep in SKILL.md:
- Activation triggers (when to use)
- Core workflow
- Common patterns
- Quick reference table

## Common Tasks

### Create Simple Task Skill
1. Copy `examples/minimal-example.md`
2. Edit name, description, instructions
3. Validate

### Create Domain Expert Skill
1. Copy `references/templates.md` Template 2
2. Fill in domain details
3. Create `references/` subdirectory
4. Add domain-specific guides

### Create API Integration Skill
1. Copy `references/templates.md` Template 3
2. Document API operations in SKILL.md
3. Add API reference in `references/api.md`
4. Include error handling table

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Name validation fails | Check: lowercase, no underscores, doesn't start/end with `-` |
| Description too long | Keep under 1024 chars, move details to body |
| Agent not activating | Add specific keywords to description |
| Context overflow | Move detailed info to `references/`, keep SKILL.md lean |

## Resources

### In This Skill
- All reference documentation in `references/`
- Quick reference: `QUICKREF.md`
- Working examples in `examples/`

### External Documentation
- Official spec: https://agentskills.io/specification
- Best practices: https://agentskills.io/what-are-skills
- Integration guide: https://agentskills.io/integrate-skills
- Source references: `references/sources.md`
- Validation tool: `skills-ref` CLI (from skills-ref library)
