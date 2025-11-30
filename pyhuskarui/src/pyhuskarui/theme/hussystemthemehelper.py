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

from PySide6.QtCore import QObject, QBasicTimer, Property, Slot, Signal, QEnum
from PySide6.QtGui import QWindow, QColor, QPalette, Qt, QGuiApplication
from PySide6.QtQml import QmlElement

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


@QmlElement
class HusSystemThemeHelper(QObject):
    """
    系统主题助手类，用于检测系统主题变化
    """

    class ColorScheme(Enum):
        """颜色方案枚举"""
        Unknown = 0
        Light = 1
        Dark = 2

    QEnum(ColorScheme)

    themeColorChanged = Signal(QColor)
    colorSchemeChanged = Signal(ColorScheme)

    def __init__(self, parent: QObject = None) -> None:
        super().__init__(parent = parent)

        self._themeColor = QPalette().color(QPalette.ColorRole.Accent)
        self._timer = QBasicTimer(self)
        self._timer.start(200, self)

        QGuiApplication.styleHints().colorSchemeChanged.connect(
            self._on_color_scheme_changed)
        
    def _on_color_scheme_changed(self, color_scheme: Qt.ColorScheme):
        """
        颜色方案改变事件处理
        """
        self.colorSchemeChanged.emit(color_scheme.value)

    @Property(QColor, notify = themeColorChanged)
    def themeColor(self) -> QColor:
        """
        获取当前主题颜色（可用于绑定）
        
        Returns:
            QColor: 当前系统主题颜色
        """
        return self._themeColor

    @Property(ColorScheme, notify = colorSchemeChanged)
    def colorScheme(self) -> ColorScheme:
        """
        获取当前颜色方案（可用于绑定）
        
        Returns:
            ColorScheme: 当前颜色方案
        """
        return HusSystemThemeHelper.ColorScheme(QGuiApplication.styleHints().colorScheme().value)    

    @Slot(QWindow, bool, result = bool)
    @staticmethod
    def setWindowTitleBarMode(window: QWindow, is_dark: bool) -> bool:
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

    def timerEvent(self, event):
        """
        定时器事件处理(用于兼容C++版本的实现)
        """
        if event.timerId() == self._timer.timerId():
            if self._themeColor != QPalette().color(QPalette.ColorRole.Accent):
                self._themeColor = QPalette().color(QPalette.ColorRole.Accent)
                self.themeColorChanged.emit(self._themeColor)
        super().timerEvent(event)