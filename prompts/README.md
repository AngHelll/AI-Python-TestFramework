# AI Context Directory

**Technical reference + Phase 1 prompt contracts for AI-assisted automation.**

---

## Purpose

This directory contains framework documentation and **versioned prompt contracts** so agents can:

- Understand framework architecture
- Emit structured Analyst / Planner outputs (`analysis.v1` / `plan.v1`)
- Generate code following framework patterns (after Gate 2)
- Debug issues with framework-specific knowledge

Evolution docs: `docs/ai-evolution/PHASE-1.md`.

---

## Directory Structure

```
prompts/
├── contracts/                  # Phase 1 — analysis.v1 / plan.v1
├── fragments/                  # Shared anti-patterns, gates, load order
├── library/                    # Prompt inventory by purpose
├── context/                    # Technical knowledge base (Python framework)
├── examples/
│   ├── few_shot_examples.json  # Legacy Q&A
│   └── approved/               # Human-curated few-shots (FS-01…)
├── system/                     # AI behavior instructions
└── README.md
```

---

## Content Files

### `context/FRAMEWORK.md`
**Complete technical reference**

Contains:
- Framework architecture and structure
- Configuration system
- Page Object Model implementation
- Test writing patterns (Pytest + Behave)
- Utility modules usage
- Command reference
- Adding new features

**When to use:** Primary reference for understanding framework capabilities

---

### `context/architecture.md`
**Deep architectural analysis**

Contains:
- Design patterns (POM, Factory, Decorator, etc.)
- Component interactions
- Data flow
- Class hierarchies
- Module dependencies

**When to use:** Understanding framework design decisions and patterns

---

### `context/bdd_with_behave.md`
**BDD implementation guide**

Contains:
- Behave framework integration
- Gherkin syntax
- Step definition patterns
- Feature organization
- BDD best practices

**When to use:** Working with BDD tests or Behave-specific features

---

### `context/best_practices.md`
**Coding standards and conventions**

Contains:
- Code style guidelines
- Naming conventions
- Test organization patterns
- Anti-patterns to avoid
- Performance optimizations

**When to use:** Ensuring code quality and consistency

---

### `context/troubleshooting.md`
**Problem-solving guide**

Contains:
- Common errors and solutions
- Debugging techniques
- Configuration issues
- Browser-specific problems
- CI/CD troubleshooting

**When to use:** Debugging issues or answering "why isn't X working?"

---

### `examples/few_shot_examples.json`
**Training examples**

Contains:
- Example user questions
- Expected AI responses
- Code generation examples
- Debugging scenarios

**When to use:** Understanding expected AI behavior patterns

---

### `system/system_prompt.md`
**AI behavior instructions**

Contains:
- AI assistant role definition
- Response guidelines
- Code generation rules
- Communication style

**When to use:** Defining how AI should interact with users

---

## How AI Should Use This Context

### Step 1: Load Relevant Context
When user asks about the framework, load appropriate files:
- General questions → `FRAMEWORK.md`
- Architecture questions → `architecture.md`
- BDD questions → `bdd_with_behave.md`
- Errors/issues → `troubleshooting.md`
- Code quality → `best_practices.md`

### Step 2: Apply Framework Patterns
Use loaded context to:
- Generate code matching framework style
- Follow established patterns
- Use correct imports and structure
- Apply best practices

### Step 3: Provide Directive Responses
Responses should be:
- **Authoritative:** "The framework uses X" (not "you could use X")
- **Specific:** Exact file paths, class names, commands
- **Complete:** Working code examples
- **Directive:** Clear instructions, not suggestions

---

## Documentation Tone

All files in `prompts/context/` use **directive, authoritative language**:

✅ **DO:**
- "The framework uses Behave for BDD"
- "Place page objects in `pages/` directory"
- "Execute tests with `pytest` command"
- "The BasePage class provides retry logic"

❌ **DON'T:**
- "We recently added BDD support"
- "You can write tests"
- "This might help"
- "Consider using page objects"

---

## Maintenance

### When Adding Features
1. Update `FRAMEWORK.md` with feature usage
2. Update `architecture.md` if pattern changes
3. Update `best_practices.md` with new conventions
4. Add examples to `few_shot_examples.json`

### When Fixing Issues
1. Document solution in `troubleshooting.md`
2. Update `best_practices.md` to prevent recurrence
3. Update `FRAMEWORK.md` if configuration changes

---

## Integration with IDE AI Tools

### GitHub Copilot
Load context files as reference to improve suggestions

### ChatGPT/Claude
Copy relevant context files into chat for framework-aware responses

### Cursor AI
Place cursor in relevant files for context-aware completions

---

## File Sizes

| File | Size | Load Time |
|------|------|-----------|
| FRAMEWORK.md | ~15KB | Instant |
| architecture.md | ~17KB | Instant |
| bdd_with_behave.md | ~13KB | Instant |
| best_practices.md | ~13KB | Instant |
| troubleshooting.md | ~12KB | Instant |
| **Total Context** | ~70KB | < 1 second |

All files load quickly and fit within typical AI context windows.

---

## Quick Reference

| User Question | Load This File |
|--------------|----------------|
| "How do I create a page object?" | `FRAMEWORK.md` |
| "Why use POM pattern?" | `architecture.md` |
| "How to write BDD scenarios?" | `bdd_with_behave.md` |
| "Element not found error" | `troubleshooting.md` |
| "Best way to organize tests?" | `best_practices.md` |
| "Generate login test" | `few_shot_examples.json` + `FRAMEWORK.md` |

---

**These files enable AI agents to work with the framework as effectively as experienced developers.**
