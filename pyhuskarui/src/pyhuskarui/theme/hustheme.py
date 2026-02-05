# PyHuskarUI
#
# Copyright (C) 2025 mengps (MenPenS)
# https://github.com/mengps/PyHuskarUI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import re
from enum import Enum
from typing import Dict
from dataclasses import dataclass, field

from PySide6.QtCore import QObject, QFile, QIODevice, Property, Slot, Signal, QEnum
from PySide6.QtGui import QColor
from PySide6.QtQml import QmlElement, QmlSingleton
from loguru import logger

from .huscolorgenerator import HusColorGenerator
from .hussystemthemehelper import HusSystemThemeHelper
from .husthemefunctions import HusThemeFunctions

QML_IMPORT_NAME = "HuskarUI.Basic"
QML_IMPORT_MAJOR_VERSION = 1


class Component(Enum):
    """组件枚举"""

    HusButton = "HusButton"
    HusIconText = "HusIconText"
    HusCopyableText = "HusCopyableText"
    HusCaptionButton = "HusCaptionButton"
    HusTour = "HusTour"
    HusMenu = "HusMenu"
    HusDivider = "HusDivider"
    HusEmpty = "HusEmpty"
    HusSwitch = "HusSwitch"
    HusScrollBar = "HusScrollBar"
    HusSlider = "HusSlider"
    HusTabView = "HusTabView"
    HusToolTip = "HusToolTip"
    HusSelect = "HusSelect"
    HusInput = "HusInput"
    HusRate = "HusRate"
    HusRadio = "HusRadio"
    HusRadioBlock = "HusRadioBlock"
    HusCheckBox = "HusCheckBox"
    HusDrawer = "HusDrawer"
    HusCollapse = "HusCollapse"
    HusCard = "HusCard"
    HusPagination = "HusPagination"
    HusPopup = "HusPopup"
    HusTimeline = "HusTimeline"
    HusTag = "HusTag"
    HusTableView = "HusTableView"
    HusMessage = "HusMessage"
    HusAutoComplete = "HusAutoComplete"
    HusProgress = "HusProgress"
    HusCarousel = "HusCarousel"
    HusBreadcrumb = "HusBreadcrumb"
    HusImage = "HusImage"
    HusMultiSelect = "HusMultiSelect"
    HusDateTimePicker = "HusDateTimePicker"
    HusNotification = "HusNotification"
    HusPopconfirm = "HusPopconfirm"
    HusPopover = "HusPopover"
    HusModal = "HusModal"
    HusTextArea = "HusTextArea"
    HusSpin = "HusSpin"
    HusColorPicker = "HusColorPicker"
    HusTreeView = "HusTreeView"
    HusLabel = "HusLabel"
    HusTransfer = "HusTransfer"


@dataclass
class ComponentData:
    """组件数据"""

    path: str = ""
    token_map: dict = field(default_factory=dict)
    install_token_map: Dict[str, str] = field(default_factory=dict)


@dataclass
class ThemeData:
    """主题数据"""

    theme_object: QObject = None
    component_map: Dict[str, ComponentData] = field(default_factory=dict)


