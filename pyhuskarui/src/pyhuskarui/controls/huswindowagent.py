# Copyright (C) 2025 mengps (MenPenS)
# SPDX-License-Identifier: Apache-2.0
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

from PySide6.QtCore import QObject, Slot
from PySide6.QtQuick import QQuickItem
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "HuskarUI.Basic"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class HusWindowAgent(QObject):
    
    def __init__(self, parent: QObject = None) -> None:
        super().__init__(parent = parent)
        
    @Slot(QQuickItem, result = bool)
    def setTitleBar(self, item: QQuickItem) -> bool:
        """
        Set the title bar item.
        """
        return False
    
    @Slot(int, QQuickItem, result = bool)
    def setSystemButton(self, button: int, item: QQuickItem) -> bool:
        """
        Set the system button visible.
        """
        return False
    
    @Slot(QQuickItem, bool, result = bool)
    def setHitTestVisible(self, item: QQuickItem, visible: bool) -> bool:
        """
        Set the hit test visible.
        """
        return False
    
    @Slot(str, bool, result = bool)
    def setWindowAttribute(self, attribute: str, value: bool) -> bool:
        """
        Set the window attribute.
        """
        return False
