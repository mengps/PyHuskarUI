---
name: "HuskarUI"
description: "Use Python to query HuskarUI metadata when the agent needs component properties, interfaces, examples, or HuskarUI-first UI code."
---

# HuskarUI Expert

Use this skill whenever the agent needs to understand HuskarUI component capabilities or generate UI code that should follow the repository's component conventions. Treat Python output as the primary source. Read source files only for verification. `guide.metainfo.json` and `query_metainfo.py` are always located in `<SKILL_DIR>`.

## When To Use

Invoke this skill proactively when any of the following is true:

1. The agent needs to know which properties, signals, slots, methods, or examples a HuskarUI component supports.
2. The agent needs to find which HuskarUI component matches a requested UI element or interaction.
3. The user asks for a page, dialog, form, toolbar, navigation area, or other UI code that should follow project conventions.
4. The user describes a generic UI need such as button, input, avatar, dialog, table, navigation, or layout, and the agent needs to map it to HuskarUI components.
5. The agent is unsure whether a native QtQuick control should be replaced by a HuskarUI component.

## Capabilities

1. **Lookup**: Return component documentation, properties, interfaces, and examples.
2. **Search**: Find components by keyword or by a requested UI role.
3. **List**: Return all available components.
4. **Component Mapping**: Help choose HuskarUI components that should replace native QtQuick controls.

## Rules

1. Always use Python.
2. Never read the full `guide.metainfo.json` file directly.
3. Read source files only when Python output is unclear, incomplete, or needs verification.
4. Prefer HuskarUI components over native QtQuick controls whenever an equivalent or near-equivalent HuskarUI component exists.
5. Use native QtQuick components only when no suitable HuskarUI component exists, or when low-level primitives are clearly more appropriate.
6. If the user asks for generic UI code, first determine whether HuskarUI provides the needed component before falling back to native controls.
7. When generating code, base component selection on metadata results instead of assumptions.

## Workflow

1. Resolve the paths for `query_metainfo.py` and `guide.metainfo.json`.
2. For list, run:

```Shell
python <SKILL_DIR>/query_metainfo.py <SKILL_DIR>/guide.metainfo.json list
```

1. For lookup or search, run:

```shell
python <SKILL_DIR>/query_metainfo.py <SKILL_DIR>/guide.metainfo.json <ComponentName_or_Keyword>
```

1. Base the answer on the Python output.
2. If the request is for UI generation, first search for the relevant HuskarUI components and use them as the default building blocks.
3. If the result includes `"sources"` and verification is needed, read the referenced source file and confirm the answer against the implementation.
4. If no suitable HuskarUI component is found, state that clearly and then use the minimum necessary native QtQuick components.

## Verification

If Python output is unclear or appears outdated:

1. Look for the `"sources"` field.
2. Read the actual source file, for example `src/imports/HusAvatar.qml`.
3. Verify properties, signals, and implementation details before answering.

## Component Selection Policy

1. Prefer `HuskarUI` components for visible controls such as buttons, inputs, avatars, dialogs, navigation, and other reusable widgets.
2. Keep native `QtQuick` usage mainly for primitives, layout glue, containers, animation, and other foundational items that are not replaced by HuskarUI.
3. When the user names a generic control, translate it to the closest HuskarUI component whenever possible.
4. When providing code, avoid mixing native controls and HuskarUI alternatives for the same role unless there is a clear technical reason.

## Coding Guidelines

### QML Style Guide

Based on project conventions (e.g., `src/imports/HusAvatar.qml`):

1. **Imports**:
   - Order: `QtQuick` -> `QtQuick.*` -> `HuskarUI.Basic`.
   - Use `import QtQuick.Templates as T` when inheriting from templates.
2. **Naming**:
   - **Components**: PascalCase (e.g., `HusButton`).
   - **Properties/Functions**: camelCase (e.g., `iconSource`, `calcBestSize`).
   - **Private Members**: Prefix with double underscore (e.g., `__iconImpl`, `__bg`).
   - **IDs**: camelCase, descriptive (e.g., `control`, `titleText`).
3. **Formatting**:
   - **Indentation**: 4 spaces.
   - **Quotes**: Single quotes `'string'` preferred for properties.
   - **Braces**: Egyptian style (opening brace on the same line).
4. **Structure**:
   - `id` first.
   - Property declarations.
   - `implicitWidth` / `implicitHeight`.
   - Visual properties (font, color).
   - Child objects / Components.
5. **Best Practices**:
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
