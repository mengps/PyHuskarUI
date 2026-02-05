#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
from pathlib import Path
from typing import Dict, List, Any

sources_table = {
    "HusIcon": ["pyhuskarui/src/pyhuskarui/controls/husiconfont.py"],
    "HusQrCode": ["pyhuskarui/src/pyhuskarui/controls/husqrcode.py"],
    "HusRectangle": [
        "pyhuskarui/src/pyhuskarui/controls/husrectangle.py",
    ],
    "HusRadius": [
        "pyhuskarui/src/pyhuskarui/controls/husrectangle.py",
    ],
    "HusWatermark": [
        "pyhuskarui/src/pyhuskarui/controls/huswatermark.py",
    ],
    "HusColorGenerator": [
        "pyhuskarui/src/pyhuskarui/theme/huscolorgenerator.py",
    ],
    "HusRadiusGenerator": [
        "pyhuskarui/src/pyhuskarui/theme/husradiusgenerator.py",
    ],
    "HusSizeGenerator": [
        "pyhuskarui/src/pyhuskarui/theme/hussizegenerator.py",
    ],
    "HusSystemThemeHelper": [
        "pyhuskarui/src/pyhuskarui/theme/hussystemthemehelper.py",
    ],
    "HusThemeFunctions": [
        "pyhuskarui/src/pyhuskarui/theme/husthemefunctions.py",
    ],
    "HusTheme": [
        "pyhuskarui/src/pyhuskarui/theme/hustheme.py",
    ],
    "HusApi": ["pyhuskarui/src/pyhuskarui/utils/husapi.py"],
    "HusAsyncHasher": [
        "pyhuskarui/src/pyhuskarui/utils/husasynchasher.py",
    ],
    "HusRouter": ["pyhuskarui/src/pyhuskarui/utils/husrouter.py"],
    "HusApp": ["pyhuskarui/src/pyhuskarui/husapp.py"],
    "HusAcrylic": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusAcrylic.qml"],
    "HusAnimatedImage": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusAnimatedImage.qml"],
    "HusAutoComplete": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusAutoComplete.qml"],
    "HusAvatar": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusAvatar.qml"],
    "HusBadge": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusBadge.qml"],
    "HusBreadcrumb": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusBreadcrumb.qml"],
    "HusButton": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusButton.qml"],
    "HusButtonBlock": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusButtonBlock.qml"],
    "HusCaptionBar": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusCaptionBar.qml"],
    "HusCaptionButton": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusCaptionButton.qml"],
    "HusCard": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusCard.qml"],
    "HusCarousel": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusCarousel.qml"],
    "HusCheckBox": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusCheckBox.qml"],
    "HusCheckerBoard": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusCheckerBoard.qml"],
    "HusCollapse": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusCollapse.qml"],
    "HusColorPicker": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusColorPicker.qml"],
    "HusColorPickerPanel": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusColorPickerPanel.qml"],
    "HusContextMenu": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusContextMenu.qml"],
    "HusCopyableText": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusCopyableText.qml"],
    "HusDateTimePicker": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusDateTimePicker.qml"],
    "HusDateTimePickerPanel": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusDateTimePickerPanel.qml"],
    "HusDivider": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusDivider.qml"],
    "HusDrawer": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusDrawer.qml"],
    "HusEmpty": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusEmpty.qml"],
    "HusIconButton": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusIconButton.qml"],
    "HusIconText": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusIconText.qml"],
    "HusImage": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusImage.qml"],
    "HusImagePreview": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusImagePreview.qml"],
    "HusInput": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusInput.qml"],
    "HusInputInteger": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusInputInteger.qml"],
    "HusInputNumber": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusInputNumber.qml"],
    "HusLabel": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusLabel.qml"],
    "HusMenu": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusMenu.qml"],
    "HusMessage": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusMessage.qml"],
    "HusModal": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusModal.qml"],
    "HusMoveMouseArea": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusMoveMouseArea.qml"],
    "HusMultiSelect": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusMultiSelect.qml"],
    "HusNotification": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusNotification.qml"],
    "HusOTPInput": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusOTPInput.qml"],
    "HusPagination": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusPagination.qml"],
    "HusPopconfirm": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusPopconfirm.qml"],
    "HusPopover": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusPopover.qml"],
    "HusPopup": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusPopup.qml"],
    "HusProgress": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusProgress.qml"],
    "HusRadio": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusRadio.qml"],
    "HusRadioBlock": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusRadioBlock.qml"],
    "HusRate": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusRate.qml"],
    "HusResizeMouseArea": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusResizeMouseArea.qml"],
    "HusScrollBar": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusScrollBar.qml"],
    "HusSelect": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusSelect.qml"],
    "HusShadow": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusShadow.qml"],
    "HusSlider": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusSlider.qml"],
    "HusSpace": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusSpace.qml"],
    "HusSpin": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusSpin.qml"],
    "HusSwitch": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusSwitch.qml"],
    "HusSwitchEffect": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusSwitchEffect.qml"],
    "HusTableView": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusTableView.qml"],
    "HusTabView": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusTabView.qml"],
    "HusTag": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusTag.qml"],
    "HusText": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusText.qml"],
    "HusTextArea": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusTextArea.qml"],
    "HusTimeline": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusTimeline.qml"],
    "HusToolTip": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusToolTip.qml"],
    "HusTourFocus": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusTourFocus.qml"],
    "HusTourStep": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusTourStep.qml"],
    "HusTreeView": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusTreeView.qml"],
    "HusTransfer": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusTransfer.qml"],
    "HusWindow": ["pyhuskarui/src/pyhuskarui/qml/HuskarUI/Basic/HusWindow.qml"],
}


