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

from PySide6.QtCore import Qt, QUrl, QObject, QFile, QIODevice, QDateTime, Slot
from PySide6.QtGui import QGuiApplication, QWindow, QDesktopServices
from PySide6.QtQml import QmlElement, QmlSingleton


def systemName() -> str:
    """
    Get the system name.
    """
    if sys.platform.startswith("win"):
        return "windows"
    elif sys.platform.startswith("darwin"):
        return "macos"
    elif sys.platform.startswith("linux"):
        return "linux"
    else:
        return "unknown"


if systemName() == "windows":
    from ctypes import WinDLL

    user32 = WinDLL("user32")

QML_IMPORT_NAME = "HuskarUI.Basic"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlSingleton
class HusApi(QObject):
    """
    HusApp class.
    """

    def __init__(self, parent: QObject = None) -> None:
        super().__init__(parent = parent)

    @Slot(QWindow, bool)
    def setWindowStaysOnTopHint(self, window: QWindow, hint: bool) -> None:
        if window is not None:
            if systemName() == "windows":
                hwnd = window.winId()
                user32.SetWindowPos(hwnd, -1 if hint else -2, 0, 0, 0, 0,
                                    0x0001)
            else:
                window.setFlag(Qt.WindowType.WindowStaysOnTopHint, hint)

    @Slot(QWindow, int)
    def setWindowState(self, window: QWindow, state: int) -> None:
        if window is not None:
            if systemName() == "windows":
                hwnd = window.winId()
                user32.ShowWindow(hwnd, state)
            else:
                window.setWindowState(Qt.WindowState(state))

    @Slot(QObject)
    @Slot(QObject, bool, bool)
    def setPopupAllowAutoFlip(self,
                              popup: QObject,
                              allowVerticalFlip: bool = True,
                              allowHorizontalFlip: bool = True) -> None:
        pass

    @Slot(result = str)
    def getClipbordText(self) -> str:
        clipboard = QGuiApplication.clipboard()
        if clipboard is not None:
            return clipboard.text()
        else:
            return ""

    @Slot(str, result = bool)
    def setClipbordText(self, text: str) -> bool:
        clipboard = QGuiApplication.clipboard()
        if clipboard is not None:
            clipboard.setText(text)
            return True
        else:
            return False

    @Slot(str, result = str)
    def readFileToString(self, fileName: str) -> str:
        file = QFile(fileName)
        if file.open(QIODevice.ReadOnly):
            return file.readAll().toStdString()
        else:
            print("Open file error:", file.errorString())

        return ""

    @Slot(QDateTime, result = int)
    def getWeekNumber(self, dateTime: QDateTime) -> int:
        return dateTime.date().weekNumber()[0]

    @Slot(str, str, result = QDateTime)
    def dateFromString(self, dateTime: str, format: str) -> QDateTime:
        """从字符串中解析日期时间

        Args:
            dateTime (str): 日期字符串 例如: "2023-01-01 12:00:00"
            format (str): 格式字符串 例如: "yyyy-MM-dd hh:mm:ss"

        Returns:
            QDateTime: 解析后的日期时间
        """

        return QDateTime.fromString(dateTime, format)

    @Slot(str)
    def openFile(self, fileName: str) -> None:
        """打开文件

        Args:
            fileName (str): 文件名
        """

        QDesktopServices.openUrl(QUrl.fromLocalFile(fileName))
