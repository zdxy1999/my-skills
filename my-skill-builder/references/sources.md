# Reference Sources

This skill is based on the official Agent Skills documentation from https://agentskills.io

## Official Documentation

| Page | URL | Key Content |
|------|-----|-------------|
| Home | https://agentskills.io/home | What are Agent Skills, benefits, adoption |
| What are Skills | https://agentskills.io/what-are-skills | Core concepts, progressive disclosure, structure |
| Specification | https://agentskills.io/specification | Complete format specification, validation rules |
| Integration Guide | https://agentskills.io/integrate-skills | How to add skills support to agents |

## Key Concepts

### Progressive Disclosure
Skills use progressive disclosure to manage context efficiently:
1. **Discovery**: Load only name and description (~100 tokens)
2. **Activation**: Read full SKILL.md instructions (<5000 tokens)
3. **Execution**: Load referenced files as needed

### File Structure
```
skill-name/
├── SKILL.md          # Required
├── scripts/          # Optional
├── references/       # Optional
└── assets/          # Optional
```

### Validation
Use the `skills-ref` CLI tool:
```bash
skills-ref validate ./my-skill
```

## External Resources

- [GitHub Repository](https://github.com/anthropics/agent-skills) - Reference implementation and examples
- [skills-ref library](https://github.com/anthropics/agent-skills) - Python utilities and CLI

## Version

Based on Agent Skills specification as of 2025. For the latest updates, visit https://agentskills.io
