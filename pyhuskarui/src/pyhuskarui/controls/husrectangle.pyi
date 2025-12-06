from PySide6.QtCore import QObject
from PySide6.QtGui import QPainter
from PySide6.QtQml import QJSValue
from PySide6.QtQuick import QQuickPaintedItem
from _typeshed import Incomplete

QML_IMPORT_NAME: str
QML_IMPORT_MAJOR_VERSION: int

class HusRadius(QObject):
    allChanged: Incomplete
    topLeftChanged: Incomplete
    topRightChanged: Incomplete
    bottomLeftChanged: Incomplete
    bottomRightChanged: Incomplete
    def __init__(self, parent=None) -> None: ...

class HusPen(QObject):
    widthChanged: Incomplete
    colorChanged: Incomplete
    styleChanged: Incomplete
    def __init__(self, parent=None) -> None: ...
    def isValid(self) -> bool: ...

class HusRectangle(QQuickPaintedItem):
    colorChanged: Incomplete
    radiusChanged: Incomplete
    topLeftRadiusChanged: Incomplete
    topRightRadiusChanged: Incomplete
    bottomLeftRadiusChanged: Incomplete
    bottomRightRadiusChanged: Incomplete
    doUpdateSlotIdx: int
    def __init__(self, parent=None) -> None: ...
    def getGradient(self) -> QJSValue: ...
    def setGradient(self, value: QJSValue): ...
    def resetGradient(self) -> None: ...
    gradient: Incomplete
    def border(self): ...
    def paint(self, painter: QPainter): ...
