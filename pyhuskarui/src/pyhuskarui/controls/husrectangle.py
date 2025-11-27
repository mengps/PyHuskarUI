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

from PySide6.QtCore import QObject, Property, Qt, QPointF, QRectF, QSize, Signal
from PySide6.QtGui import QColor, QPainter, QPen, QPainterPath
from PySide6.QtQml import QmlElement, QJSValue
from PySide6.QtQuick import QQuickPaintedItem

QML_IMPORT_NAME = "HuskarUI.Basic"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class HusRadius(QObject):
    
    allChanged = Signal()
    topLeftChanged = Signal()
    topRightChanged = Signal()
    bottomLeftChanged = Signal()
    bottomRightChanged = Signal()

    def __init__(self, parent = None):
        QObject.__init__(self, parent)
        self._all = 0.0
        self._topLeft = -1.0
        self._topRight = -1.0
        self._bottomLeft = -1.0
        self._bottomRight = -1.0
         
    @Property(float, notify = allChanged)
    def all(self):
        return self._all

    @all.setter
    def all(self, value: float):
        if self._all == value:
            return
        self._all = value
        self.allChanged.emit()

        if self._topLeft < 0.0:
            self.topLeftChanged.emit()
        if self._topRight < 0.0:
            self.topRightChanged.emit()
        if self._bottomLeft < 0.0:
            self.bottomLeftChanged.emit()
        if self._bottomRight < 0.0:
            self.bottomRightChanged.emit()

    @Property(float, notify = topLeftChanged)
    def topLeft(self):
        if self._topLeft >= 0.0:
            return self._topLeft
        return self._all

    @topLeft.setter
    def topLeft(self, value: float):
        if self._topLeft == value:
            return
        if value < 0.0:
            print(f"topLeftRadius must >=0.0 { value=}")
            return
        self._topLeft = value
        self.topLeftChanged.emit()

    @Property(float, notify = topRightChanged)
    def topRight(self):
        if self._topRight >= 0.0:
            return self._topRight
        return self._all

    @topRight.setter
    def topRight(self, value: float):
        if self._topRight == value:
            return
        if value < 0.0:
            print(f"topRightRadius must >=0.0 { value=}")
            return
        self._topRight = value
        self.topRightChanged.emit()

    @Property(float, notify = bottomLeftChanged)
    def bottomLeft(self):
        if self._bottomLeft >= 0.0:
            return self._bottomLeft
        return self._all

    @bottomLeft.setter
    def bottomLeft(self, value: float):
        if self._bottomLeft == value:
            return
        if value < 0.0:
            print(f"bottomLeftRadius must >=0.0 { value=}")
            return
        self._bottomLeft = value
        self.bottomLeftChanged.emit()

    @Property(float, notify = bottomRightChanged)
    def bottomRight(self):
        if self._bottomRight >= 0.0:
            return self._bottomRight
        return self._all

    @bottomRight.setter
    def bottomRight(self, value: float):
        if self._bottomRight == value:
            return
        if value < 0.0:
            print(f"bottomRightRadius must >=0.0 { value=}")
            return
        self._bottomRight = value
        self.bottomRightChanged.emit()


@QmlElement
class HusPen(QObject):
    
    widthChanged = Signal()
    colorChanged = Signal()
    styleChanged = Signal()

    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self._width = 1.0
        self._color = QColor(Qt.GlobalColor.transparent.value)
        self._style = QColor(Qt.PenStyle.SolidLine.value)

    @Property(float, notify = widthChanged)
    def width(self):
        return self._width

    @width.setter
    def width(self, value: float):
        if self._width == value:
            return
        self._width = value
        self.widthChanged.emit()

    @Property(QColor, notify = colorChanged)
    def color(self):
        return self._color

    @color.setter
    def color(self, value: QColor):
        if self._color == value:
            return
        self._color = value
        self.colorChanged.emit()

    @Property(int, notify = styleChanged)
    def style(self):
        return self._style

    @style.setter
    def style(self, value: Qt.PenStyle):
        if self._style == value:
            return
        self._style = value
        self.styleChanged.emit()

    def isValid(self) -> bool:
        return all([
            self._width > 0.0,
            self._color.isValid(),
            self._color.alpha() > 0,
        ])


