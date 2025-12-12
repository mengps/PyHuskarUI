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
import HuskarUI.Basic

HusText {
    id: control

    readonly property bool empty: iconSource === 0 || iconSource === ''
    property var iconSource: 0 ?? ''
    property alias iconSize: control.font.pixelSize
    property alias colorIcon: control.color
    property string contentDescription: text

    objectName: '__HusIconText__'
    width: __iconLoader.active ? (__iconLoader.implicitWidth + leftPadding + rightPadding) : implicitWidth
    height: __iconLoader.active ? (__iconLoader.implicitHeight + topPadding + bottomPadding) : implicitHeight
    text: __iconLoader.active ? '' : String.fromCharCode(iconSource)
    font {
        family: 'HuskarUI-Icons'
        pixelSize: parseInt(HusTheme.HusIconText.fontSize)
    }
    color: HusTheme.HusIconText.colorText

    Loader {
        id: __iconLoader
        anchors.centerIn: parent
        active: typeof iconSource == 'string' && iconSource !== ''
        sourceComponent: Image {
            source: control.iconSource
            width: control.iconSize
            height: control.iconSize
            sourceSize: Qt.size(width, height)
        }
    }

    Accessible.role: Accessible.Graphic
    Accessible.name: control.text
    Accessible.description: control.contentDescription
}
