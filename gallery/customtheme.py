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

from PySide6.QtQml import QmlElement, QmlSingleton
from PySide6.QtCore import QObject

QML_IMPORT_NAME = "Gallery"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
@QmlSingleton
class CustomTheme(QObject):
    """
    Custom Theme class.
    """
    def __init__(self, parent: QObject = None) -> None:
        super().__init__(parent = parent)

    def registerAll(self) -> None:
        """
        Register all the custom components.
        """
