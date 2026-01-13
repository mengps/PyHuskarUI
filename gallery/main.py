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

from __future__ import annotations

import sys

from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickWindow, QSGRendererInterface

import qml_rc
import images_rc
import shaders_rc
import logger

from pyhuskarui.husapp import HusApp

from customtheme import *
from themeswitchitem import *

if __name__ == "__main__":
    # 设置渲染后端, 目前来说不需要
    # QQuickWindow.setGraphicsApi(QSGRendererInterface.GraphicsApi.OpenGL)
    # QQuickWindow.setDefaultAlphaBuffer(True)

    QGuiApplication.setOrganizationName("MenPenS")
    QGuiApplication.setApplicationName("PyHuskarUI")
    QGuiApplication.setApplicationDisplayName("PyHuskarUI Gallery")
    QGuiApplication.setApplicationVersion(HusApp.libVersion())

    app = QGuiApplication(sys.argv)
    app.setWindowIcon(QIcon(":/Gallery/images/huskarui_new_square.png"))

    engine = QQmlApplicationEngine()
    engine.singletonInstance("Gallery", "CustomTheme").registerAll()

    url = QUrl("qrc:/Gallery/qml/Gallery.qml")
    engine.objectCreated.connect(
        lambda obj, obj_url: (sys.exit(-1) if obj is None and url == obj_url else None),
        Qt.ConnectionType.QueuedConnection,
    )
    engine.load(url)

    res = app.exec()
    del engine

    sys.exit(res)