@QmlElement
@QmlSingleton
class HusTheme(QObject):
    """
    主题系统主类，管理整个应用程序的主题
    """

    class DarkMode(Enum):
        Light = 0
        Dark = 1
        System = 2

    class TextRenderType(Enum):
        QtRendering = 0
        NativeRendering = 1
        CurveRendering = 2

    QEnum(DarkMode)
    QEnum(TextRenderType)

    # 信号定义
    isDarkChanged = Signal()
    darkModeChanged = Signal()
    textRenderTypeChanged = Signal()
    sizeHintChanged = Signal()
    animationEnabledChanged = Signal()

    # 组件属性信号
    PrimaryChanged = Signal()

    HusButtonChanged = Signal()
    HusIconTextChanged = Signal()
    HusCopyableTextChanged = Signal()
    HusCaptionButtonChanged = Signal()
    HusTourChanged = Signal()
    HusMenuChanged = Signal()
    HusDividerChanged = Signal()
    HusEmptyChanged = Signal()
    HusSwitchChanged = Signal()
    HusScrollBarChanged = Signal()
    HusSliderChanged = Signal()
    HusTabViewChanged = Signal()
    HusToolTipChanged = Signal()
    HusSelectChanged = Signal()
    HusInputChanged = Signal()
    HusRateChanged = Signal()
    HusRadioChanged = Signal()
    HusRadioBlockChanged = Signal()
    HusCheckBoxChanged = Signal()
    HusDrawerChanged = Signal()
    HusCollapseChanged = Signal()
    HusCardChanged = Signal()
    HusPaginationChanged = Signal()
    HusPopupChanged = Signal()
    HusTimelineChanged = Signal()
    HusTagChanged = Signal()
    HusTableViewChanged = Signal()
    HusMessageChanged = Signal()
    HusAutoCompleteChanged = Signal()
    HusProgressChanged = Signal()
    HusCarouselChanged = Signal()
    HusBreadcrumbChanged = Signal()
    HusImageChanged = Signal()
    HusMultiSelectChanged = Signal()
    HusDateTimePickerChanged = Signal()
    HusNotificationChanged = Signal()
    HusPopconfirmChanged = Signal()
    HusPopoverChanged = Signal()
    HusModalChanged = Signal()
    HusTextAreaChanged = Signal()
    HusSpinChanged = Signal()
    HusColorPickerChanged = Signal()
    HusTreeViewChanged = Signal()
    HusLabelChanged = Signal()
    HusTransferChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._animation_enabled = True
        self._dark_mode = HusTheme.DarkMode.Light
        self._text_render_type = HusTheme.TextRenderType.QtRendering.value
        self._helper = HusSystemThemeHelper(self)
        self._theme_index_path = ":/HuskarUI/resources/theme/Index.json"
        self._index_object = {}
        self._index_token_table: dict = {}

        self._default_theme: Dict[QObject, ThemeData] = {}
        self._custom_theme: Dict[QObject, ThemeData] = {}

        self._size_hint_map = {"small": 0.8, "normal": 1.0, "large": 1.25}

        # 正则表达式
        self._func_regex = re.compile(r"\$([^)]+)\(")
        self._args_regex = re.compile(r"\(([^)]+)\)")

        # 初始化组件属性
        self._Primary = {}

        # 使用Component枚举动态初始化所有组件属性
        for component in Component:
            setattr(self, f"_{component.value}", {})

        # 连接系统主题变化信号
        self._helper.colorSchemeChanged.connect(self._on_system_color_scheme_changed)

        self.reloadTheme()

    def _on_system_color_scheme_changed(self):
        """处理系统颜色方案变化"""
        if self._dark_mode == HusTheme.DarkMode.System:
            self._reload_index_theme()
            self._reload_default_component_theme()
            self._reload_custom_component_theme()
            self.isDarkChanged.emit()

    def _parse_function(self, out: dict, token_name: str, expr: str):
        """解析函数表达式"""
        func_match = re.search(self._func_regex, expr)
        args_match = re.search(self._args_regex, expr)

        if not func_match:
            return

        if func_match and args_match:
            func_name = func_match.group(1)
            args_str = args_match.group(1)

            if func_name == "genColor":
                self._parse_gen_color(out, token_name, args_str)
            elif func_name == "genFontFamily":
                self._parse_gen_font_family(out, args_str)
            elif func_name == "genFontSize":
                self._parse_gen_font_size(out, token_name, args_str)
            elif func_name == "genFontLineHeight":
                self._parse_gen_font_line_height(out, token_name, args_str)
            elif func_name == "genRadius":
                self._parse_gen_radius(out, token_name, args_str)
            elif func_name == "darker":
                self._parse_darker(out, token_name, args_str)
            elif func_name == "lighter":
                self._parse_lighter(out, token_name, args_str)
            elif func_name == "brightness":
                self._parse_brightness(out, token_name, args_str)
            elif func_name == "alpha":
                self._parse_alpha(out, token_name, args_str)
            elif func_name == "onBackground":
                self._parse_on_background(out, token_name, args_str)
            elif func_name == "multiply":
                self._parse_multiply(out, token_name, args_str)
            else:
                logger.error(f"Unknown function name: {func_name}")
        else:
            logger.error(f"Unknown expression: {expr}")

    def _parse_gen_color(self, out: dict, token_name: str, args: str):
        """解析生成颜色函数"""
        color = self._color_from_index_table(args)
        if color.isValid():
            color_bg_base = self._index_token_table.get("colorBgBase", QColor())
            if isinstance(color_bg_base, str):
                color_bg_base = QColor(color_bg_base)

            colors = HusThemeFunctions.genColor(color, not self.isDark, color_bg_base)

            if self.isDark:
                # 暗黑模式需要后移并翻转色表
                colors.append(colors[0])
                colors.reverse()

            for i, gen_color in enumerate(colors):
                key = f"{token_name}-{i + 1}"
                out[key] = gen_color
        else:
            logger.error(f"func genColor() invalid color: {args}")

    def _parse_gen_font_family(self, out: dict, args: str):
        """解析生成字体族函数"""
        out["fontFamilyBase"] = HusThemeFunctions.genFontFamily(args.strip())

    def _parse_gen_font_size(self, out: dict, token_name: str, args: str):
        """解析生成字体大小函数"""
        try:
            base = float(args)
            font_sizes = HusThemeFunctions.genFontSize(base)
            for i, font_size in enumerate(font_sizes):
                key = f"{token_name}-{i + 1}"
                out[key] = font_size
        except ValueError:
            logger.error(f"func genFontSize() invalid size: {args}")

    def _parse_gen_font_line_height(self, out: dict, token_name: str, args: str):
        """解析生成字体行高函数"""
        try:
            base = float(args)
            line_heights = HusThemeFunctions.genFontLineHeight(base)
            for i, line_height in enumerate(line_heights):
                key = f"{token_name}-{i + 1}"
                out[key] = line_height
        except ValueError:
            logger.error(f"func genFontLineHeight() invalid size: {args}")

    def _parse_gen_radius(self, out: dict, token_name: str, args: str):
        """解析生成圆角函数"""
        try:
            base = int(args)
            radii = HusThemeFunctions.genRadius(base)
            for i, radius in enumerate(radii):
                key = f"{token_name}-{i + 1}"
                out[key] = radius
        except ValueError:
            logger.error(f"func genRadius() invalid size: {args}")

    def _parse_darker(self, out: dict, token_name: str, args: str):
        """解析变暗函数"""
        arg_list = args.split(",")
        if len(arg_list) == 1:
            arg1 = self._color_from_index_table(arg_list[0])
            out[token_name] = HusThemeFunctions.darker(arg1)
        elif len(arg_list) == 2:
            arg1 = self._color_from_index_table(arg_list[0])
            arg2 = self._number_from_index_table(arg_list[1])
            out[token_name] = HusThemeFunctions.darker(arg1, int(arg2))
        else:
            logger.error(f"func darker() only accepts 1/2 parameters: {args}")

    def _parse_lighter(self, out: dict, token_name: str, args: str):
        """解析变亮函数"""
        arg_list = args.split(",")
        if len(arg_list) == 1:
            arg1 = self._color_from_index_table(arg_list[0])
            out[token_name] = HusThemeFunctions.lighter(arg1)
        elif len(arg_list) == 2:
            arg1 = self._color_from_index_table(arg_list[0])
            arg2 = self._number_from_index_table(arg_list[1])
            out[token_name] = HusThemeFunctions.lighter(arg1, int(arg2))
        else:
            logger.error(f"func lighter() only accepts 1/2 parameters: {args}")

    def _parse_brightness(self, out: dict, token_name: str, args: str):
        """解析亮度函数"""
        arg_list = args.split(",")
        if len(arg_list) == 1:
            arg1 = self._color_from_index_table(arg_list[0])
            out[token_name] = HusThemeFunctions.brightness(arg1, not self.isDark)
        elif len(arg_list) == 2:
            arg1 = self._color_from_index_table(arg_list[0])
            arg2 = self._number_from_index_table(arg_list[1])
            out[token_name] = HusThemeFunctions.brightness(arg1, not self.isDark, int(arg2))
        elif len(arg_list) == 3:
            arg1 = self._color_from_index_table(arg_list[0])
            arg2 = self._number_from_index_table(arg_list[1])
            arg3 = self._number_from_index_table(arg_list[2])
            out[token_name] = HusThemeFunctions.brightness(arg1, not self.isDark, int(arg2), int(arg3))
        else:
            logger.error(f"func brightness() only accepts 1/2/3 parameters: {args}")

    def _parse_alpha(self, out: dict, token_name: str, args: str):
        """解析透明度函数"""
        arg_list = args.split(",")
        if len(arg_list) == 1:
            arg1 = self._color_from_index_table(arg_list[0])
            out[token_name] = HusThemeFunctions.alpha(arg1)
        elif len(arg_list) == 2:
            arg1 = self._color_from_index_table(arg_list[0])
            arg2 = self._number_from_index_table(arg_list[1])
            out[token_name] = HusThemeFunctions.alpha(arg1, arg2)
        else:
            logger.error(f"func alpha() only accepts 1/2 parameters: {args}")

    def _parse_on_background(self, out: dict, token_name: str, args: str):
        """解析背景上颜色函数"""
        arg_list = args.split(",")
        if len(arg_list) == 2:
            arg1 = self._color_from_index_table(arg_list[0].strip())
            arg2 = self._color_from_index_table(arg_list[1].strip())
            out[token_name] = HusThemeFunctions.onBackground(arg1, arg2)
        else:
            logger.error(f"func onBackground() only accepts 2 parameters: {args}")

    def _parse_multiply(self, out: dict, token_name: str, args: str):
        """解析乘法函数"""
        arg_list = args.split(",")
        if len(arg_list) == 2:
            arg1 = self._number_from_index_table(arg_list[0].strip())
            arg2 = self._number_from_index_table(arg_list[1].strip())
            out[token_name] = HusThemeFunctions.multiply(arg1, arg2)
        else:
            logger.error(f"func multiply() only accepts 2 parameters: {args}")

    def _color_from_index_table(self, token_name: str) -> QColor:
        """从索引表中获取颜色"""
        ref_token_name = token_name
        if ref_token_name.startswith("@"):
            ref_token_name = token_name[1:]
            if ref_token_name in self._index_token_table:
                value = self._index_token_table[ref_token_name]
                if isinstance(value, QColor):
                    return value
                elif isinstance(value, str):
                    color = QColor(value)
                    if color.isValid():
                        return color
                logger.error(f"Token toColor failed: {token_name}")
            else:
                logger.error(f"Index Token({ref_token_name}) not found!")
        else:
            # 按颜色处理
            color = QColor(token_name)
            # 从预置颜色中获取
            if token_name.startswith("#Preset_"):
                color = HusColorGenerator.presetToColor(token_name[1:])
            if not color.isValid():
                logger.error(f"Token toColor failed: {token_name}")
            return color

        return QColor()

    def _number_from_index_table(self, token_name: str) -> float:
        """从索引表中获取数字"""
        ref_token_name = token_name
        if ref_token_name.startswith("@"):
            ref_token_name = token_name[1:]
            if ref_token_name in self._index_token_table:
                value = self._index_token_table[ref_token_name]
                try:
                    if isinstance(value, (int, float)):
                        return float(value)
                    elif isinstance(value, str):
                        return float(value)
                except (ValueError, TypeError):
                    logger.error(f"Token toDouble failed: {ref_token_name}")
            else:
                logger.error(f"Index Token({ref_token_name}) not found!")
        else:
            try:
                return float(token_name)
            except ValueError:
                logger.error(f"Token toDouble failed: {token_name}")

        return 0.0

    def _parse_index_expr(self, token_name: str, expr: str):
        """解析索引表达式"""
        expr = expr.strip()

        if expr.startswith("@"):
            ref_token_name = expr[1:]
            if ref_token_name in self._index_token_table:
                self._index_token_table[token_name] = self._index_token_table[ref_token_name]
            else:
                logger.error(f"Token({expr}):Ref({ref_token_name}) not found!")
        elif expr.startswith("$"):
            self._parse_function(self._index_token_table, token_name, expr)
        elif expr.startswith("#"):
            # 按颜色处理
            color = QColor(expr)
            # 从预置颜色中获取
            if expr.startswith("Preset_"):
                color = HusColorGenerator.presetToColor(expr[1:])
            if not color.isValid():
                logger.error(f"Unknown color: {expr}")
            self._index_token_table[token_name] = color
        else:
            # 按字符串处理
            self._index_token_table[token_name] = expr

    def _parse_component_expr(self, token_map: dict, token_name: str, expr: str):
        """解析组件表达式"""
        expr = expr.strip()

        if expr.startswith("@"):
            ref_token_name = expr[1:]
            if ref_token_name in self._index_token_table:
                token_map[token_name] = self._index_token_table[ref_token_name]
            else:
                logger.error(f"Component: Token({token_name}):Ref({ref_token_name}) not found!")
        elif expr.startswith("$"):
            self._parse_function(token_map, token_name, expr)
        elif expr.startswith("#"):
            # 按颜色处理
            color = QColor(expr)
            # 从预置颜色中获取
            if expr.startswith("Preset_"):
                color = HusColorGenerator.presetToColor(expr[1:])
            if not color.isValid():
                logger.error(f"Component [{token_name}]: Unknown color: {expr}")
            token_map[token_name] = color
        else:
            # 按字符串处理
            token_map[token_name] = expr

    def _reload_index_theme(self):
        """重新加载索引主题"""
        self._index_token_table.clear()
        self._Primary.clear()

        init_obj = self._index_object.get("__init__", {})
        base_obj = init_obj.get("__base__", {})

        color_text_base = base_obj.get("colorTextBase", "#000000|#FFFFFF")
        color_bg_base = base_obj.get("colorBgBase", "#FFFFFF|#000000")

        color_text_list = color_text_base.split("|")
        color_bg_list = color_bg_base.split("|")

        if len(color_text_list) != 2:
            raise ValueError(f"colorTextBase({color_text_base}) Must be in light:color|dark:color format!")
        if len(color_bg_list) != 2:
            raise ValueError(f"colorBgBase({color_bg_base}) Must be in light:color|dark:color format!")

        is_dark = self.isDark
        self._index_token_table["colorTextBase"] = color_text_list[1] if is_dark else color_text_list[0]
        self._index_token_table["colorBgBase"] = color_bg_list[1] if is_dark else color_bg_list[0]

        # 处理变量
        vars_obj = init_obj.get("__vars__", {})
        for key, value in vars_obj.items():
            self._parse_index_expr(key, str(value))

        # 处理样式
        style_obj = self._index_object.get("__style__", {})
        for key, value in style_obj.items():
            self._parse_index_expr(key, str(value))

        # 更新Primary属性
        self._Primary = self._index_token_table.copy()
        self.PrimaryChanged.emit()

        # 注册默认组件主题
        component_obj = self._index_object.get("__component__", {})
        for component_name, theme_path in component_obj.items():
            self._register_default_component_theme(component_name, str(theme_path))

    def _reload_component_theme(self, data_map: Dict[QObject, ThemeData]):
        """重新加载组件主题"""
        for theme_data in data_map.values():
            for component_name, component_theme in theme_data.component_map.items():
                self._reload_component_theme_file(theme_data.theme_object, component_name, component_theme)

    def _reload_component_import(self, style: dict, component_name: str) -> bool:
        """重新加载组件导入"""
        component_obj = self._index_object.get("__component__", {})
        if component_name in component_obj:
            theme_path = component_obj[component_name]
            file = QFile(theme_path)
            if file.open(QIODevice.ReadOnly):
                try:
                    theme_content = json.loads(file.readAll().toStdString())
                    init_obj = theme_content.get("__init__", {})
                    if "__import__" in init_obj:
                        import_list = init_obj["__import__"]
                        for import_component in import_list:
                            self._reload_component_import(style, str(import_component))

                    # 读取样式
                    style_obj = theme_content.get("__style__", {})
                    for key, value in style_obj.items():
                        style[key] = value

                    return True

                except Exception as e:
                    logger.error(f"Parse import component theme [{theme_path}] failed: {e}")
                    return False
            else:
                logger.error(f"Open import component theme faild: {file.errorString()}, theme_path: {theme_path}")
        else:
            return False

    def _reload_component_theme_file(self, theme_object: QObject, component_name: str, component_theme: ComponentData):
        """重新加载组件主题文件"""
        token_map = component_theme.token_map
        install_token_map = component_theme.install_token_map

        style = {}
        if self._reload_component_import(style, component_name):
            # 读取样式
            for key, value in style.items():
                self._parse_component_expr(token_map, key, str(value))

            # 读取通过installComponentToken安装的变量
            for token, value in install_token_map.items():
                self._parse_component_expr(token_map, token, value)

            # 发出组件变化信号
            signal_name = f"{component_name}Changed"
            if hasattr(theme_object, signal_name):
                getattr(theme_object, signal_name).emit()

    def _reload_default_component_theme(self):
        """重新加载默认组件主题"""
        self._reload_component_theme(self._default_theme)

    def _reload_custom_component_theme(self):
        """重新加载自定义组件主题"""
        self._reload_component_theme(self._custom_theme)

    def _register_default_component_theme(self, component_name: str, theme_path: str):
        """注册默认组件主题"""
        if component_name in Component.__members__:
            # 根据组件名称设置对应的属性
            if hasattr(self, f"_{component_name}"):
                theme_map = getattr(self, f"_{component_name}")
                self._register_component_theme(self, component_name, theme_map, theme_path, self._default_theme)

    def _register_component_theme(
        self,
        theme_object: QObject,
        component: str,
        theme_map: dict,
        theme_path: str,
        data_map: Dict[QObject, ThemeData],
    ):
        """注册组件主题"""
        if theme_object not in data_map:
            data_map[theme_object] = ThemeData(theme_object=theme_object)

        data_map[theme_object].component_map[component] = ComponentData(path=theme_path, token_map=theme_map)

    @Property(bool, notify=isDarkChanged)
    def isDark(self) -> bool:
        """是否为暗黑模式"""
        if self._dark_mode == HusTheme.DarkMode.System:
            return self._helper.colorScheme == HusSystemThemeHelper.ColorScheme.Dark
        else:
            return self._dark_mode == HusTheme.DarkMode.Dark

    @Property(int, notify=darkModeChanged)
    def darkMode(self) -> int:
        return self._dark_mode.value

    @darkMode.setter
    def darkMode(self, mode: int):
        if self._dark_mode != HusTheme.DarkMode(mode):
            old_is_dark = self.isDark
            self._dark_mode = HusTheme.DarkMode(mode)
            if old_is_dark != self.isDark:
                self._reload_index_theme()
                self._reload_default_component_theme()
                self._reload_custom_component_theme()
                self.isDarkChanged.emit()
            self.darkModeChanged.emit()

    @Property(int, notify=textRenderTypeChanged)
    def textRenderType(self) -> int:
        return self._text_render_type

    @textRenderType.setter
    def textRenderType(self, render_type: int):
        if self._text_render_type != render_type:
            self._text_render_type = render_type
            self.textRenderTypeChanged.emit()

    @Property(dict, notify=sizeHintChanged)
    def sizeHint(self) -> Dict[str, float]:
        return self._size_hint_map.copy()

    @Property(bool, notify=animationEnabledChanged)
    def animationEnabled(self) -> bool:
        return self._animation_enabled

    @animationEnabled.setter
    def animationEnabled(self, enabled: bool):
        if self._animation_enabled != enabled:
            self._animation_enabled = enabled
            self.animationEnabledChanged.emit()

    @Property(dict, notify=PrimaryChanged)
    def Primary(self) -> dict:
        return self._Primary

    @Property(dict, notify=HusButtonChanged)
    def HusButton(self) -> dict:
        return self._HusButton

    @Property(dict, notify=HusIconTextChanged)
    def HusIconText(self) -> dict:
        return self._HusIconText

    @Property(dict, notify=HusCopyableTextChanged)
    def HusCopyableText(self) -> dict:
        return self._HusCopyableText

    @Property(dict, notify=HusCaptionButtonChanged)
    def HusCaptionButton(self) -> dict:
        return self._HusCaptionButton

    @Property(dict, notify=HusTourChanged)
    def HusTour(self) -> dict:
        return self._HusTour

    @Property(dict, notify=HusMenuChanged)
    def HusMenu(self) -> dict:
        return self._HusMenu

    @Property(dict, notify=HusDividerChanged)
    def HusDivider(self) -> dict:
        return self._HusDivider

    @Property(dict, notify=HusEmptyChanged)
    def HusEmpty(self) -> dict:
        return self._HusEmpty

    @Property(dict, notify=HusSwitchChanged)
    def HusSwitch(self) -> dict:
        return self._HusSwitch

    @Property(dict, notify=HusScrollBarChanged)
    def HusScrollBar(self) -> dict:
        return self._HusScrollBar

    @Property(dict, notify=HusSliderChanged)
    def HusSlider(self) -> dict:
        return self._HusSlider

    @Property(dict, notify=HusTabViewChanged)
    def HusTabView(self) -> dict:
        return self._HusTabView

    @Property(dict, notify=HusToolTipChanged)
    def HusToolTip(self) -> dict:
        return self._HusToolTip

    @Property(dict, notify=HusSelectChanged)
    def HusSelect(self) -> dict:
        return self._HusSelect

    @Property(dict, notify=HusInputChanged)
    def HusInput(self) -> dict:
        return self._HusInput

    @Property(dict, notify=HusRateChanged)
    def HusRate(self) -> dict:
        return self._HusRate

    @Property(dict, notify=HusRadioChanged)
    def HusRadio(self) -> dict:
        return self._HusRadio

    @Property(dict, notify=HusRadioBlockChanged)
    def HusRadioBlock(self) -> dict:
        return self._HusRadioBlock

    @Property(dict, notify=HusCheckBoxChanged)
    def HusCheckBox(self) -> dict:
        return self._HusCheckBox

    @Property(dict, notify=HusDrawerChanged)
    def HusDrawer(self) -> dict:
        return self._HusDrawer

    @Property(dict, notify=HusCollapseChanged)
    def HusCollapse(self) -> dict:
        return self._HusCollapse

    @Property(dict, notify=HusCardChanged)
    def HusCard(self) -> dict:
        return self._HusCard

    @Property(dict, notify=HusPaginationChanged)
    def HusPagination(self) -> dict:
        return self._HusPagination

    @Property(dict, notify=HusPopupChanged)
    def HusPopup(self) -> dict:
        return self._HusPopup

    @Property(dict, notify=HusTimelineChanged)
    def HusTimeline(self) -> dict:
        return self._HusTimeline

    @Property(dict, notify=HusTagChanged)
    def HusTag(self) -> dict:
        return self._HusTag

    @Property(dict, notify=HusTableViewChanged)
    def HusTableView(self) -> dict:
        return self._HusTableView

    @Property(dict, notify=HusMessageChanged)
    def HusMessage(self) -> dict:
        return self._HusMessage

    @Property(dict, notify=HusAutoCompleteChanged)
    def HusAutoComplete(self) -> dict:
        return self._HusAutoComplete

    @Property(dict, notify=HusProgressChanged)
    def HusProgress(self) -> dict:
        return self._HusProgress

    @Property(dict, notify=HusCarouselChanged)
    def HusCarousel(self) -> dict:
        return self._HusCarousel

    @Property(dict, notify=HusBreadcrumbChanged)
    def HusBreadcrumb(self) -> dict:
        return self._HusBreadcrumb

    @Property(dict, notify=HusImageChanged)
    def HusImage(self) -> dict:
        return self._HusImage

    @Property(dict, notify=HusMultiSelectChanged)
    def HusMultiSelect(self) -> dict:
        return self._HusMultiSelect

    @Property(dict, notify=HusDateTimePickerChanged)
    def HusDateTimePicker(self) -> dict:
        return self._HusDateTimePicker

    @Property(dict, notify=HusNotificationChanged)
    def HusNotification(self) -> dict:
        return self._HusNotification

    @Property(dict, notify=HusPopconfirmChanged)
    def HusPopconfirm(self) -> dict:
        return self._HusPopconfirm

    @Property(dict, notify=HusPopoverChanged)
    def HusPopover(self) -> dict:
        return self._HusPopover

    @Property(dict, notify=HusModalChanged)
    def HusModal(self) -> dict:
        return self._HusModal

    @Property(dict, notify=HusTextAreaChanged)
    def HusTextArea(self) -> dict:
        return self._HusTextArea

    @Property(dict, notify=HusSpinChanged)
    def HusSpin(self) -> dict:
        return self._HusSpin

    @Property(dict, notify=HusColorPickerChanged)
    def HusColorPicker(self) -> dict:
        return self._HusColorPicker

    @Property(dict, notify=HusTreeViewChanged)
    def HusTreeView(self) -> dict:
        return self._HusTreeView

    @Property(dict, notify=HusLabelChanged)
    def HusLabel(self) -> dict:
        return self._HusLabel

    @Property(dict, notify=HusTransferChanged)
    def HusTransfer(self) -> dict:
        return self._HusTransfer

    @Slot(QObject, str, dict, str)
    def registerCustomComponentTheme(self, theme_object: QObject, component: str, theme_map: dict, theme_path: str):
        """注册自定义组件主题"""
        self._register_component_theme(theme_object, component, theme_map, theme_path, self._custom_theme)

    @Slot()
    def reloadTheme(self):
        """重新加载主题"""
        file = QFile(self._theme_index_path)
        if file.open(QIODevice.ReadOnly):
            try:
                self._index_object = json.loads(file.readAll().toStdString())
            except json.JSONDecodeError as e:
                logger.error(f"Index.json parse faild: {e}")
            else:
                self._reload_index_theme()
                self._reload_default_component_theme()
                self._reload_custom_component_theme()

        else:
            logger.error(f"Index.json open faild: {file.errorString()}")

    # 安装主题的各种方法
    @Slot(str)
    def installThemeColorTextBase(self, light_and_dark: str):
        """设置文本基础色"""
        init_obj = self._index_object.get("__init__", {})
        base_obj = init_obj.get("__base__", {})
        base_obj["colorTextBase"] = light_and_dark.strip()
        init_obj["__base__"] = base_obj
        self._index_object["__init__"] = init_obj

        self._reload_index_theme()
        self._reload_default_component_theme()
        self._reload_custom_component_theme()

    @Slot(str)
    def installThemeColorBgBase(self, light_and_dark: str):
        """设置背景基础色"""
        init_obj = self._index_object.get("__init__", {})
        base_obj = init_obj.get("__base__", {})
        base_obj["colorBgBase"] = light_and_dark.strip()
        init_obj["__base__"] = base_obj
        self._index_object["__init__"] = init_obj

        self._reload_index_theme()
        self._reload_default_component_theme()
        self._reload_custom_component_theme()

    @Slot(QColor)
    def installThemePrimaryColorBase(self, color_base: QColor):
        """设置主基础色"""
        self.installIndexToken("colorPrimaryBase", f"$genColor({color_base.name()})")

    @Slot(int)
    def installThemePrimaryFontSizeBase(self, font_size_base: int):
        """设置字体基础大小"""
        self.installIndexToken("fontSizeBase", f"$genFontSize({font_size_base})")

    @Slot(str)
    def installThemePrimaryFontFamiliesBase(self, families_base: str):
        """设置基础字体族"""
        self.installIndexToken("fontFamilyBase", f"$genFontFamily({families_base})")

    @Slot(int)
    def installThemePrimaryRadiusBase(self, radius_base: int):
        """设置圆角半径基础大小"""
        self.installIndexToken("radiusBase", f"$genRadius({radius_base})")

    @Slot(int, int, int)
    def installThemePrimaryAnimationBase(self, duration_fast: int, duration_mid: int, duration_slow: int):
        """设置动画基础速度"""
        style_obj = self._index_object.get("__style__", {})
        style_obj["durationFast"] = str(duration_fast)
        style_obj["durationMid"] = str(duration_mid)
        style_obj["durationSlow"] = str(duration_slow)
        self._index_object["__style__"] = style_obj

        self._reload_index_theme()
        self._reload_default_component_theme()
        self._reload_custom_component_theme()

    @Slot(str, float)
    def installSizeHintRatio(self, size: str, ratio: float):
        """设置尺寸提示比率"""
        changed = False
        if size in self._size_hint_map:
            value = self._size_hint_map[size]
            if abs(value - ratio) > 1e-6:  # 浮点数比较
                changed = True
        else:
            changed = True

        if changed:
            self._size_hint_map[size] = ratio
            self.sizeHintChanged.emit()

    @Slot(str)
    def installIndexTheme(self, theme_path: str):
        """设置索引主题"""
        if theme_path != self._theme_index_path:
            if not theme_path:
                self._theme_index_path = ":/HuskarUI/theme/Index.json"
            else:
                self._theme_index_path = theme_path

            self.reloadTheme()

    @Slot(str, str)
    def installIndexToken(self, token: str, value: str):
        """设置索引主题令牌"""
        init_obj = self._index_object.get("__init__", {})
        vars_obj = init_obj.get("__vars__", {})
        vars_obj[token] = value.strip()
        init_obj["__vars__"] = vars_obj
        self._index_object["__init__"] = init_obj

        self._reload_index_theme()
        self._reload_default_component_theme()
        self._reload_custom_component_theme()

    @Slot(str, str)
    def installComponentTheme(self, component: str, theme_path: str):
        """设置组件主题"""
        component_obj = self._index_object.get("__component__", {})
        if component in component_obj:
            component_obj[component] = theme_path
            self._index_object["__component__"] = component_obj
            self._reload_default_component_theme()
        else:
            logger.error(f"Component [{component}] not found!")

    @Slot(str, str, str)
    def installComponentToken(self, component: str, token: str, value: str):
        """设置组件主题令牌"""
        # 在默认主题中查找
        for theme in self._default_theme.values():
            if component in theme.component_map:
                theme.component_map[component].install_token_map[token] = value
                self._reload_default_component_theme()
                return

        # 在自定义主题中查找
        for theme in self._custom_theme.values():
            if component in theme.component_map:
                theme.component_map[component].install_token_map[token] = value
                self._reload_custom_component_theme()
                return

        logger.error(f"Component [{component}] not found!")
