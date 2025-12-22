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
import QtQuick.Shapes
import HuskarUI.Basic

Item {
    id: control

    enum Align
    {
        Align_Left = 0,
        Align_Center = 1,
        Align_Right = 2
    }

    enum Style
    {
        SolidLine = 0,
        DashLine = 1
    }

    property bool animationEnabled: HusTheme.animationEnabled
    property string title: ''
    property font titleFont: Qt.font({
                                         family: HusTheme.HusDivider.fontFamily,
                                         pixelSize: parseInt(HusTheme.HusDivider.fontSize)
                                     })
    property int titleAlign: HusDivider.Align_Left
    property int titlePadding: 20
    property int lineStyle: HusDivider.SolidLine
    property int lineWidth: 1
    property list<real> dashPattern: [4, 2]
    property int orientation: Qt.Horizontal
    property color colorText: HusTheme.HusDivider.colorText
    property color colorSplit: HusTheme.HusDivider.colorSplit
    property Component titleDelegate: HusText {
        text: control.title
        font: control.titleFont
        color: control.colorText
    }
    property Component splitDelegate: Shape {
        id: __shape

        property real lineX: __titleLoader.x + __titleLoader.implicitWidth * 0.5
        property real lineY: __titleLoader.y + __titleLoader.implicitHeight * 0.5

        ShapePath {
            strokeStyle: control.lineStyle === HusDivider.SolidLine ? ShapePath.SolidLine : ShapePath.DashLine
            strokeColor: control.colorSplit
            strokeWidth: control.lineWidth
            dashPattern: control.dashPattern
            fillColor: 'transparent'
            startX: control.orientation === Qt.Horizontal ? 0 : __shape.lineX
            startY: control.orientation === Qt.Horizontal ? __shape.lineY : 0

            PathLine {
                x: {
                    if (control.orientation === Qt.Horizontal) {
                        return control.title === '' ? 0 : __titleLoader.x - 10;
                    } else {
                        return __shape.lineX;
                    }
                }
                y: control.orientation === Qt.Horizontal ? __shape.lineY : __titleLoader.y - 10
            }
        }

        ShapePath {
            strokeStyle: control.lineStyle === HusDivider.SolidLine ? ShapePath.SolidLine : ShapePath.DashLine
            strokeColor: control.colorSplit
            strokeWidth: control.lineWidth
            dashPattern: control.dashPattern
            fillColor: 'transparent'
            startX: {
                if (control.orientation === Qt.Horizontal) {
                    return control.title === '' ? 0 : (__titleLoader.x + __titleLoader.implicitWidth + 10);
                } else {
                    return __shape.lineX;
                }
            }
            startY: {
                if (control.orientation === Qt.Horizontal) {
                    return __shape.lineY;
                } else {
                    return control.title === '' ? 0 : (__titleLoader.y + __titleLoader.implicitHeight + 10);
                }
            }

            PathLine {
                x: control.orientation === Qt.Horizontal ?  control.width : __shape.lineX
                y: control.orientation === Qt.Horizontal ? __shape.lineY : control.height
            }
        }
    }
    property string contentDescription: title

    objectName: '__HusDivider__'

    Behavior on colorSplit { enabled: control.animationEnabled; ColorAnimation { duration: HusTheme.Primary.durationFast } }
    Behavior on colorText { enabled: control.animationEnabled; ColorAnimation { duration: HusTheme.Primary.durationFast } }

    Loader {
        id: __splitLoader
        sourceComponent: control.splitDelegate
    }

    Loader {
        id: __titleLoader
        z: 1
        anchors.top: (control.orientation !== Qt.Horizontal && control.titleAlign === HusDivider.Align_Left) ? parent.top : undefined
        anchors.topMargin: (control.orientation !== Qt.Horizontal && control.titleAlign === HusDivider.Align_Left) ? control.titlePadding : 0
        anchors.bottom: (control.orientation !== Qt.Horizontal && control.titleAlign === HusDivider.Align_Right) ? parent.right : undefined
        anchors.bottomMargin: (control.orientation !== Qt.Horizontal && control.titleAlign === HusDivider.Align_Right) ? control.titlePadding : 0
        anchors.left: (control.orientation === Qt.Horizontal && control.titleAlign === HusDivider.Align_Left) ? parent.left : undefined
        anchors.leftMargin: (control.orientation === Qt.Horizontal && control.titleAlign === HusDivider.Align_Left) ? control.titlePadding : 0
        anchors.right: (control.orientation === Qt.Horizontal && control.titleAlign === HusDivider.Align_Right) ? parent.right : undefined
        anchors.rightMargin: (control.orientation === Qt.Horizontal && control.titleAlign === HusDivider.Align_Right) ? control.titlePadding : 0
        anchors.horizontalCenter: (control.orientation !== Qt.Horizontal || control.titleAlign === HusDivider.Align_Center) ? parent.horizontalCenter : undefined
        anchors.verticalCenter: (control.orientation === Qt.Horizontal || control.titleAlign === HusDivider.Align_Center) ? parent.verticalCenter : undefined
        sourceComponent: control.titleDelegate
    }

    Accessible.role: Accessible.Separator
    Accessible.name: control.title
    Accessible.description: control.contentDescription
}
