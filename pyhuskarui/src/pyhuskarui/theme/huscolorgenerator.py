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

from enum import IntEnum
from typing import List, Union

from PySide6.QtCore import QObject, QTimer, QSettings, Property, Slot, Signal, QEnum
from PySide6.QtGui import QColor, QFontDatabase, QPalette
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "HuskarUI.Basic"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class HusColorGenerator(QObject):

    #@QEnum
    class Preset(IntEnum):
        Preset_None = 0
        Preset_Red = 1
        Preset_Volcano = 2
        Preset_Orange = 3
        Preset_Gold = 4
        Preset_Yellow = 5
        Preset_Lime = 6
        Preset_Green = 7
        Preset_Cyan = 8
        Preset_Blue = 9
        Preset_Geekblue = 10
        Preset_Purple = 11
        Preset_Magenta = 12
        Preset_Grey = 13

    QEnum(Preset)

    # 常量
    HUE_STEP = 2
    SATURATION_STEP = 0.16
    SATURATION_STEP2 = 0.05
    BRIGHTNESS_STEP1 = 0.05
    BRIGHTNESS_STEP2 = 0.15
    LIGHT_COLOR_COUNT = 5
    DARK_COLOR_COUNT = 4

    preset_table = {
        Preset.Preset_Red.value: QColor(0xF5222D),
        Preset.Preset_Volcano.value: QColor(0xFA541C),
        Preset.Preset_Orange.value: QColor(0xFA8C16),
        Preset.Preset_Gold.value: QColor(0xFAAD14),
        Preset.Preset_Yellow.value: QColor(0xFADB14),
        Preset.Preset_Lime.value: QColor(0xA0D911),
        Preset.Preset_Green.value: QColor(0x52C41A),
        Preset.Preset_Cyan.value: QColor(0x13C2C2),
        Preset.Preset_Blue.value: QColor(0x1677FF),
        Preset.Preset_Geekblue.value: QColor(0x2F54EB),
        Preset.Preset_Purple.value: QColor(0x722ED1),
        Preset.Preset_Magenta.value: QColor(0xEB2F96),
        Preset.Preset_Grey.value: QColor(0x666666)
    }

    preset_str_table = {
        "Preset_Red": QColor(0xF5222D),
        "Preset_Volcano": QColor(0xFA541C),
        "Preset_Orange": QColor(0xFA8C16),
        "Preset_Gold": QColor(0xFAAD14),
        "Preset_Yellow": QColor(0xFADB14),
        "Preset_Lime": QColor(0xA0D911),
        "Preset_Green": QColor(0x52C41A),
        "Preset_Cyan": QColor(0x13C2C2),
        "Preset_Blue": QColor(0x1677FF),
        "Preset_Geekblue": QColor(0x2F54EB),
        "Preset_Purple": QColor(0x722ED1),
        "Preset_Magenta": QColor(0xEB2F96),
        "Preset_Grey": QColor(0x666666)
    }

    def __init__(self, parent = None):
        super().__init__(parent)

    @staticmethod
    def _mix(rgb1: QColor, rgb2: QColor, amount: int) -> QColor:
        p = amount / 100.0
        return QColor.fromRgbF(
            (rgb2.redF() - rgb1.redF()) * p + rgb1.redF(),
            (rgb2.greenF() - rgb1.greenF()) * p + rgb1.greenF(),
            (rgb2.blueF() - rgb1.blueF()) * p + rgb1.blueF())

    @staticmethod
    def _get_hue(hsv: QColor, i: int, light: bool = False) -> float:
        hue = hsv.hsvHue()
        if hue >= 60 and hue <= 240:
            hue = hue - HusColorGenerator.HUE_STEP * i if light else hue + HusColorGenerator.HUE_STEP * i
        else:
            hue = hue + HusColorGenerator.HUE_STEP * i if light else hue - HusColorGenerator.HUE_STEP * i

        if hue < 0:
            hue += 360
        elif hue >= 360:
            hue -= 360

        return hue

    @staticmethod
    def _get_saturation(hsv: QColor, i: int, light: bool = False) -> float:
        if hsv.hsvHue() == 0 and hsv.hsvSaturation() == 0:
            return hsv.hsvSaturation()

        if light:
            saturation = hsv.hsvSaturationF(
            ) - HusColorGenerator.SATURATION_STEP * i
        elif i == HusColorGenerator.DARK_COLOR_COUNT:
            saturation = hsv.hsvSaturationF(
            ) + HusColorGenerator.SATURATION_STEP
        else:
            saturation = hsv.hsvSaturationF(
            ) + HusColorGenerator.SATURATION_STEP2 * i

        if saturation > 1:
            saturation = 1
        if light and i == HusColorGenerator.LIGHT_COLOR_COUNT and saturation > 0.1:
            saturation = 0.1
        if saturation < 0.06:
            saturation = 0.06

        return saturation

    @staticmethod
    def _get_value(hsv: QColor, i: int, light: bool = False) -> float:
        if light:
            value = hsv.valueF() + HusColorGenerator.BRIGHTNESS_STEP1 * i
        else:
            value = hsv.valueF() - HusColorGenerator.BRIGHTNESS_STEP2 * i

        if value > 1:
            value = 1

        return value

    @Slot(QColor, result = QColor)
    @staticmethod
    def reverseColor(color: QColor) -> QColor:
        return QColor(255 - color.red(), 255 - color.green(),
                      255 - color.blue(), color.alpha())

    @Slot(int, result = QColor)
    @staticmethod
    def presetToColor(color: int | Preset | str) -> QColor:
        if isinstance(color, HusColorGenerator.Preset):
            return HusColorGenerator.presetToColor(color.value)
        elif isinstance(color, str):
            if color in HusColorGenerator.preset_str_table:
                return HusColorGenerator.preset_str_table.get(color, QColor())
            else:
                return QColor()
        elif isinstance(color, int):
            if color in HusColorGenerator.preset_table:
                return HusColorGenerator.preset_table.get(color, QColor())
            else:
                return QColor()

        return QColor()

    @Slot(QColor, bool, QColor, result = List[QColor])
    @staticmethod
    def generate(
        color: Union[Preset, QColor],
        light: bool = True,
        background: QColor = QColor()) -> List[QColor]:
        if isinstance(color, HusColorGenerator.Preset):
            color_obj = HusColorGenerator.presetToColor(color)
        else:
            color_obj = color

        patterns =[]
        hsv = color_obj.toHsv()

        # 生成浅色
        for i in range(HusColorGenerator.LIGHT_COLOR_COUNT, 0, -1):
            hue = HusColorGenerator._get_hue(hsv, i, True) / 360.0
            saturation = HusColorGenerator._get_saturation(hsv, i, True)
            value = max(HusColorGenerator._get_value(hsv, i, True), 0.0)
            color_str = QColor.fromHsvF(hue, saturation, value).name()
            patterns.append(color_str)

        # 添加主色
        patterns.append(color_obj.name())

        # 生成深色
        for i in range(1, HusColorGenerator.DARK_COLOR_COUNT + 1):
            hue = HusColorGenerator._get_hue(hsv, i) / 360.0
            saturation = HusColorGenerator._get_saturation(hsv, i)
            value = max(HusColorGenerator._get_value(hsv, i), 0.0)
            color_str = QColor.fromHsvF(hue, saturation, value).name()
            patterns.append(color_str)

        # 暗黑主题处理
        if not light:
            dark_color_map = [(7, 15), (6, 25), (5, 30), (5, 45), (5, 65),
                              (5, 85), (4, 90), (3, 95), (2, 97), (1, 98)]
            dark_color_string = []
            bg_color = background if background.isValid() else QColor(0x141414)
            for index, amount in dark_color_map:
                dark_color_string.append(
                    HusColorGenerator._mix(QColor(bg_color), QColor(patterns[index]), amount))
            return dark_color_string

        return patterns
