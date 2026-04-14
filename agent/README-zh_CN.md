# Agent Skills（智能体技能）

本目录为本仓库提供了两个智能体技能：

- **`huskarui`**：通过 Python 从仓库元数据中查询 HuskarUI 组件的文档、属性和示例。
- **`qmlpreviewer`**：使用 `qmlscene` 预览当前编辑的 QML文件，并捕获运行截图到剪贴板。

## 前置条件

### huskarui

- `agent/skills/huskarui/query_metainfo.py`
- `agent/skills/huskarui/guide.metainfo.json`
- 系统中已安装 Python (`python`)

### qmlpreviewer

- `qmlscene.exe` 的绝对路径 (Qt)

## 安装

将这些文件夹复制（或创建符号链接/联结）到你的智能体的 skills 目录中（即你的智能体扫描 `SKILL.md` 文件的目录）：

- `agent/skills/huskarui`
- `agent/skills/qmlpreviewer`

## 使用方法

安装完成后，你可以向 AI 提问。除了基本的组件查找外，你还可以要求 AI 协助完成更复杂的任务。

### huskarui 示例

- “如何使用 HusAvatar 组件？”
- “显示 HusButton 的属性。”
- “查找与‘导航’相关的组件。”
- “列出所有可用的 HuskarUI 组件。”

你也可以基于具体场景要求生成端到端的代码：

**创建应用骨架**

> “使用 HuskarUI 创建一个带有侧边栏导航和顶部标题栏的仪表盘应用骨架。”

**创建功能页面**

> “使用 HuskarUI 创建一个用户个人资料页面，包括头像 (HusAvatar)、用户名输入框 (HusTextField) 和保存按钮 (HusButton)。”

**实现交互逻辑**

> “如何使用 HuskarUI 实现一个带确认对话框的删除按钮？请提供完整代码。”

AI 应使用 `agent/skills/huskarui/query_metainfo.py` 从 `agent/skills/huskarui/guide.metainfo.json` 中检索准确信息，并生成符合项目标准的代码。

### qmlpreviewer 示例

- “预览当前的 QML 文件。”
- “截取当前 QML 界面的截图，并告诉我布局是否正确。”
- “直观地验证我刚才所做的 QML 更改。”

