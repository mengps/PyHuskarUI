from PySide6.QtCore import QObject
from PySide6.QtGui import QColor
from _typeshed import Incomplete
from enum import IntEnum

QML_IMPORT_NAME: str
QML_IMPORT_MAJOR_VERSION: int

class HusColorGenerator(QObject):
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
    HUE_STEP: int
    SATURATION_STEP: float
    SATURATION_STEP2: float
    BRIGHTNESS_STEP1: float
    BRIGHTNESS_STEP2: float
    LIGHT_COLOR_COUNT: int
    DARK_COLOR_COUNT: int
    preset_table: Incomplete
    preset_str_table: Incomplete
    def __init__(self, parent=None) -> None: ...
    @staticmethod
    def reverseColor(color: QColor) -> QColor: ...
    @staticmethod
    def presetToColor(color: int | Preset | str) -> QColor: ...
    @staticmethod
    def generate(color: Preset | QColor, light: bool = True, background: QColor = ...) -> list[QColor]: ...
