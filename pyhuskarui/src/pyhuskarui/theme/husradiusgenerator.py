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

from typing import List

from PySide6.QtQml import QmlElement
from PySide6.QtCore import QObject, Slot

QML_IMPORT_NAME = "HuskarUI.Basic"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class HusRadiusGenerator(QObject):
    """
    HusRadiusGenerator class.
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    @staticmethod
    @Slot(int, result=List)
    def generateRadius(radius_base: int) -> List[int]:
        radius_lg = radius_base
        radius_sm = radius_base
        radius_xs = radius_base
        radius_outer = radius_base

        # radiusLG
        if 5 <= radius_base < 6:
            radius_lg = radius_base + 1
        elif 6 <= radius_base < 16:
            radius_lg = radius_base + 2
        elif radius_base >= 16:
            radius_lg = 16

        # radiusSM
        if 5 <= radius_base < 7:
            radius_sm = 4
        elif 7 <= radius_base < 8:
            radius_sm = 5
        elif 8 <= radius_base < 14:
            radius_sm = 6
        elif 14 <= radius_base < 16:
            radius_sm = 7
        elif radius_base >= 16:
            radius_sm = 8

        # radiusXS
        if 2 <= radius_base < 6:
            radius_xs = 1
        elif radius_base >= 6:
            radius_xs = 2

        # radiusOuter
        if 4 < radius_base < 8:
            radius_outer = 4
        elif radius_base >= 8:
            radius_outer = 6

        return [radius_base, radius_lg, radius_sm, radius_xs, radius_outer]
