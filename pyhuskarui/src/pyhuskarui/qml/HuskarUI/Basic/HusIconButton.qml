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
import QtQuick.Layouts
import HuskarUI.Basic

HusButton {
    id: control

    enum IconPosition {
        Position_Start = 0,
        Position_End = 1
    }

    property bool loading: false
    property var iconSource: 0 ?? ''
    property int iconSize: parseInt(themeSource.fontSize)
    property int iconSpacing: 5 * sizeRatio
    property int iconPosition: HusIconButton.Position_Start
    property int orientation: Qt.Horizontal
    property font iconFont: Qt.font({
                                        family: 'HuskarUI-Icons',
                                        pixelSize: iconSize
                                    })
    property color colorIcon: colorText

    property Component iconDelegate: HusIconText {
        font: control.iconFont
        color: control.colorIcon
        iconSize: control.iconSize
        iconSource: control.loading ? HusIcon.LoadingOutlined : control.iconSource
        verticalAlignment: Text.AlignVCenter
        visible: !empty

        Behavior on color { enabled: control.animationEnabled; ColorAnimation { duration: HusTheme.Primary.durationFast } }

        NumberAnimation on rotation {
            running: control.loading
            from: 0
            to: 360
            loops: Animation.Infinite
            duration: 1000
        }
    }

    objectName: '__HusIconButton__'
    contentItem: Item {
        implicitWidth: control.orientation === Qt.Horizontal ? __horLoader.implicitWidth : __verLoader.implicitWidth
        implicitHeight: control.orientation === Qt.Horizontal ? __horLoader.implicitHeight : __verLoader.implicitHeight

        Behavior on implicitWidth { enabled: control.animationEnabled; NumberAnimation { duration: HusTheme.Primary.durationMid } }
        Behavior on implicitHeight { enabled: control.animationEnabled; NumberAnimation { duration: HusTheme.Primary.durationMid } }

        Loader {
            id: __horLoader
            anchors.centerIn: parent
            active: control.orientation === Qt.Horizontal
            sourceComponent: Row {
                spacing: control.iconSpacing
                layoutDirection: control.iconPosition === HusIconButton.Position_Start ? Qt.LeftToRight : Qt.RightToLeft

                Loader {
                    id: __hIcon
                    height: Math.max(__hIcon.implicitHeight, __hText.implicitHeight)
                    anchors.verticalCenter: parent.verticalCenter
                    sourceComponent: control.iconDelegate
                }

                HusText {
                    id: __hText
                    anchors.verticalCenter: parent.verticalCenter
                    text: control.text
                    font: control.font
                    lineHeight: HusTheme.HusButton.fontLineHeight
                    color: control.colorText
                    elide: Text.ElideRight
                    visible: text !== ''

                    Behavior on color { enabled: control.animationEnabled; ColorAnimation { duration: HusTheme.Primary.durationFast } }
                }
            }
        }

        Loader {
            id: __verLoader
            active: control.orientation === Qt.Vertical
            anchors.centerIn: parent
            sourceComponent: Column {
                spacing: control.iconSpacing
                Component.onCompleted: relayout();

                function relayout() {
                    if (control.iconPosition === HusIconButton.Position_Start) {
                        children = [__vIcon, __vText];
                    } else {
                        children = [__vText, __vIcon];
                    }
                }

                Loader {
                    id: __vIcon
                    height: Math.max(__vIcon.implicitHeight, __vText.implicitHeight)
                    anchors.horizontalCenter: parent.horizontalCenter
                    sourceComponent: control.iconDelegate
                }

                HusText {
                    id: __vText
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: control.text
                    font: control.font
                    lineHeight: HusTheme.HusButton.fontLineHeight
                    color: control.colorText
                    elide: Text.ElideRight
                    visible: text !== ''

                    Behavior on color { enabled: control.animationEnabled; ColorAnimation { duration: HusTheme.Primary.durationFast } }
                }
            }
        }
    }
}