def extract_component_name(qml_file_path: Path) -> str:
    """从QML文件路径提取组件名称

    Args:
        qml_file_path: QML文件路径，格式为 ...Examples/Category/ExpComponentName.qml

    Returns:
        组件名称，如HusComponentName；如果无法提取则返回空字符串
    """
    filename = qml_file_path.stem
    if filename.startswith("Exp"):
        return "Hus" + filename[3:]
    return ""


def extract_docs_from_qml(qml_file_path: Path, project_root: Path) -> Dict[str, Any]:
    """
    从单个 QML 文件中提取文档信息

    Args:
        qml_file_path: QML 文件路径

    Returns:
        包含文档信息的字典
    """
    with open(qml_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 提取 DocDescription 的 desc 属性
    doc_description = ""

    # 使用更健壮的方法来提取多行字符串
    # 首先找到 DocDescription 的开始位置
    doc_desc_start = content.find("DocDescription")
    if doc_desc_start != -1:
        # 找到 desc: qsTr(` 的位置
        desc_start = content.find("desc: qsTr(`", doc_desc_start)
        if desc_start != -1:
            # 找到开始反引号的位置
            backtick_start = content.find("`", desc_start) + 1
            if backtick_start > 0:
                # 使用更健壮的方法来查找结束的反引号
                # 考虑到可能有转义的反引号或嵌套的反引号
                in_escape = False
                pos = backtick_start
                while pos < len(content):
                    if content[pos] == "\\" and not in_escape:
                        # 遇到转义字符，跳过下一个字符
                        in_escape = True
                    elif content[pos] == "`" and not in_escape:
                        # 找到非转义的反引号，可能是结束位置
                        # 检查后面是否还有反引号（三反引号情况）
                        if pos + 2 < len(content) and content[pos + 1] == "`" and content[pos + 2] == "`":
                            # 三反引号，跳过
                            pos += 3
                        else:
                            # 单反引号，结束
                            backtick_end = pos
                            doc_description = content[backtick_start:backtick_end].strip()
                            break
                    else:
                        in_escape = False
                    pos += 1

    # 如果上面的方法没有成功，尝试使用正则表达式
    if not doc_description:
        # 使用更灵活的正则表达式，处理多行和嵌套内容
        doc_description_match = re.search(
            r"DocDescription\s*\{[^}]*desc:\s*qsTr\(`([^`]*(?:`(?!``)[^`]*)*)`",
            content,
            re.DOTALL,
        )
        if doc_description_match:
            doc_description = doc_description_match.group(1).strip()

    # 如果仍然没有匹配到，尝试更宽松的模式
    if not doc_description:
        doc_description_match = re.search(
            r"DocDescription\s*\{[^}]*desc:\s*qsTr\(\s*`([^`]+)`\s*\)",
            content,
            re.DOTALL,
        )
        if doc_description_match:
            doc_description = doc_description_match.group(1).strip()

    # 最后尝试：直接搜索desc: qsTr(`和`)`之间的内容
    if not doc_description:
        desc_start = content.find("desc: qsTr(`")
        if desc_start != -1:
            desc_start = content.find("`", desc_start) + 1
            if desc_start > 0:
                desc_end = content.find("`)`", desc_start)
                if desc_end != -1:
                    doc_description = content[desc_start:desc_end].strip()

    # 提取所有 CodeBox 组件
    code_boxes = []

    # 使用更健壮的方法来提取CodeBox
    # 首先找到所有CodeBox的开始位置
    codebox_start = 0
    while True:
        codebox_start = content.find("CodeBox", codebox_start)
        if codebox_start == -1:
            break

        # 找到CodeBox的开始大括号
        brace_start = content.find("{", codebox_start)
        if brace_start == -1:
            break

        # 找到匹配的结束大括号
        brace_count = 1
        pos = brace_start + 1
        while pos < len(content) and brace_count > 0:
            if content[pos] == "{":
                brace_count += 1
            elif content[pos] == "}":
                brace_count -= 1
            pos += 1

        if brace_count == 0:
            codebox_content = content[brace_start + 1 : pos - 1]

            # 提取description - 严格限制在 desc: qsTr(` 和 `) 之间
            # 使用最简单直接的方法
            desc_start_str = "desc: qsTr(`"
            desc_start_pos = codebox_content.find(desc_start_str)
            if desc_start_pos != -1:
                # 从反引号之后开始查找
                search_start = desc_start_pos + len(desc_start_str)
                # 查找 `) 序列（反引号后跟右括号）
                closing_seq = "`)"
                closing_pos = codebox_content.find(closing_seq, search_start)
                if closing_pos != -1:
                    # 提取中间的内容
                    desc = codebox_content[search_start:closing_pos].strip()
                else:
                    desc = ""
            else:
                desc = ""

            # 提取code - 从 code: 开始，到下一个字段定义或结尾
            # 先找到 code: 的位置
            code_match_pos = re.search(r"code:\s*`", codebox_content)
            if code_match_pos:
                code_start = code_match_pos.end()  # 从 ` 开始
                # 找到结束位置 - 下一个字段定义的开始或文本结束
                remaining_content = codebox_content[code_start:]

                # 查找下一个字段定义，包括 exampleDelegate
                next_field_match = re.search(r"\s+(?:desc|descTitle|exampleDelegate):\s*", remaining_content)
                if next_field_match:
                    code = remaining_content[: next_field_match.start()].rstrip("` ")
                else:
                    # 如果没有找到下一个字段，尝试找到结束的反引号
                    # 使用更健壮的方法来查找结束的反引号
                    in_escape = False
                    pos = 0
                    while pos < len(remaining_content):
                        if remaining_content[pos] == "\\" and not in_escape:
                            # 遇到转义字符，跳过下一个字符
                            in_escape = True
                        elif remaining_content[pos] == "`" and not in_escape:
                            # 找到非转义的反引号，可能是结束位置
                            # 检查后面是否还有反引号（三反引号情况）
                            if (
                                pos + 2 < len(remaining_content)
                                and remaining_content[pos + 1] == "`"
                                and remaining_content[pos + 2] == "`"
                            ):
                                # 三反引号，跳过
                                pos += 3
                            else:
                                # 单反引号，结束
                                code = remaining_content[:pos]
                                break
                        else:
                            in_escape = False
                        pos += 1
                    else:
                        # 如果没有找到结束的反引号，使用全部内容
                        code = remaining_content

                # 清理代码末尾可能存在的多余字符
                code = code.rstrip("`").strip()
            else:
                # 如果没找到，尝试更宽松的模式
                code_match = re.search(r"code:\s*`([^`]*(?:`(?!``)[^`]*)*)`", codebox_content, re.DOTALL)
                code = code_match.group(1).strip() if code_match else ""

            # 提取title - 支持单引号和反引号两种格式
            # 先尝试反引号格式
            title_match = re.search(r"descTitle:\s*qsTr\(`([^`]+)`\)", codebox_content, re.DOTALL)
            if not title_match:
                # 尝试单引号格式
                title_match = re.search(r"descTitle:\s*qsTr\('([^']+)'\)", codebox_content, re.DOTALL)
            title = title_match.group(1).strip() if title_match else ""

            if desc and code:
                code_boxes.append({"title": title, "description": desc, "code": code})

        codebox_start = pos

    # 提取组件名称并从 sources_table 中查找源文件
    component_name = extract_component_name(qml_file_path)
    sources = sources_table.get(component_name, [])

    # 使用相对路径
    rel_path = qml_file_path.relative_to(project_root).as_posix()

    return {
        "name": component_name,
        "doc": doc_description,
        "docPath": rel_path,
        "examples": code_boxes,
        "sources": sources,
    }


def extract_all_docs(examples_dir: Path, project_root: Path) -> List[Dict[str, Any]]:
    """从examples_dir目录下的所有QML文件中提取文档信息

    Returns:
        包含所有文档信息的列表
    """
    return [extract_docs_from_qml(qml_file, project_root) for qml_file in examples_dir.rglob("*.qml")]


def clean_escape_sequences(text: str, preserve_newlines: bool = False) -> str:
    """清理文本中的转义序列

    Args:
        text: 需要清理的文本
        preserve_newlines: 是否保留\\n为字面量（代码块场景使用True）

    Returns:
        清理后的文本
    """
    if not text:
        return text

    text = text.replace("\\`\\`", "``")
    text = text.replace("\\`", "`")
    text = text.replace("\\t", "\t")
    text = text.replace('\\"', '"')
    text = text.replace("\\'", "'")
    text = text.replace("\\\\", "\\")

    if not preserve_newlines:
        text = text.replace("\\n", "\n")

    return text


def save_docs_to_json(docs: List[Dict[str, Any]], output_path: Path) -> None:
    """将文档信息保存为JSON文件

    Args:
        docs: 文档信息列表
        output_path: 输出文件路径
    """
    for doc in docs:
        if doc.get("doc"):
            doc["doc"] = clean_escape_sequences(doc["doc"])

        for example in doc.get("examples", []):
            if example.get("description"):
                example["description"] = clean_escape_sequences(example["description"])
            if example.get("code"):
                example["code"] = clean_escape_sequences(example["code"], preserve_newlines=True)
            if example.get("title"):
                example["title"] = clean_escape_sequences(example["title"])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)
