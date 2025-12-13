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

import math
from typing import List

from PySide6.QtQml import QmlElement
from PySide6.QtCore import QObject, Slot

QML_IMPORT_NAME = "HuskarUI.Basic"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class HusSizeGenerator(QObject):
    """
    HusSizeGenerator class.
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    @staticmethod
    @Slot(float, result=List)
    def generateFontSize(font_size_base: float) -> List[float]:
        font_sizes = [0.0] * 10
        for index in range(10):
            i = index - 1
            base_size = font_size_base * math.exp(i / 5.0)
            int_size = math.floor(base_size) if (i + 1) > 1 else math.ceil(base_size)
            # 转换为偶数
            font_sizes[index] = math.floor(int_size / 2) * 2

        font_sizes[1] = font_size_base
        return font_sizes

    @staticmethod
    @Slot(float, result=List)
    def generateFontLineHeight(font_size_base: float) -> List[float]:
        font_line_heights = HusSizeGenerator.generateFontSize(font_size_base)
        for index in range(10):
            font_size = font_line_heights[index]
            font_line_heights[index] = (font_size + 8) / font_size

        return font_line_heights
