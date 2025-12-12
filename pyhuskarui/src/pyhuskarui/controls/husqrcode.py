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

from enum import Enum

from PySide6.QtCore import (QObject, QUrl, Signal, Property, QSize, Qt, QEnum)
from PySide6.QtGui import QImage, QColor
from PySide6.QtNetwork import QNetworkRequest, QNetworkReply
from PySide6.QtQuick import QQuickItem, QSGNode, QSGTexture, QQuickWindow
from PySide6.QtQml import QmlElement, qmlEngine
from loguru import logger

from .qrcodegen import QrCode

QML_IMPORT_NAME = "HuskarUI.Basic"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class HusIconSettings(QObject):
    urlChanged = Signal()
    widthChanged = Signal()
    heightChanged = Signal()

    def __init__(self, parent = None):
        super().__init__(parent)
        self._url = QUrl()
        self._width = 40.0
        self._height = 40.0

    @Property(QUrl, notify = urlChanged)
    def url(self) -> QUrl:
        return self._url

    @url.setter
    def url(self, url: QUrl):
        if self._url != url:
            self._url = url
            self.urlChanged.emit()

    @Property(float, notify = widthChanged)
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, width: float):
        if self._width != width:
            self._width = width
            self.widthChanged.emit()

    @Property(float, notify = heightChanged)
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, height: float):
        if self._height != height:
            self._height = height
            self.heightChanged.emit()

    def is_valid(self) -> bool:
        return self._url.isValid() and self._width > 0 and self._height > 0

