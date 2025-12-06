from .qrcodegen import QrCode as QrCode
from PySide6.QtCore import QObject
from PySide6.QtQuick import QQuickItem, QSGNode as QSGNode
from _typeshed import Incomplete
from enum import Enum

QML_IMPORT_NAME: str
QML_IMPORT_MAJOR_VERSION: int

class HusIconSettings(QObject):
    urlChanged: Incomplete
    widthChanged: Incomplete
    heightChanged: Incomplete
    def __init__(self, parent=None) -> None: ...
    def is_valid(self) -> bool: ...

class HusQrCode(QQuickItem):
    class ErrorLevel(Enum):
        Low = 0
        Medium = 1
        Quartile = 2
        High = 3
    textChanged: Incomplete
    marginChanged: Incomplete
    colorChanged: Incomplete
    colorMarginChanged: Incomplete
    colorBgChanged: Incomplete
    errorLevelChanged: Incomplete
    def __init__(self, parent=None) -> None: ...
    def icon(self) -> HusIconSettings: ...
    def updatePaintNode(self, node: QSGNode, update_data): ...
