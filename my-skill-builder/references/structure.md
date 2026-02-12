# Skill Structure Templates

## Basic Skill (Minimal)

```
my-skill/
└── SKILL.md
```

## Standard Skill

```
my-skill/
├── SKILL.md
├── references/
│   └── REFERENCE.md
└── assets/
    └── template.txt
```

## Advanced Skill

```
my-skill/
├── SKILL.md
├── references/
│   ├── REFERENCE.md
│   ├── FORMS.md
│   └── domain-guide.md
└── assets/
    ├── template.json
    └── schema.yaml
```

## Directory Usage Guidelines

### references/
- Additional documentation loaded on demand
- `REFERENCE.md` - Technical reference
- `FORMS.md` - Form templates or data formats
- Domain-specific files (e.g., `finance.md`, `legal.md`)
- Keep files focused for efficient context loading

### assets/
- Static resources
- Templates (documents, configs)
- Images (diagrams, examples)
- Data files (lookup tables, schemas)

Note: Scripts are optional and environment-specific. This skill focuses on documentation-only structure for maximum portability across different agent environments.
