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

from PySide6.QtCore import (QPropertyAnimation, QPoint, QPointF, QSize, 
                            QEasingCurve, Property, Slot, Signal)
from PySide6.QtGui import QPainter, QPainterPath, QImage, QColor
from PySide6.QtQuick import QQuickItem, QQuickPaintedItem, QQuickItemGrabResult
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "Gallery"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class ThemeSwitchItem(QQuickPaintedItem):
    
    switchStarted = Signal()
    animationFinished = Signal()

    radiusChanged = Signal()
    durationChanged = Signal()
    colorBgChanged = Signal()
    isDarkChanged = Signal()
    targetChanged = Signal()

    def __init__(self, parent = None):
        super().__init__(parent)

        # 初始化属性
        self._radius = 0
        self._duration = 300
        self._colorBg = QColor()
        self._isDark = False
        self._target: QQuickItem = None

        # 其他成员变量
        self._source = QImage()
        self._center = QPoint()
        self._grabResult: QQuickItemGrabResult = None
        self._animation = QPropertyAnimation(self, b"radius")
        self._animation.setDuration(self._duration)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)

        self.setVisible(False)

        # 连接信号
        self._animation.finished.connect(self._onAnimationFinished)
        self.radiusChanged.connect(self.update)
        self.durationChanged.connect(self._onDurationChanged)

    def _onAnimationFinished(self):
        self.update()
        self.setVisible(False)
        self.animationFinished.emit()

    def _onDurationChanged(self):
        self._animation.setDuration(self._duration)

    @Property(int, notify = radiusChanged)
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        if self._radius != radius:
            self._radius = radius
            self.radiusChanged.emit()

    @Property(int, notify = durationChanged)
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration):
        if self._duration != duration:
            self._duration = duration
            self.durationChanged.emit()

    @Property(QColor, notify = colorBgChanged)
    def colorBg(self):
        return self._colorBg

    @colorBg.setter
    def colorBg(self, colorBg):
        if self._colorBg != colorBg:
            self._colorBg = colorBg
            self.colorBgChanged.emit()

    @Property(bool, notify = isDarkChanged)
    def isDark(self):
        return self._isDark

    @isDark.setter
    def isDark(self, isDark):
        if self._isDark != isDark:
            self._isDark = isDark
            self.isDarkChanged.emit()

    @Property(QQuickItem, notify = targetChanged)
    def target(self):
        return self._target

    @target.setter
    def target(self, target):
        if self._target != target:
            self._target = target
            self.targetChanged.emit()

    def paint(self, painter):
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制源图像
        if not self._source.isNull():
            painter.drawImage(self.boundingRect(), self._source)

        # 创建圆形路径
        path = QPainterPath()
        path.moveTo(self._center.x(), self._center.y())
        path.addEllipse(QPointF(self._center.x(), self._center.y()),
                        self._radius, self._radius)

        # 设置合成模式
        painter.setCompositionMode(QPainter.CompositionMode_Xor)

        if self._isDark:
            # 暗色模式：填充圆形区域
            painter.fillPath(path, self._colorBg)
        else:
            # 亮色模式：填充圆形以外的区域
            outerRect = QPainterPath()
            outerRect.addRect(self.boundingRect())
            outerRect = outerRect.subtracted(path)
            painter.fillPath(outerRect, self._colorBg)

        painter.restore()

    @Slot(int, int, QPoint, int)
    def start(self, width, height, center, radius):
        if not self._target:
            return

        if self._animation.state() == QPropertyAnimation.Running:
            self._animation.stop()
            currentRadius = self._radius
            self._animation.setStartValue(currentRadius)
            endValue = 0 if self._isDark else radius
            self._animation.setEndValue(endValue)
        else:
            if self._isDark:
                self._animation.setStartValue(radius)
                self._animation.setEndValue(0)
            else:
                self._animation.setStartValue(0)
                self._animation.setEndValue(radius)

        self._center = center
        self._grabResult = self._target.grabToImage(QSize(width, height))
        if self._grabResult:
            self._grabResult.ready.connect(self._onGrabReady)

    def _onGrabReady(self):
        """当图像抓取完成时的回调"""
        if self._grabResult:
            self._source = self._grabResult.data().image()
            self.update()
            self.setVisible(True)
            self.switchStarted.emit()
            self._animation.start()
