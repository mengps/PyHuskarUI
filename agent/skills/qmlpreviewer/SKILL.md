---
name: "QmlPreviewer"
description: "Auto-detects the active QML file from editor context, runs qmlscene, and copies the rendered image to the clipboard by default. Invoke proactively when the agent needs to preview or visually verify a QML UI."
---

# QML Previewer

Use this skill to quickly run and inspect the currently edited QML file, with the rendered result copied to the clipboard by default.

## When to invoke

- The agent needs to preview the current QML page to understand its visual result
- The agent needs to visually verify QML UI changes it just made or inspected
- The agent needs screenshot-based evidence to check layout, rendering, or missing assets
- Invoke proactively without asking the user to explicitly request a preview when visual verification is needed

## Inputs required

- `qmlscene.exe` absolute path

## Execution steps

1. Resolve QML file path from current editor context:
   - Prefer the currently opened file path from IDE context if it ends with `.qml`.
   - If multiple files are open, use the actively focused editor tab.
   - If context is missing or file is not QML, search workspace for the most recently modified `.qml` file that user is editing.
2. Build and run this command as the default preview flow:

```powershell
& "<SKILL_DIR>\capture_qmlscene_to_clipboard.ps1" -QmlScenePath "<qmlscene.exe>" -QmlFilePath "<auto-detected absolute QML file path>"
```

3. If the clipboard capture flow is unavailable or unsuitable, launch the page directly instead:

```powershell
& "<qmlscene.exe>" "<auto-detected absolute QML file path>" --maximized
```

4. Read and analyze the clipboard image or live preview to report:
   - Whether the page loads successfully
   - Any obvious rendering/layout issues
   - Any visual errors or missing assets

## Fallback checks

- If launch fails, verify both paths exist and are absolute paths.
- If auto-detection fails, ask for the QML file path once, then continue with preview.
- If QML cannot load, capture terminal/runtime error output and include it in the report.
