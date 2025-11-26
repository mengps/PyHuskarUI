# Copyright (C) 2025 mengps (MenPenS)
# SPDX-License-Identifier: Apache-2.0
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

from PySide6.QtCore import (Property, Signal, QUrl, QRectF, QSize, QPointF,
                            QLoggingCategory)
from PySide6.QtGui import QPainter, QFont, QColor, QImage, QFontMetricsF
from PySide6.QtNetwork import QNetworkRequest, QNetworkReply
from PySide6.QtQuick import QQuickPaintedItem
from PySide6.QtQml import QmlElement, qmlEngine

# 创建日志分类
lcHusWatermark = QLoggingCategory("huskarui.basic.watermark")

QML_IMPORT_NAME = "HuskarUI.Basic"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class HusWatermark(QQuickPaintedItem):

    textChanged = Signal()
    imageChanged = Signal()
    markSizeChanged = Signal()
    gapChanged = Signal()
    offsetChanged = Signal()
    rotateChanged = Signal()
    fontChanged = Signal()
    colorTextChanged = Signal()

    def __init__(self, parent = None):
        super().__init__(parent = parent)

        self._text = ""
        self._image = QUrl()
        self._markSize = QSize()
        self._gap = QPointF(100, 100)
        self._offset = QPointF(50, 50)
        self._rotate = -22
        self._font = QFont()
        self._colorText = QColor(0, 0, 0, 15)

        self._cachedImage = QImage()
        self._imageReply = None
        self._manager = None
        self._isSetMarkSize = False

        self.setAntialiasing(True)

    @Property(str, notify = textChanged)
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        if self._text != text:
            self._text = text
            self.textChanged.emit()
            self._updateMarkSize()
            self.update()

    @Property(QUrl, notify = imageChanged)
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        if self._image != image:
            self._image = image
            self.imageChanged.emit()
            self._updateImage()
            self.update()

    @Property(QSize, notify = markSizeChanged)
    def markSize(self):
        return self._markSize

    @markSize.setter
    def markSize(self, markSize):
        self._isSetMarkSize = True
        if self._markSize != markSize:
            self._markSize = markSize
            self.markSizeChanged.emit()
            self.update()

    @Property(QPointF, notify = gapChanged)
    def gap(self):
        return self._gap

    @gap.setter
    def gap(self, gap):
        if self._gap != gap:
            self._gap = gap
            self.gapChanged.emit()
            self.update()

    @Property(QPointF, notify = offsetChanged)
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset):
        if self._offset != offset:
            self._offset = offset
            self.offsetChanged.emit()
            self.update()

    @Property(float, notify = rotateChanged)
    def rotate(self):
        return self._rotate

    @rotate.setter
    def rotate(self, rotate):
        if self._rotate != rotate:
            self._rotate = rotate
            self.rotateChanged.emit()
            self.update()

    @Property(QFont, notify = fontChanged)
    def font(self):
        return self._font

    @font.setter
    def font(self, font):
        if self._font != font:
            self._font = font
            self.fontChanged.emit()
            self._updateMarkSize()
            self.update()

    @Property(QColor, notify = colorTextChanged)
    def colorText(self):
        return self._colorText

    @colorText.setter
    def colorText(self, colorText):
        if self._colorText != colorText:
            self._colorText = colorText
            self.colorTextChanged.emit()
            self.update()

    def _updateImage(self):
        """更新图像"""
        if self._image.isLocalFile():
            # 本地文件
            self._cachedImage = QImage(self._image.toLocalFile())
            self._updateMarkSize()
            self.update()
        else:
            # 网络文件
            if self._imageReply:
                self._imageReply.abort()
                self._imageReply = None

            # 获取网络访问管理器
            if not self._manager:
                engine = qmlEngine(self)
                if engine:
                    self._manager = engine.networkAccessManager()
                else:
                    print(
                        "HusWatermark without QmlEngine, we cannot get QNetworkAccessManager!"
                    )

            if self._manager:
                self._imageReply = self._manager.get(
                    QNetworkRequest(self._image))
                self._imageReply.finished.connect(self._onImageReplyFinished)

    def _onImageReplyFinished(self):
        """网络图像请求完成"""
        if self._imageReply.error() == QNetworkReply.NoError:
            self._cachedImage = QImage.fromData(self._imageReply.readAll())
            self._updateMarkSize()
            self.update()
        else:
            print(f"Request image error: {self._imageReply.errorString()}")

        self._imageReply.deleteLater()
        self._imageReply = None

    def _updateMarkSize(self):
        """更新水印尺寸"""
        if not self._isSetMarkSize:
            if self._cachedImage.isNull():
                # 文本水印：使用文本尺寸
                metrics = QFontMetricsF(self._font)
                textWidth = metrics.horizontalAdvance(self._text)
                textHeight = metrics.height()
                self._markSize = QSize(int(textWidth), int(textHeight))
            else:
                # 图像水印：使用图像尺寸
                self._markSize = QSize(self._cachedImage.width(),
                                       self._cachedImage.height())

    def paint(self, painter: QPainter):
        """绘制水印"""
        if not painter:
            return

        painter.save()

        if self.antialiasing():
            painter.setRenderHint(QPainter.Antialiasing)

        painter.setFont(self._font)
        painter.setPen(self._colorText)

        markWidth = self._markSize.width()
        markHeight = self._markSize.height()

        if markWidth <= 0 or markHeight <= 0:
            painter.restore()
            return

        stepX = round(markWidth + self._gap.x())
        stepY = round(markHeight + self._gap.y())

        if stepX <= 0 or stepY <= 0:
            painter.restore()
            return

        rowCount = round(self.width() / stepX + 1)
        columnCount = round(self.height() / stepY + 1)

        for row in range(rowCount):
            for column in range(columnCount):
                x = stepX * row + self._offset.x() + markWidth * 0.5
                y = stepY * column + self._offset.y() + markHeight * 0.5

                painter.save()
                painter.translate(x, y)
                painter.rotate(self._rotate)

                if self._cachedImage.isNull():
                    # 绘制文本水印
                    rect = QRectF(-markWidth * 0.5, -markHeight * 0.5,
                                  markWidth, markHeight)
                    painter.drawText(rect, self._text)
                else:
                    # 绘制图像水印
                    rect = QRectF(-markWidth * 0.5, -markHeight * 0.5,
                                  markWidth, markHeight)
                    painter.drawImage(rect, self._cachedImage)

                painter.restore()

        painter.restore()
