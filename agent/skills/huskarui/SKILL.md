---
name: "HuskarUI"
description: "Use Python to query HuskarUI metadata and answer component questions."
---

# HuskarUI Expert

Answer HuskarUI component questions with `query_metainfo.py`. Treat Python output as the primary source. Read source files only for verification. `guide.metainfo.json` and `query_metainfo.py` are always located in `<SKILL_DIR>`.

## Capabilities

1.  **Lookup**: Return component documentation, properties, and examples.
2.  **Search**: Find components by keyword.
3.  **List**: Return all available components.

## Rules

1. Always use Python.
2. Never read the full `guide.metainfo.json` file directly.
3. Read source files only when Python output is unclear, incomplete, or needs verification.

## Workflow

1. Resolve the paths for `query_metainfo.py` and `guide.metainfo.json`.
2. For lookup or search, run:

```bash
python <SKILL_DIR>/query_metainfo.py <SKILL_DIR>/guide.metainfo.json <ComponentName_or_Keyword>
```

3. For list, run:

```bash
python <SKILL_DIR>/query_metainfo.py <SKILL_DIR>/guide.metainfo.json list
```

4. Base the answer on the Python output.
5. If the result includes `"sources"` and verification is needed, read the referenced source file and confirm the answer against the implementation.

## Verification

If Python output is unclear or appears outdated:

1. Look for the `"sources"` field.
2. Read the actual source file, for example `src/imports/HusAvatar.qml`.
3. Verify properties, signals, and implementation details before answering.

## Coding Guidelines

### QML Style Guide
Based on project conventions (e.g., `src/imports/HusAvatar.qml`):

1.  **Imports**:
    - Order: `QtQuick` -> `QtQuick.*` -> `HuskarUI.Basic`.
    - Use `import QtQuick.Templates as T` when inheriting from templates.

2.  **Naming**:
    - **Components**: PascalCase (e.g., `HusButton`).
    - **Properties/Functions**: camelCase (e.g., `iconSource`, `calcBestSize`).
    - **Private Members**: Prefix with double underscore (e.g., `__iconImpl`, `__bg`).
    - **IDs**: camelCase, descriptive (e.g., `control`, `titleText`).

3.  **Formatting**:
    - **Indentation**: 4 spaces.
    - **Quotes**: Single quotes `'string'` preferred for properties.
    - **Braces**: Egyptian style (opening brace on the same line).

4.  **Structure**:
    - `id` first.
    - Property declarations.
    - `implicitWidth` / `implicitHeight`.
    - Visual properties (font, color).
    - Child objects / Components.

5.  **Best Practices**:
    - **Performance**:
        - Use `Loader` for conditional complex sub-components to improve performance.
        - Avoid binding loops (circular dependencies in property bindings).
    - **JavaScript**:
        - Use `let` or `const` instead of `var` to avoid scope hoisting issues.
        - Use strict equality `===` and `!==` instead of `==` and `!=`.
        - Avoid global variables; encapsulate logic in stateless JavaScript libraries (`.js`/`.mjs` files) imported as stateless modules `.pragma library`.
        - Use arrow functions `() => {}` for short callbacks to preserve lexical `this` (if supported by the Qt version).
        - Prefer `Qt.binding(function() { ... })` when imperatively assigning bindings.

### C++ Style Guide
Based on `.clang-format`:

- **Style**: LLVM-based.
- **Standard**: C++17 or newer.
- **Indentation**: 4 spaces.
- **Pointer Alignment**: Right (`Type *ptr`).
- **Column Limit**: 100 characters.
- **Access Modifiers**: Indented by -4 spaces (align with class definition).
