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

from PySide6.QtCore import QObject, QUrl, Slot
from PySide6.QtGui import QFontDatabase
from PySide6.QtQml import QQmlEngine, QmlElement, QmlSingleton, qmlRegisterType

import huskarui

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
from .controls.husrectangle import *
from .controls.huswatermark import *
from .controls.huswindowagent import *

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
    def _registerTypes(uri: str, version_major: int, version_minor: int) -> None:
        """
        Register all the custom components.
        """
        
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusAcrylic.qml"), uri, version_major, version_minor, "HusAcrylic")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusAutoComplete.qml"), uri, version_major, version_minor, "HusAutoComplete")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusAvatar.qml"), uri, version_major, version_minor, "HusAvatar")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusBadge.qml"), uri, version_major, version_minor, "HusBadge")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusBreadcrumb.qml"), uri, version_major, version_minor, "HusBreadcrumb")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusButton.qml"), uri, version_major, version_minor, "HusButton")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusButtonBlock.qml"), uri, version_major, version_minor, "HusButtonBlock")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusCaptionBar.qml"), uri, version_major, version_minor, "HusCaptionBar")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusCaptionButton.qml"), uri, version_major, version_minor, "HusCaptionButton")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusCard.qml"), uri, version_major, version_minor, "HusCard")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusCarousel.qml"), uri, version_major, version_minor, "HusCarousel")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusCheckBox.qml"), uri, version_major, version_minor, "HusCheckBox")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusCollapse.qml"), uri, version_major, version_minor, "HusCollapse")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusContextMenu.qml"), uri, version_major, version_minor, "HusContextMenu")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusCopyableText.qml"), uri, version_major, version_minor, "HusCopyableText")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusDateTimePicker.qml"), uri, version_major, version_minor, "HusDateTimePicker")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusDivider.qml"), uri, version_major, version_minor, "HusDivider")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusDrawer.qml"), uri, version_major, version_minor, "HusDrawer")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusIconButton.qml"), uri, version_major, version_minor, "HusIconButton")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusIconText.qml"), uri, version_major, version_minor, "HusIconText")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusImage.qml"), uri, version_major, version_minor, "HusImage")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusImagePreview.qml"), uri, version_major, version_minor, "HusImagePreview")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusInput.qml"), uri, version_major, version_minor, "HusInput")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusInputNumber.qml"), uri, version_major, version_minor, "HusInputNumber")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusMenu.qml"), uri, version_major, version_minor, "HusMenu")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusMessage.qml"), uri, version_major, version_minor, "HusMessage")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusModal.qml"), uri, version_major, version_minor, "HusModal")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusMoveMouseArea.qml"), uri, version_major, version_minor, "HusMoveMouseArea")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusMultiSelect.qml"), uri, version_major, version_minor, "HusMultiSelect")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusNotification.qml"), uri, version_major, version_minor, "HusNotification")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusOTPInput.qml"), uri, version_major, version_minor, "HusOTPInput")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusPagination.qml"), uri, version_major, version_minor, "HusPagination")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusPopconfirm.qml"), uri, version_major, version_minor, "HusPopconfirm")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusPopup.qml"), uri, version_major, version_minor, "HusPopup")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusProgress.qml"), uri, version_major, version_minor, "HusProgress")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusRadio.qml"), uri, version_major, version_minor, "HusRadio")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusRadioBlock.qml"), uri, version_major, version_minor, "HusRadioBlock")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusRate.qml"), uri, version_major, version_minor, "HusRate")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusResizeMouseArea.qml"), uri, version_major, version_minor, "HusResizeMouseArea")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusScrollBar.qml"), uri, version_major, version_minor, "HusScrollBar")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusSelect.qml"), uri, version_major, version_minor, "HusSelect")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusShadow.qml"), uri, version_major, version_minor, "HusShadow")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusSlider.qml"), uri, version_major, version_minor, "HusSlider")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusSwitch.qml"), uri, version_major, version_minor, "HusSwitch")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusSwitchEffect.qml"), uri, version_major, version_minor, "HusSwitchEffect")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusTableView.qml"), uri, version_major, version_minor, "HusTableView")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusTabView.qml"), uri, version_major, version_minor, "HusTabView")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusTag.qml"), uri, version_major, version_minor, "HusTag")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusText.qml"), uri, version_major, version_minor, "HusText")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusTextArea.qml"), uri, version_major, version_minor, "HusTextArea")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusTimeline.qml"), uri, version_major, version_minor, "HusTimeline")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusToolTip.qml"), uri, version_major, version_minor, "HusToolTip")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusTourFocus.qml"), uri, version_major, version_minor, "HusTourFocus")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusTourStep.qml"), uri, version_major, version_minor, "HusTourStep")
        qmlRegisterType(QUrl("qrc:/HuskarUI/imports/HusWindow.qml"), uri, version_major, version_minor, "HusWindow")

    @staticmethod
    def initialize(engine: QQmlEngine) -> None:
        """
        Initialize the HusApp class.
        """
        QFontDatabase.addApplicationFont(":/HuskarUI/resources/font/HuskarUI-Icons.ttf")
        
        HusApp._registerTypes("HuskarUI.Basic", QML_IMPORT_MAJOR_VERSION, 0)

    @Slot(result = str)
    @staticmethod
    def libVersion() -> str:
        """
        Get the version of the HuskarUI library.
        """
        return huskarui.__version__