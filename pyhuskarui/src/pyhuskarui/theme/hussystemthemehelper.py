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

import sys
import ctypes
from ctypes import wintypes
from enum import Enum
from typing import Optional, Union

from PySide6.QtCore import QObject, QTimer, QSettings, Qt, Property, Slot, Signal, QEnum
from PySide6.QtGui import QWindow, QColor, QPalette, QGuiApplication
from PySide6.QtQml import QmlElement
from PySide6.QtWidgets import QWidget

QML_IMPORT_NAME = "HuskarUI.Basic"
QML_IMPORT_MAJOR_VERSION = 1

# Windows API 类型定义
if sys.platform == "win32":
    try:
        # 加载dwmapi.dll
        dwmapi = ctypes.windll.dwmapi

        # 定义DwmSetWindowAttribute函数
        DwmSetWindowAttribute = dwmapi.DwmSetWindowAttribute
        DwmSetWindowAttribute.argtypes = [
            wintypes.HWND,  # hwnd
            wintypes.DWORD,  # dwAttribute
            ctypes.c_void_p,  # pvAttribute
            wintypes.DWORD  # cbAttribute
        ]
        DwmSetWindowAttribute.restype = wintypes.HRESULT

        # DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20

        # 标记函数指针已初始化
        _dwm_initialized = True

    except (AttributeError, OSError):
        _dwm_initialized = False
        DwmSetWindowAttribute = None
else:
    _dwm_initialized = False
    DwmSetWindowAttribute = None


class HusSystemThemeHelperPrivate:
    """HusSystemThemeHelper的私有实现类"""

    def __init__(self, public_obj: 'HusSystemThemeHelper') -> None:
        self.q = public_obj
        self._theme_color = QColor()
        self._color_scheme = HusSystemThemeHelper.ColorScheme.Unknown

        # 创建定时器用于检测系统主题变化
        self._timer = QTimer()
        self._timer.timeout.connect(self._check_system_theme)
        self._timer.start(200)  # 每200ms检查一次

        # Windows注册表设置
        if sys.platform == "win32":
            self._theme_color_settings = QSettings(
                QSettings.Scope.UserScope,
                "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\DWM")
            self._color_scheme_settings = QSettings(
                QSettings.Scope.UserScope,
                "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize"
            )
        else:
            self._theme_color_settings = None
            self._color_scheme_settings = None

        # 初始化当前值
        #self._update_theme_color()
        #self._update_color_scheme()

    def _check_system_theme(self):
        """检查系统主题变化"""
        self._update_theme_color()

        if not hasattr(QGuiApplication.styleHints(), 'colorSchemeChanged'):
            self._update_color_scheme()

    def _update_theme_color(self):
        """更新主题颜色"""
        new_color = self.q.getThemeColor()
        if new_color != self._theme_color:
            self._theme_color = new_color
            self.q.themeColorChanged.emit(new_color)

    def _update_color_scheme(self):
        """更新颜色方案"""
        new_scheme = self.q.getColorScheme()
        if new_scheme != self._color_scheme:
            self._color_scheme = new_scheme
            self.q.colorSchemeChanged.emit(new_scheme)


