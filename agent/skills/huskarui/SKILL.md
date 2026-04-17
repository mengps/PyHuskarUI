---
name: "HuskarUI"
description: "Queries HuskarUI metadata with Python and guides HuskarUI-first QML/C++ code. Invoke when choosing components, checking examples, or generating HuskarUI UI."
---

# HuskarUI

Use this skill whenever the agent needs HuskarUI component knowledge or must generate UI that should follow HuskarUI conventions. Treat Python query results as the primary source of truth. Read source files only for verification. `guide.metainfo.json` and `query_metainfo.py` are always located in `<SKILL_DIR>`.

## When To Use

Invoke this skill proactively when any of the following is true:

1. The agent needs to know which HuskarUI component matches a requested control, pattern, or interaction.
2. The agent needs examples or usage guidance for a HuskarUI component.
3. The user asks for HuskarUI-first QML code such as a page, dialog, toolbar, form, navigation area, or card.
4. The agent is unsure whether to use HuskarUI or native QtQuick for a visible control.
5. The agent needs to search the HuskarUI component set before proposing an implementation.

## Capabilities

1. **List**: Return all available component titles.
2. **Lookup**: Return component documentation and embedded examples for an exact component name.
3. **Search**: Find candidate components by keyword across titles and docs.
4. **Component Mapping**: Map generic UI requests to HuskarUI components before code generation.
5. **HuskarUI-first Guidance**: Prefer HuskarUI controls over native QtQuick when a suitable component exists.

## Critical Rules

These rules are always enforced. Follow them in this order.

### Metadata

- **Always use Python first.** Query metadata before answering from memory.
- **Never read the full `guide.metainfo.json` directly.** Use `query_metainfo.py`.
- **Use exact lookup for known component names.** Do not guess APIs or examples.
- **Use keyword search for generic UI needs.** Search by role such as `button`, `dialog`, `avatar`, `table`, `navigation`.

### Component Selection

- **Prefer HuskarUI for visible controls.** Buttons, inputs, avatars, dialogs, tables, navigation, and common widgets should map to HuskarUI first.
- **Use native QtQuick only when HuskarUI has no suitable component** or when the need is clearly low-level layout, animation, or primitives.
- **Do not mix HuskarUI and native controls for the same role without a clear reason.**
- **If no HuskarUI component fits, say so explicitly** before falling back to native QtQuick.

### Code Generation

- **Base generated code on metadata results, not assumptions.**
- **Use examples returned by Python as the primary usage reference.**
- **For generic UI requests, map each requested role to a HuskarUI component before writing code.**
- **Prefer composition from existing HuskarUI components over custom controls.**

## Query Workflow

1. Resolve the paths for `query_metainfo.py` and `guide.metainfo.json`.
2. Choose the query mode:
   - `list` for discovery.
   - Exact component name for lookup.
   - Keyword for generic UI requests.
3. Run the Python command.
4. Base the answer on the returned title, documentation, and examples.
5. For UI generation, choose HuskarUI building blocks from the results before writing code.
6. If nothing useful is found, state that clearly and use the minimum native QtQuick needed.

## Verification Workflow

Read source files only when one of these is true:

1. The Python output is ambiguous.
2. The examples do not cover the requested usage.
3. The user asks for implementation-level behavior.
4. The metadata appears stale or incomplete.

When verification is needed:

1. Identify the component through Python first.
2. Read only the relevant source file or section.
3. Confirm the specific behavior being discussed.
4. Answer from the verified implementation, not from guesswork.

## Coding Guidelines

### QML

- **Import order:** `QtQuick` -> `QtQuick.*` -> `HuskarUI.Basic`.
- **Use `QtQuick.Templates as T`** when inheriting from templates.
- **Names:** Components in PascalCase; properties, functions, and ids in camelCase.
- **Private members:** Prefix with double underscore.
- **Indentation:** 4 spaces.
- **Structure:** `id`, properties, implicit size, visual properties, child objects.
- **Prefer `let` and `const`** over `var`.
- **Use strict equality** with `===` and `!==`.
- **Avoid binding loops.**
- **Use `Loader` for conditional heavy subtrees** when appropriate.

## Response Policy

When using this skill in an answer:

1. Start from Python query results.
2. Name the HuskarUI component(s) that best match the request.
3. Summarize the relevant documentation and examples.
4. Generate HuskarUI-first code when the user asks for implementation.
5. Explicitly mention when the answer required source verification.
6. Explicitly mention when no suitable HuskarUI component was found.

## Quick Reference

```powershell
# List all components
python <SKILL_DIR>/query_metainfo.py <SKILL_DIR>/guide.metainfo.json list

# Exact lookup
python <SKILL_DIR>/query_metainfo.py <SKILL_DIR>/guide.metainfo.json HusAvatar --exact

# Search by keyword or UI role
python <SKILL_DIR>/query_metainfo.py <SKILL_DIR>/guide.metainfo.json button
python <SKILL_DIR>/query_metainfo.py <SKILL_DIR>/guide.metainfo.json navigation
python <SKILL_DIR>/query_metainfo.py <SKILL_DIR>/guide.metainfo.json table
```

## Current Skill Context

The skill always works from these two files:

```text
<SKILL_DIR>/query_metainfo.py
<SKILL_DIR>/guide.metainfo.json
```

The Python helper currently supports:

- Listing all component titles.
- Exact component lookup by title.
- Keyword search across component titles and docs.
- Returning documentation and embedded QML examples.

## Detailed References

- `query_metainfo.py` - metadata query entrypoint
- `guide.metainfo.json` - metadata database, accessed through Python only
- Repository source files - selective verification only when Python output is insufficient
