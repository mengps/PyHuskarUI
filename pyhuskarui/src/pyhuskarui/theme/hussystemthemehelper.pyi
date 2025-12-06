from PySide6.QtCore import QObject
from PySide6.QtGui import QColor, QWindow, Qt as Qt
from _typeshed import Incomplete
from enum import Enum

QML_IMPORT_NAME: str
QML_IMPORT_MAJOR_VERSION: int
dwmapi: Incomplete
DwmSetWindowAttribute: Incomplete
DWMWA_USE_IMMERSIVE_DARK_MODE: int

class HusSystemThemeHelper(QObject):
    class ColorScheme(Enum):
        Unknown = 0
        Light = 1
        Dark = 2
    themeColorChanged: Incomplete
    colorSchemeChanged: Incomplete
    def __init__(self, parent: QObject = None) -> None: ...
    def themeColor(self) -> QColor: ...
    def colorScheme(self) -> ColorScheme: ...
    @staticmethod
    def setWindowTitleBarMode(window: QWindow, is_dark: bool) -> bool: ...
    def timerEvent(self, event) -> None: ...