@QmlElement
class HusRectangle(QQuickPaintedItem):
    
    colorChanged = Signal()
    radiusChanged = Signal()
    topLeftRadiusChanged = Signal()
    topRightRadiusChanged = Signal()
    bottomLeftRadiusChanged = Signal()
    bottomRightRadiusChanged = Signal()

    def __init__(self, parent = None):
        super().__init__(parent)
        self._color = QColor(0xFFFFFF)
        self._radius = 0.0
        self._topLeftRadius = -1.0
        self._topRightRadius = -1.0
        self._bottomLeftRadius = -1.0
        self._bottomRightRadius = -1.0
        self._pen = None
        self._gradient = QJSValue()
        self.doUpdateSlotIdx = -1

    @Property(QColor, notify = colorChanged)
    def color(self) -> QColor:
        return self._color

    @color.setter
    def color(self, value: QColor):
        if self._color == value:
            return
        self._color = value
        self.colorChanged.emit()
        self.update()

    def getGradient(self) -> QJSValue:
        return self._gradient

    def setGradient(self, value: QJSValue):
        if self._gradient.equals(value):
            return
        
        self._gradient = value
        self.update()
        # todo
        # QMetaMethod.fromSignal(QQuickGradient)

    def resetGradient(self):
        self.setGradient(QJSValue())

    gradient = Property(
        QJSValue,
        getGradient,
        setGradient,
        resetGradient,
    )

    @Property(HusPen)
    def border(self):
        if self._pen is None:
            self._pen = HusPen(self)
            # QQml_setParent_noEvent(self._pen, self) #todo
            self._pen.colorChanged.connect(self.update)
            self._pen.widthChanged.connect(self.update)
            self._pen.styleChanged.connect(self.update)

    @Property(float, notify = radiusChanged)
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value: float):
        if self._radius == value:
            return
        self._radius = value
        self.radiusChanged.emit()
        if self._topLeftRadius < 0:
            self.topLeftRadiusChanged.emit()
        if self._topRightRadius < 0:
            self.topRightRadiusChanged.emit()
        if self._bottomLeftRadius < 0:
            self.bottomLeftRadiusChanged.emit()
        if self._bottomRightRadius < 0:
            self.bottomRightRadiusChanged.emit()
        self.update()

    @Property(float, notify = topLeftRadiusChanged)
    def topLeftRadius(self):
        if self._topLeftRadius >= 0.0:
            return self._topLeftRadius
        return self._radius

    @topLeftRadius.setter
    def topLeftRadius(self, value: float):
        if self._topLeftRadius == value:
            return
        if value < 0.0:
            print(f"topLeftRadius must >=0.0 { value=}")
            return
        self._topLeftRadius = value
        self.topLeftRadiusChanged.emit()
        self.update()

    @Property(float, notify = topRightRadiusChanged)
    def topRightRadius(self):
        if self._topRightRadius >= 0.0:
            return self._topRightRadius
        return self._radius

    @topRightRadius.setter
    def topRightRadius(self, value: float):
        if self._topRightRadius == value:
            return
        if value < 0.0:
            print(f"topRightRadius must >=0.0 { value=}")
            return
        self._topRightRadius = value
        self.topRightRadiusChanged.emit()
        self.update()

    @Property(float, notify = bottomLeftRadiusChanged)
    def bottomLeftRadius(self):
        if self._bottomLeftRadius >= 0.0:
            return self._bottomLeftRadius
        return self._radius

    @bottomLeftRadius.setter
    def bottomLeftRadius(self, value: float):
        if self._bottomLeftRadius == value:
            return
        if value < 0.0:
            print(f"bottomLeftRadius must >=0.0 { value=}")
            return

        self._bottomLeftRadius = value
        self.bottomLeftRadiusChanged.emit()
        self.update()

    @Property(float, notify = bottomRightRadiusChanged)
    def bottomRightRadius(self):
        if self._bottomRightRadius >= 0.0:
            return self._bottomRightRadius
        return self._radius

    @bottomRightRadius.setter
    def bottomRightRadius(self, value: float):
        if self._bottomRightRadius == value:
            return
        if value < 0.0:
            print(f"bottomRightRadius must >=0.0 { value=}")
            return
        self._bottomRightRadius = value
        self.bottomRightRadiusChanged.emit()
        self.update()

    def _maybeSetImplicitAntialiasing(self) -> bool:
        implicit_aa = bool(self._radius != 0.0)
        if implicit_aa:
            implicit_aa = any([
                self._topLeftRadius > 0.0,
                self._topRightRadius > 0.0,
                self._bottomLeftRadius > 0.0,
                self._bottomRightRadius > 0.0,
            ])
        return implicit_aa

    def paint(self, painter: QPainter):
        
        painter.save()
        if any([self.antialiasing(), self._maybeSetImplicitAntialiasing()]):
            painter.setRenderHint(QPainter.Antialiasing)
        rect = self.boundingRect()
        if self._pen and self._pen.isValid():
            if rect.width() > self._pen.width * 2:
                dx = self._pen.width / 2
                rect.adjust(dx, 0, -dx, 0)
            if rect.height() > self._pen.width * 2:
                dy = self._pen.width / 2
                rect.adjust(0, dy, 0, -dy)
            painter.setPen(
                QPen(
                    self._pen.color,
                    self._pen.width,
                    Qt.PenStyle(self._pen.style),
                    Qt.FlatCap,
                    Qt.SvgMiterJoin,
                ))
        else:
            painter.setPen(Qt.transparent)
            
        max_radius = self.height() * 0.5
        top_left_radius = min(self._topLeftRadius, max_radius)
        top_right_radius = min(self._topRightRadius, max_radius)
        bottom_left_radius = min(self._bottomLeftRadius, max_radius)
        bottom_right_radius = min(self._bottomRightRadius, max_radius)
        path = QPainterPath()
        path.moveTo(rect.bottomRight() - QPointF(0, bottom_right_radius))
        path.lineTo(rect.topRight() + QPointF(0, top_right_radius))
        path.arcTo(
            QRectF(
                QPointF(rect.topRight() - QPointF(top_right_radius * 2, 0)),
                QSize(top_right_radius * 2, top_right_radius * 2),
            ),
            0,
            90,
        )
        path.lineTo(rect.topLeft() + QPointF(top_left_radius, 0))
        path.arcTo(
            QRectF(QPointF(rect.topLeft()),
                   QSize(top_left_radius * 2, top_left_radius * 2)),
            90,
            90,
        )
        path.lineTo(rect.bottomLeft() - QPointF(0, bottom_left_radius))
        path.arcTo(
            QRectF(
                QPointF(
                    rect.bottomLeft().x(),
                    rect.bottomLeft().y() - bottom_left_radius * 2,
                ),
                QSize(bottom_left_radius * 2, bottom_left_radius * 2),
            ),
            180,
            90,
        )
        path.lineTo(rect.bottomRight() - QPointF(bottom_right_radius, 0))
        path.arcTo(
            QRectF(
                QPointF(rect.bottomRight() -
                        QPointF(bottom_right_radius * 2, bottom_right_radius *
                                2)),
                QSize(bottom_right_radius * 2, bottom_right_radius * 2),
            ),
            270,
            90,
        )

        veritical = True
        if self._gradient.isQObject():
            ...
            #todo

            #gradient = qobject_cast(QQuickGradient, self._gradient.toQObject())
            
        painter.restore()