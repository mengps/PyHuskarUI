/*
 * PyHuskarUI
 *
 * Copyright (C) 2025 mengps (MenPenS)
 * https://github.com/mengps/PyHuskarUI
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import QtQuick
import QtQuick.Templates as T
import HuskarUI.Basic

T.Frame {
    id: control

    property real borderWidth: 1
    property color colorBg: 'transparent'
    property color colorBorder: HusTheme.Primary.colorSplit
    property HusRadius radiusBg: HusRadius { all: HusTheme.Primary.radiusPrimary }

    objectName: '__HusFrame__'
    implicitWidth: Math.max(implicitBackgroundWidth + leftInset + rightInset,
                            contentWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset,
                             contentHeight + topPadding + bottomPadding)
    padding: 5
    font {
        family: HusTheme.Primary.fontPrimaryFamily
        pixelSize: parseInt(HusTheme.Primary.fontPrimarySize)
    }
    background: HusRectangleInternal {
        radius: control.radiusBg.all
        topLeftRadius: control.radiusBg.topLeft
        topRightRadius: control.radiusBg.topRight
        bottomLeftRadius: control.radiusBg.bottomLeft
        bottomRightRadius: control.radiusBg.bottomRight
        color: control.colorBg
        border.color: control.colorBorder
        border.width: control.borderWidth
    }
}