@QmlElement
class HusSystemThemeHelper(QObject):
    """
    系统主题助手类，用于检测系统主题变化
    """

    class ColorScheme(Enum):
        """颜色方案枚举"""
        Unknown = 0
        Dark = 1
        Light = 2

    QEnum(ColorScheme)

    # 信号定义
    themeColorChanged = Signal(QColor)
    colorSchemeChanged = Signal(ColorScheme)

    def __init__(self, parent: QObject = None) -> None:
        super().__init__(parent)
        self._d = HusSystemThemeHelperPrivate(self)

        # 连接Qt 6.5+的系统颜色方案变化信号
        if hasattr(QGuiApplication.styleHints(), 'colorSchemeChanged'):
            QGuiApplication.styleHints().colorSchemeChanged.connect(
                self._on_qt_color_scheme_changed)

    def _on_qt_color_scheme_changed(self, scheme):
        """处理Qt 6.5+的颜色方案变化"""
        color_scheme = (HusSystemThemeHelper.ColorScheme.Dark
                        if scheme == Qt.ColorScheme.Dark else
                        HusSystemThemeHelper.ColorScheme.Light)
        self._d._color_scheme = color_scheme
        self.colorSchemeChanged.emit(color_scheme)

    def getThemeColor(self) -> QColor:
        """
        立即获取当前主题颜色（不可用于绑定）
        
        Returns:
            QColor: 当前系统主题颜色
        """
        if sys.platform == "win32" and self._d._theme_color_settings:
            """ 
            color_value = self._d._theme_color_settings.value("ColorizationColor")
            if color_value is not None:
                return QColor.fromRgb(int(color_value))
            """

        # 回退方案：使用系统调色板的高亮颜色
        return QPalette().color(QPalette.Highlight)

    def getColorScheme(self) -> ColorScheme:
        """
        立即获取当前颜色方案（不可用于绑定）
        
        Returns:
            ColorScheme: 当前颜色方案
        """
        # Qt 6.5+ 使用内置的颜色方案检测
        if hasattr(QGuiApplication.styleHints(), 'colorScheme'):
            scheme = QGuiApplication.styleHints().colorScheme()
            return (HusSystemThemeHelper.ColorScheme.Dark
                    if scheme == Qt.ColorScheme.Dark else
                    HusSystemThemeHelper.ColorScheme.Light)

        # Windows平台检测
        if sys.platform == "win32" and self._d._color_scheme_settings:
            try:
                # AppsUseLightTheme: 0=深色, 1=浅色
                use_light_theme = self._d._color_scheme_settings.value(
                    "AppsUseLightTheme", 1)
                if use_light_theme == 0:
                    return HusSystemThemeHelper.ColorScheme.Dark
                else:
                    return HusSystemThemeHelper.ColorScheme.Light
            except (ValueError, TypeError):
                pass

        # Linux/macOS或其他平台：通过调色板检测
        palette = QPalette()
        text_color = palette.color(QPalette.WindowText)
        window_color = palette.color(QPalette.Window)

        # 如果文本比窗口亮，则认为是深色模式
        if text_color.lightness() > window_color.lightness():
            return HusSystemThemeHelper.ColorScheme.Dark
        else:
            return HusSystemThemeHelper.ColorScheme.Light

    @Property(QColor, notify = themeColorChanged)
    def themeColor(self) -> QColor:
        """
        获取当前主题颜色（可用于绑定）
        
        Returns:
            QColor: 当前系统主题颜色
        """
        self._d._update_theme_color()
        return self._d._theme_color

    @Property(ColorScheme, notify = colorSchemeChanged)
    def colorScheme(self) -> ColorScheme:
        """
        获取当前颜色方案（可用于绑定）
        
        Returns:
            ColorScheme: 当前颜色方案
        """
        self._d._update_color_scheme()
        return self._d._color_scheme

    @staticmethod
    def setWindowTitleBarMode(window: Union[QWidget, QWindow],
                              is_dark: bool) -> bool:
        """
        设置窗口标题栏模式（深色/浅色）
        
        Args:
            window: 要设置的窗口对象
            is_dark: 是否为深色模式
            
        Returns:
            bool: 设置是否成功
        """
        if not _dwm_initialized or DwmSetWindowAttribute is None:
            return False

        if sys.platform != "win32":
            return False

        try:
            # 获取窗口句柄
            if hasattr(window, 'winId'):
                hwnd = window.winId()
            else:
                return False

            # 准备参数
            dark_mode = ctypes.c_int(1 if is_dark else 0)
            size = ctypes.sizeof(ctypes.c_int)

            # 调用Windows API
            result = DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE,
                                           ctypes.byref(dark_mode), size)

            # HRESULT为0表示成功
            return result == 0

        except (AttributeError, OSError, ctypes.ArgumentError):
            return False

    # 为QWidget提供重载版本
    @staticmethod
    def setWindowTitleBarModeWidget(window: QWidget, is_dark: bool) -> bool:
        """
        设置QWidget窗口标题栏模式(深色/浅色)
        
        Args:
            window: 要设置的QWidget窗口
            is_dark: 是否为深色模式
            
        Returns:
            bool: 设置是否成功
        """
        return HusSystemThemeHelper.setWindowTitleBarMode(window, is_dark)

    def timerEvent(self, event):
        """
        定时器事件处理(用于兼容C++版本的实现)
        """
        self._d._check_system_theme()
        super().timerEvent(event)
