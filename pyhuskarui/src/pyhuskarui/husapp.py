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

from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QFontDatabase
from PySide6.QtQml import QQmlEngine, QmlElement, QmlSingleton

import pyhuskarui

from .qml_rc import *
from .resources_rc import *
from .shaders_rc import *

from .utils.husapi import *
from .utils.husasynchasher import *
from .theme.hustheme import *
from .theme.huscolorgenerator import *
from .theme.husthemefunctions import *
from .theme.husradiusgenerator import *
from .theme.hussizegenerator import *
from .theme.hussystemthemehelper import *
from .controls.husiconfont import *
from .controls.husqrcode import *
from .controls.husrectangle import *
from .controls.huswatermark import *
from .controls.huswindowagent import *
from .utils.logger import logger

QML_IMPORT_NAME = "HuskarUI.Basic"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlSingleton
class HusApp(QObject):
    """
    HusApp class.
    """

    def __init__(self, parent: QObject = None) -> None:
        super().__init__(parent = parent)
        
    @staticmethod
    def initialize(engine: QQmlEngine) -> None:
        """
        Initialize the HusApp class.
        """
        QFontDatabase.addApplicationFont(":/HuskarUI/resources/font/HuskarUI-Icons.ttf")
        
    @Slot(result = str)
    @staticmethod
    def libName() -> str:
        """
        Get the name of the HuskarUI library.
        """
        return pyhuskarui.__name__

    @Slot(result = str)
    @staticmethod
    def libVersion() -> str:
        """
        Get the version of the HuskarUI library.
        """
        return pyhuskarui.__version__