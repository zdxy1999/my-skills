# SKILL.md Content Templates

## Template 1: Simple Task Skill

```yaml
---
name: skill-name
description: Brief description of what this skill does. Use when user mentions [keywords].
---

# Skill Title

## When to use
Use this skill when [specific conditions].

## Instructions
1. Step one
2. Step two
3. Step three

## Examples
- Input example
- Output example
```

## Template 2: Complex Domain Skill

```yaml
---
name: domain-expert
description: Performs specialized tasks in [domain]. Use when user needs [specific outcomes].
license: MIT
metadata:
  version: "1.0"
  author: your-name
---

# Domain Expert Skill

## Activation Triggers
Use this skill when user mentions:
- [Keyword 1]
- [Keyword 2]
- [Specific phrase]

## Quick Reference
| Task | Method |
|------|--------|
| Task A | See `references/method-a.md` |
| Task B | See `references/method-b.md` |

## Core Workflow
1. **Discovery**: [What to check first]
2. **Analysis**: [How to analyze]
3. **Execution**: [How to perform]
4. **Validation**: [How to verify]

## Common Patterns
### Pattern 1: [Name]
- When: [When to use]
- How: [Implementation steps]

### Pattern 2: [Name]
- When: [When to use]
- How: [Implementation steps]

## Edge Cases
- [Edge case 1]: [How to handle]
- [Edge case 2]: [How to handle]

## Resources
- Detailed methods: `references/methods.md`
- Data formats: `references/formats.md`
- Examples: `examples/`
```

## Template 3: API Integration Skill

```yaml
---
name: api-integrator
description: Integrates with [Service] API for [purpose]. Use when user needs [operations].
compatibility: Requires API key and network access
---

# [Service] API Integration

## Prerequisites
- API key stored in environment
- Network access to [service domain]
- Required package: `[package-name]`

## Setup Instructions
1. Verify credentials: Check API key validity
2. Install dependencies: `pip install [package-name]`
3. Test connection: Make test API call to health endpoint

## Operations
### List Resources
Use the API endpoint: `GET /api/[resource]`
Parameters:
- `filter`: Optional filter criteria
- `limit`: Max results (default: 50)

### Create Resource
Use the API endpoint: `POST /api/[resource]`
Request body: See `references/request-schemas.md`

### Update Resource
Use the API endpoint: `PUT /api/[resource]/{id}`
Request body: See `references/request-schemas.md`

## Error Handling
| Error | Cause | Solution |
|-------|-------|----------|
| 401 | Invalid credentials | Check API key in environment |
| 429 | Rate limit | Implement exponential backoff |
| 500 | Server error | Retry with exponential backoff |

## Reference
- API documentation: `references/api-spec.md`
- Request/response schemas: `references/schemas.md`
- Authentication guide: `references/auth.md`
```
