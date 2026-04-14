# Agent Skills

This directory provides two agent skills for this repository:

- `huskarui`: Query HuskarUI component documentation, properties, and examples from repository metadata via Python.
- `qmlpreviewer`: Preview the currently edited QML file with `qmlscene` and capture the running screenshot to the clipboard.

## Prerequisites

### huskarui

- `agent/skills/huskarui/query_metainfo.py`
- `agent/skills/huskarui/guide.metainfo.json`
- Python available on your system (`python`)

### qmlpreviewer

- `qmlscene.exe` absolute path (Qt)

## Installation

Copy (or symlink/junction) these folders into your agent's skills directory (the directory your agent scans for `SKILL.md`):

- `agent/skills/huskarui`
- `agent/skills/qmlpreviewer`

## Usage

Once installed, you can ask the AI questions. Beyond basic component lookups, you can ask the AI to help with more complex tasks.

### huskarui examples
*   "How do I use the HusAvatar component?"
*   "Show me the properties for HusButton."
*   "Find components related to 'navigation'."
*   "List all available HuskarUI components."

You can also ask for end-to-end code based on a concrete scenario:

*   **Create App Skeleton**
    > "Create a dashboard app skeleton using HuskarUI with a sidebar navigation and a top header."

*   **Create Functional Pages**
    > "Create a user profile page using HuskarUI, including an avatar (HusAvatar), a username input (HusTextField), and a save button (HusButton)."

*   **Implement Interactions**
    > "How do I implement a delete button with a confirmation dialog using HuskarUI? Please provide the full code."

The AI should use `agent/skills/huskarui/query_metainfo.py` to retrieve accurate information from `agent/skills/huskarui/guide.metainfo.json` and generate code that follows the project's standards.

### qmlpreviewer examples

*   "Preview the current QML file."
*   "Take a screenshot of the current QML UI and tell me if the layout looks correct."
*   "Visually verify the QML changes I just made."
