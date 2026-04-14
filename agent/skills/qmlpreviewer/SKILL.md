---
name: "QmlPreviewer"
description: "Auto-detects the active QML file from editor context, runs qmlscene, and copies the rendered image to the clipboard by default. Invoke when user asks to preview or visually verify QML UI."
---

# QML Previewer

Use this skill to quickly run and inspect the currently edited QML file, with the rendered result copied to the clipboard by default.

## When to invoke

- User asks to preview a QML file
- User asks to visually verify QML UI changes
- User asks for screenshot-based UI checking

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
```powershell
& "<qmlscene.exe>" "<auto-detected absolute QML file path>" --maximized
```

5. Read and analyze the clipboard image to report:
   - Whether the page loads successfully
   - Any obvious rendering/layout issues
   - Any visual errors or missing assets
& "<qmlscene.exe>" "<auto-detected absolute QML file path>" --maximized
## Fallback checks

- If launch fails, verify both paths exist and are absolute paths.
- If auto-detection fails, ask for the QML file path once, then continue with preview.
- If QML cannot load, capture terminal/runtime error output and include it in the report.
