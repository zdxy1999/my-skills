---
name: alibaba-java-code-guidelines
description: Alibaba Java code standards and best practices for static analysis, bug detection, and code quality. Use when writing, reviewing, or refactoring Java code, especially for enterprise applications. Covers concurrency, collections, date/time handling, exception handling, and production incident patterns.
---

# Alibaba Java Code Guidelines

This skill encapsulates Alibaba's Java coding standards based on Google Error-Prone static analysis. The guidelines are battle-tested from production incidents and enterprise Java development.

## When to Use

Activate this skill when:
- Writing or reviewing Java code
- Refactoring legacy Java applications
- Setting up code quality gates for Java projects
- Conducting static analysis on Java codebases
- Implementing concurrency, collections, or date/time operations

## Rule Categories

### Severity Levels

**Blocker** - Must fix. High probability bugs likely to cause production failures.
- Threading issues (locking on boxed primitives, unsafe thread pools)
- Collection misuse (type incompatibility, concurrent modification)
- Date/time pitfalls (YYYY vs yyyy, week year confusion)
- Equality comparisons on boxed primitives
- Resource leaks (double-brace initialization)

**Major** - Should fix. Affects performance, robustness, or readability.
- Empty catch blocks without documentation
- Missing @Override annotations
- Improper exception handling
- hashCode/equals contract violations
- ThreadLocal usage patterns

**Info** - Consider fixing. Better alternatives exist.
- Using legacy Date instead of java.time API

### Key Patterns

**Concurrency**
- Use `ThreadPoolExecutor` instead of `Executors` factory methods (prevents unbounded thread creation)
- Never lock on boxed primitives (cached values cause cross-thread interference)
- Always retrieve JDBC connections immediately after borrowing

**Collections & Arrays**
- Use `Arrays.asList()` carefully with primitive arrays (returns `List<int[]>` not `List<Integer>`)
- Don't modify collections during enhanced for loops
- Avoid double-brace initialization (causes memory leaks via anonymous classes)

**Date & Time**
- Use lowercase `yyyy` for calendar year, uppercase `YYYY` only for week year
- Prefer `java.time` API over `Date` and `Calendar`
- Be aware of timezone defaults in `LocalDateTime` operations

**Equality & Comparison**
- Compare boxed primitives with `Objects.equals()`, not `==`
- Float/double equality checks require epsilon comparison
- Optional should not be compared with `==`

**Exception Handling**
- Never use empty catch blocks without explanatory comments
- Don't catch `Throwable` or `Exception` broadly
- Always document why exceptions are intentionally ignored

## Reference Structure

The detailed rules are organized in `JavaCodeGuideline/bugpattern/`:
- `blocker/` - Critical bugs requiring immediate fixes
- `major/` - Important quality and performance issues
- `info/` - Modernization and improvement suggestions

Each rule file contains:
- Problem description
- Counter-example (what not to do)
- Correct example (what to do instead)

## Integration Notes

These guidelines are designed for:
- Error-Prone static analysis integration
- Maven build-time checking
- CI/CD quality gates
- IDE live coding feedback (IntelliJ/Eclipse style files included)

## Production Lessons

Many rules originate from real production incidents (marked as "业务军规"), particularly around:
- Thread pool configuration causing resource exhaustion
- Date formatting bugs (week year vs calendar year)
- BigDecimal construction from float literals
- Jedis connection pool misusage
