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

from PySide6.QtCore import QObject, Property, Signal
from PySide6.QtQml import QmlElement
from loguru import logger

QML_IMPORT_NAME = "HuskarUI.Basic"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class HusRadius(QObject):
    allChanged = Signal()
    topLeftChanged = Signal()
    topRightChanged = Signal()
    bottomLeftChanged = Signal()
    bottomRightChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._all = 0.0
        self._topLeft = -1.0
        self._topRight = -1.0
        self._bottomLeft = -1.0
        self._bottomRight = -1.0

    @Property(float, notify=allChanged)
    def all(self):
        return self._all

    @all.setter
    def all(self, value: float):
        if self._all == value:
            return
        self._all = value
        self.allChanged.emit()

        if self._topLeft < 0.0:
            self.topLeftChanged.emit()
        if self._topRight < 0.0:
            self.topRightChanged.emit()
        if self._bottomLeft < 0.0:
            self.bottomLeftChanged.emit()
        if self._bottomRight < 0.0:
            self.bottomRightChanged.emit()

    @Property(float, notify=topLeftChanged)
    def topLeft(self):
        if self._topLeft >= 0.0:
            return self._topLeft
        return self._all

    @topLeft.setter
    def topLeft(self, value: float):
        if self._topLeft == value:
            return
        if value < 0.0:
            logger.error(f"topLeftRadius must >=0.0 { value=}")
            return
        self._topLeft = value
        self.topLeftChanged.emit()

    @Property(float, notify=topRightChanged)
    def topRight(self):
        if self._topRight >= 0.0:
            return self._topRight
        return self._all

    @topRight.setter
    def topRight(self, value: float):
        if self._topRight == value:
            return
        if value < 0.0:
            logger.error(f"topRightRadius must >=0.0 { value=}")
            return
        self._topRight = value
        self.topRightChanged.emit()

    @Property(float, notify=bottomLeftChanged)
    def bottomLeft(self):
        if self._bottomLeft >= 0.0:
            return self._bottomLeft
        return self._all

    @bottomLeft.setter
    def bottomLeft(self, value: float):
        if self._bottomLeft == value:
            return
        if value < 0.0:
            logger.error(f"bottomLeftRadius must >=0.0 { value=}")
            return
        self._bottomLeft = value
        self.bottomLeftChanged.emit()

    @Property(float, notify=bottomRightChanged)
    def bottomRight(self):
        if self._bottomRight >= 0.0:
            return self._bottomRight
        return self._all

    @bottomRight.setter
    def bottomRight(self, value: float):
        if self._bottomRight == value:
            return
        if value < 0.0:
            logger.error(f"bottomRightRadius must >=0.0 { value=}")
            return
        self._bottomRight = value
        self.bottomRightChanged.emit()
