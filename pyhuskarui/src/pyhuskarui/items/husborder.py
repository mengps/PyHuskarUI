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

from PySide6.QtCore import QObject, Property, Signal, Qt
from PySide6.QtGui import QColor
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "HuskarUI.Basic"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class HusBorder(QObject):
    widthChanged = Signal()
    colorChanged = Signal()
    styleChanged = Signal()
    pixelAlignedChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._width = 1.0
        self._color = QColor(Qt.GlobalColor.transparent.value)
        self._style = QColor(Qt.PenStyle.SolidLine.value)
        self._pixelAligned = True

    @Property(float, notify=widthChanged)
    def width(self):
        return self._width

    @width.setter
    def width(self, value: float):
        if self._width == value:
            return
        self._width = value
        self.widthChanged.emit()

    @Property(QColor, notify=colorChanged)
    def color(self):
        return self._color

    @color.setter
    def color(self, value: QColor):
        if self._color == value:
            return
        self._color = value
        self.colorChanged.emit()

    @Property(int, notify=styleChanged)
    def style(self):
        return self._style

    @style.setter
    def style(self, value: Qt.PenStyle):
        if self._style == value:
            return
        self._style = value
        self.styleChanged.emit()

    @Property(bool, notify=pixelAlignedChanged)
    def pixelAligned(self):
        return self._pixelAligned

    @pixelAligned.setter
    def pixelAligned(self, value: bool):
        if self._pixelAligned == value:
            return
        self._pixelAligned = value
        self.pixelAlignedChanged.emit()

    def isValid(self) -> bool:
        return all(
            [
                self._width > 0.0,
                self._color.isValid(),
                self._color.alpha() > 0,
            ]
        )
