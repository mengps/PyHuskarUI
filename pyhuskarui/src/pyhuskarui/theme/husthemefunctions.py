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

from PySide6.QtQml import QmlElement, QmlSingleton
from PySide6.QtGui import QFontDatabase, QColor
from PySide6.QtCore import QObject, Slot

from .huscolorgenerator import HusColorGenerator
from .hussizegenerator import HusSizeGenerator
from .husradiusgenerator import HusRadiusGenerator

QML_IMPORT_NAME = "HuskarUI.Basic"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlSingleton
class HusThemeFunctions(QObject):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    @Slot(int, result=list)
    @Slot(int, bool, QColor, result=list)
    @Slot(QColor, bool, QColor, result=list)
    @staticmethod
    def genColor(color: int | QColor, light: bool = True, background: QColor = QColor()) -> List[QColor]:
        if isinstance(color, int):
            return HusColorGenerator.generate(HusColorGenerator.Preset(color), light, background)
        else:
            return HusColorGenerator.generate(color, light, background)

    @Slot(QColor, bool, QColor, result=list)
    @staticmethod
    def genColorString(color: QColor, light: bool = True, background: QColor = QColor()) -> List[str]:
        colors = HusColorGenerator.generate(color, light, background)
        return [color.name() for color in colors]

    @Slot(float, result=list)
    @staticmethod
    def genFontSize(font_size_base: float) -> List[float]:
        return HusSizeGenerator.generateFontSize(font_size_base)

    @Slot(float, result=list)
    @staticmethod
    def genFontLineHeight(font_size_base: float) -> List[float]:
        return HusSizeGenerator.generateFontLineHeight(font_size_base)

    @Slot(int, result=list)
    @staticmethod
    def genRadius(radius_base: int) -> List[int]:
        return HusRadiusGenerator.generateRadius(radius_base)

    @Slot(str, result=str)
    @staticmethod
    def genFontFamily(family_base: str) -> str:
        families = family_base.split(",")
        database = QFontDatabase.families()

        for family in families:
            normalized = family.replace("'", "").replace('"', "").strip()
            if normalized in database:
                return normalized.strip()

        return database[0] if database else "Arial"

    @Slot(QColor, result=QColor)
    @Slot(QColor, int, result=QColor)
    @staticmethod
    def darker(color: QColor, factor: int = 140) -> QColor:
        return color.darker(factor)

    @Slot(QColor, result=QColor)
    @Slot(QColor, int, result=QColor)
    @staticmethod
    def lighter(color: QColor, factor: int = 140) -> QColor:
        return color.lighter(factor)

    @Slot(QColor, result=QColor)
    @Slot(QColor, bool, result=QColor)
    @Slot(QColor, bool, int, result=QColor)
    @Slot(QColor, bool, int, int, result=QColor)
    @staticmethod
    def brightness(color: QColor, isLight: bool = True, lightFactor: int = 140, darkFactor: int = 140) -> QColor:
        if isLight:
            return color.lighter(lightFactor)
        else:
            return color.darker(darkFactor)

    @Slot(QColor, result=QColor)
    @Slot(QColor, float, result=QColor)
    @staticmethod
    def alpha(color: QColor, alpha_val: float = 0.5) -> QColor:
        return QColor(color.red(), color.green(), color.blue(), int(alpha_val * 255))

    @Slot(QColor, QColor, result=QColor)
    @staticmethod
    def onBackground(color: QColor, background: QColor) -> QColor:
        fg = color.toRgb()
        bg = background.toRgb()
        alpha_val = fg.alphaF() + bg.alphaF() * (1 - fg.alphaF())

        return QColor.fromRgbF(
            (fg.redF() * fg.alphaF() + bg.redF() * bg.alphaF() * (1 - fg.alphaF())) / alpha_val,
            (fg.greenF() * fg.alphaF() + bg.greenF() * bg.alphaF() * (1 - fg.alphaF())) / alpha_val,
            (fg.blueF() * fg.alphaF() + bg.blueF() * bg.alphaF() * (1 - fg.alphaF())) / alpha_val,
            alpha_val,
        )

    @Slot(float, float, result=float)
    @staticmethod
    def multiply(num1: float, num2: float) -> float:
        return num1 * num2
