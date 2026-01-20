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
from PySide6.QtCore import QObject, Slot, QEvent
from PySide6.QtQuick import QQuickItem
from PySide6.QtGui import QWindow, QGuiApplication
from PySide6.QtQml import QmlElement, QPyQmlParserStatus

# Import native event filter if on Windows
if sys.platform == "win32":
    from .huswindow_win import (
        set_window_attribute,
        install_filter,
        ReleaseCapture,
        SendMessage,
        SC_MOVE,
        HTCAPTION,
        WM_SYSCOMMAND,
    )

QML_IMPORT_NAME = "HuskarUI.Impl"
QML_IMPORT_MAJOR_VERSION = 1


class TitleBarEventFilter(QObject):
    def __init__(self, parent: QObject = None) -> None:
        super().__init__(parent=parent)
        self._host_window: QWindow = None
        self._pressed = False

    def _startSystemMove(self):
        """
        Start system move (drag window).
        """
        if self._host_window:
            if sys.platform == "win32":
                hwnd = int(self._host_window.winId())
                ReleaseCapture()
                SendMessage(hwnd, WM_SYSCOMMAND, SC_MOVE | HTCAPTION, 0)
            else:
                self._startSystemMove()

    def _startSystemResize(self, edge: int):
        """
        Start system resize.
        """
        if self._host_window:
            self._host_window.startSystemResize(edge)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        """
        Event filter.
        """
        if event.type() == QEvent.MouseButtonPress:
            self._pressed = True
            return True
        elif event.type() == QEvent.MouseButtonRelease:
            self._pressed = False
            return True
        elif event.type() == QEvent.MouseMove:
            if self._pressed:
                self._startSystemMove()
            return True
        return False


@QmlElement
class HusWindowAgent(QPyQmlParserStatus):
    def __init__(self, parent: QObject = None) -> None:
        super().__init__(parent=parent)
        self._host_window: QWindow = None
        self._title_bar: QQuickItem = None
        self._native_filter = None

    def _setup(self, window: QWindow) -> None:
        """
        Setup the window agent.
        """
        self._host_window = window

        if sys.platform == "win32":
            app = QGuiApplication.instance()
            self._native_filter = install_filter(app)
            if isinstance(window, QWindow):
                self._native_filter.add_window(window)

    def classBegin(self) -> None:
        """
        Class begin.
        """
        p = self.parent()
        assert p is not None, "HusWindowAgent parent() return nullptr!"
        if p.objectName() == "__HusWindow__":
            self._setup(p)

    def componentComplete(self) -> None:
        """
        Component complete.
        """

    @Slot(QQuickItem, result=bool)
    def setTitleBar(self, item: QQuickItem) -> bool:
        """
        Set the title bar item.
        """
        self._title_bar = item
        if sys.platform == "win32" and self._native_filter and self._host_window:
            self._native_filter.update_context(self._host_window, title_bar=item)
        return True

    @Slot(int, QQuickItem, result=bool)
    def setSystemButton(self, button: int, item: QQuickItem) -> bool:
        """
        Set the system button visible.
        """
        # Treat system buttons as hit test visible items (exclude from caption area)
        return self.setHitTestVisible(item, True)

    @Slot(QQuickItem, bool, result=bool)
    def setHitTestVisible(self, item: QQuickItem, visible: bool) -> bool:
        """
        Set the hit test visible.
        """
        if sys.platform == "win32" and self._native_filter and self._host_window:
            context = self._native_filter.contexts.get(int(self._host_window.winId()))
            if context:
                items = context["hit_test_items"]
                if visible:
                    if item not in items:
                        items.add(item)
                        item.destroyed.connect(lambda: items.remove(item))
                else:
                    items.remove(item)
                self._native_filter.update_context(self._host_window, hit_test_items=items)
                return True
        return False

    @Slot(str, bool, result=bool)
    def setWindowAttribute(self, attribute: str, value: bool) -> bool:
        """
        Set the window attribute.
        """
        if sys.platform == "win32":
            return set_window_attribute(self._host_window.winId(), attribute, value)

        # For unsupported platforms
        return False