@QmlElement
class HusQrCode(QQuickItem):

    class ErrorLevel(Enum):
        Low = 0  # The QR Code can tolerate about  7% erroneous codewords
        Medium = 1  # The QR Code can tolerate about 15% erroneous codewords
        Quartile = 2  # The QR Code can tolerate about 25% erroneous codewords
        High = 3  # The QR Code can tolerate about 30% erroneous codewords

    QEnum(ErrorLevel)

    textChanged = Signal()
    marginChanged = Signal()
    colorChanged = Signal()
    colorMarginChanged = Signal()
    colorBgChanged = Signal()
    errorLevelChanged = Signal()

    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self._qr_code_image = QImage()
        self._text: str = ""
        self._qr_code_change = False
        self._margin = 4
        self._color_margin = QColor(Qt.transparent)
        self._color = QColor(Qt.black)
        self._color_bg = QColor(Qt.transparent)
        self._error_level = HusQrCode.ErrorLevel.Medium
        self._icon: HusIconSettings = None
        self._icon_reply = None
        self._cached_icon = QImage()

        self.setFlag(QQuickItem.ItemHasContents, True)
        self.setSize(QSize(160, 160))

        self.windowChanged.connect(self._on_window_changed)

    def _on_window_changed(self):
        self.qr_code_change = True
        self.update()

    def _req_icon(self):
        if self._icon and self._icon.is_valid():
            url = self._icon.url
            if url.isLocalFile():
                self.cached_icon = QImage(url.toLocalFile())
                self._gen_qr_code()
            else:
                if not self._cached_icon.isNull():
                    self._cached_icon = QImage()

                if self._icon_reply:
                    self._icon_reply.abort()
                    self._icon_reply = None

                network_manager = qmlEngine(self).networkAccessManager()
                if network_manager:
                    self._icon_reply = network_manager.get(
                        QNetworkRequest(url))
                    self._icon_reply.finished.connect(
                        self._on_icon_reply_finished)
                else:
                    logger.error(
                        "HusQrCode without QmlEngine, we cannot get QNetworkAccessManager!"
                    )

    def _on_icon_reply_finished(self):
        if self._icon_reply.error() == QNetworkReply.NoError:
            self._cached_icon = QImage.fromData(self._icon_reply.readAll())
            self._gen_qr_code()
        else:
            logger.error(f"Request icon error: {self._icon_reply.errorString()}")

        self._icon_reply.deleteLater()
        self._icon_reply = None

    def _gen_qr_code(self):
        ecc_map = {
            HusQrCode.ErrorLevel.Low: QrCode.Ecc.LOW,
            HusQrCode.ErrorLevel.Medium: QrCode.Ecc.MEDIUM,
            HusQrCode.ErrorLevel.Quartile: QrCode.Ecc.QUARTILE,
            HusQrCode.ErrorLevel.High: QrCode.Ecc.HIGH
        }

        ecc = ecc_map.get(self._error_level, QrCode.Ecc.MEDIUM)
        qr = QrCode.encode_text(self._text, ecc)

        qr_size = qr.get_size()
        qr_margin = qr_size + self._margin
        source_size = qr_size + self._margin * 2

        self._qr_code_image = QImage(source_size, source_size,
                                     QImage.Format_ARGB32)
        self._qr_code_image.fill(Qt.transparent)

        for y in range(-self.margin, qr_margin):
            for x in range(-self.margin, qr_margin):
                if x < 0 or y < 0 or x >= qr_size or y >= qr_size:
                    self._qr_code_image.setPixelColor(x + self.margin,
                                                      y + self.margin,
                                                      self._color_margin)
                else:
                    if qr.get_module(x, y):
                        self._qr_code_image.setPixelColor(
                            x + self.margin, y + self.margin, self._color)
                    else:
                        self._qr_code_image.setPixelColor(
                            x + self.margin, y + self.margin, self._color_bg)

        if self.width() > 0 and self.height() > 0:
            self._qr_code_image = self._qr_code_image.scaled(
                int(self.width()), int(self.height()))

        if self._icon and self._icon.is_valid() and not self._cached_icon.isNull():
            iconWidth = min(self._qr_code_image.width(), self._icon.width)
            iconHeight = min(self._qr_code_image.height(), self._icon.height)
            icon = self._cached_icon.scaled(iconWidth, iconHeight)
            startX = (self._qr_code_image.width() - iconWidth) * 0.5
            startY = (self._qr_code_image.height() - iconHeight) * 0.5
            rangeX = self._qr_code_image.width() - startX
            rangeY = self._qr_code_image.height() - startY
            for y in range(int(startY), int(rangeY)):
                for x in range(int(startX), int(rangeX)):
                    self._qr_code_image.setPixelColor(x, y, icon.pixelColor(x - int(startX), y - int(startY)))

        self._qr_code_change = True
        self.update()

    @Property(str, notify = textChanged)
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str):
        if self._text != text:
            self._text = text
            self.textChanged.emit()
            self._gen_qr_code()

    @Property(int, notify = marginChanged)
    def margin(self) -> int:
        return self._margin

    @margin.setter
    def margin(self, margin: int):
        if self._margin != margin:
            self._margin = margin
            self.marginChanged.emit()
            self._gen_qr_code()

    @Property(QColor, notify = colorChanged)
    def color(self) -> QColor:
        return self._color

    @color.setter
    def color(self, color: QColor):
        if self._color != color:
            self._color = color
            self.colorChanged.emit()
            self._gen_qr_code()

    @Property(QColor, notify = colorMarginChanged)
    def colorMargin(self) -> QColor:
        return self._color_margin

    @colorMargin.setter
    def colorMargin(self, color_margin: QColor):
        if self._color_margin != color_margin:
            self._color_margin = color_margin
            self.colorMarginChanged.emit()
            self._gen_qr_code()

    @Property(QColor, notify = colorBgChanged)
    def colorBg(self) -> QColor:
        return self._color_bg

    @colorBg.setter
    def colorBg(self, color_bg: QColor):
        if self._color_bg != color_bg:
            self._color_bg = color_bg
            self.colorBgChanged.emit()
            self._gen_qr_code()

    @Property(int, notify = errorLevelChanged)
    def errorLevel(self) -> int:
        return self._error_level

    @errorLevel.setter
    def errorLevel(self, level: int):
        if self._error_level != level:
            self._error_level = level
            self.errorLevelChanged.emit()
            self._gen_qr_code()

    @Property(HusIconSettings, constant = True)
    def icon(self) -> HusIconSettings:
        if not self._icon:
            self._icon = HusIconSettings(self)
            self._icon.urlChanged.connect(self._req_icon)
            self._icon.widthChanged.connect(self._gen_qr_code)
            self._icon.heightChanged.connect(self._gen_qr_code)
            self._req_icon()

        return self._icon

    def updatePaintNode(self, node: QSGNode, update_data):
        if not self._qr_code_image.isNull():
            if not node:
                node = self.window().createImageNode()
                texture = self.window().createTextureFromImage(
                    self._qr_code_image, QQuickWindow.TextureHasAlphaChannel)
                node.setTexture(texture)
                node.setFiltering(QSGTexture.Linear)
                node.setOwnsTexture(True)
            else:
                if self._qr_code_change:
                    texture = self.window().createTextureFromImage(
                        self._qr_code_image,
                        QQuickWindow.TextureHasAlphaChannel)
                    node.setTexture(texture)
                    self._qr_code_change = False

            node.setRect(self.boundingRect())

        return node
