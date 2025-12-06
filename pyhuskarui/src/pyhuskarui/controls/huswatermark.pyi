from PySide6.QtCore import Property as Property
from PySide6.QtGui import QPainter
from PySide6.QtQuick import QQuickPaintedItem
from _typeshed import Incomplete

lcHusWatermark: Incomplete
QML_IMPORT_NAME: str
QML_IMPORT_MAJOR_VERSION: int

class HusWatermark(QQuickPaintedItem):
    textChanged: Incomplete
    imageChanged: Incomplete
    markSizeChanged: Incomplete
    gapChanged: Incomplete
    offsetChanged: Incomplete
    rotateChanged: Incomplete
    fontChanged: Incomplete
    colorTextChanged: Incomplete
    def __init__(self, parent=None) -> None: ...
    def paint(self, painter: QPainter): ...
