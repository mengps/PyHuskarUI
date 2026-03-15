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

T.ScrollBar {
    id: control

    property bool animationEnabled: HusTheme.animationEnabled
    property int minimumHandleSize: 24
    property color colorBar: control.pressed ? HusTheme.HusScrollBar.colorBarActive :
                                               control.hovered ? HusTheme.HusScrollBar.colorBarHover :
                                                                 HusTheme.HusScrollBar.colorBar
    property color colorBg: control.pressed ? HusTheme.HusScrollBar.colorBgActive :
                                              control.hovered ? HusTheme.HusScrollBar.colorBgHover :
                                                                HusTheme.HusScrollBar.colorBg
    property string contentDescription: ''

    objectName: '__HusScrollBar__'
    implicitWidth: Math.max(implicitBackgroundWidth + leftInset + rightInset,
                            implicitContentWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset,
                             implicitContentHeight + topPadding + bottomPadding)
    leftPadding: control.orientation === Qt.Horizontal ? 10 : 2
    rightPadding: control.orientation === Qt.Horizontal ? 10 : 2
    topPadding: control.orientation === Qt.Vertical ? 10 : 2
    bottomPadding: control.orientation === Qt.Vertical ? 10 : 2
    policy: T.ScrollBar.AlwaysOn
    minimumSize: {
        if (control.orientation === Qt.Vertical)
            return size * height < minimumHandleSize ? minimumHandleSize / height : 0;
        else
            return size * width < minimumHandleSize ? minimumHandleSize / width : 0;
    }
    visible: (control.policy != T.ScrollBar.AlwaysOff) && control.size !== 1
    contentItem: Rectangle {
        implicitWidth: control.interactive && __private.visible ? 6 : 2
        implicitHeight: control.interactive && __private.visible ? 6 : 2
        radius: control.orientation === Qt.Vertical ? width * 0.5 : height * 0.5
        color: control.colorBar
        opacity: {
            if (control.policy === T.ScrollBar.AlwaysOn) {
                return 1;
            } else if (control.policy === T.ScrollBar.AsNeeded) {
                return __private.visible ? 1 : 0;
            } else {
                return 0;
            }
        }

        Behavior on implicitWidth { enabled: control.animationEnabled; NumberAnimation { duration: HusTheme.Primary.durationFast } }
        Behavior on implicitHeight { enabled: control.animationEnabled; NumberAnimation { duration: HusTheme.Primary.durationFast } }
        Behavior on opacity { enabled: control.animationEnabled; NumberAnimation { duration: HusTheme.Primary.durationFast } }
        Behavior on color { enabled: control.animationEnabled; ColorAnimation { duration: HusTheme.Primary.durationFast } }
    }
    background: Rectangle {
        color: control.colorBg
        opacity: __private.visible ? 1 : 0

        Behavior on opacity { enabled: control.animationEnabled; NumberAnimation { duration: HusTheme.Primary.durationFast } }

        Loader {
            active: control.orientation === Qt.Vertical
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            sourceComponent: HoverIcon {
                iconSize: 10
                iconSource: HusIcon.CaretUpOutlined
                onClicked: control.decrease();
            }
        }

        Loader {
            active: control.orientation === Qt.Vertical
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.bottom
            sourceComponent: HoverIcon {
                iconSize: 10
                iconSource: HusIcon.CaretDownOutlined
                onClicked: control.increase();
            }
        }

        Loader {
            active: control.orientation === Qt.Horizontal
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            sourceComponent: HoverIcon {
                iconSize: 10
                iconSource: HusIcon.CaretLeftOutlined
                onClicked: control.decrease();
            }
        }

        Loader {
            active: control.orientation === Qt.Horizontal
            anchors.verticalCenter: parent.verticalCenter
            anchors.right: parent.right
            sourceComponent: HoverIcon {
                iconSize: 10
                iconSource: HusIcon.CaretRightOutlined
                onClicked: control.increase();
            }
        }
    }

    onHoveredChanged: {
        if (hovered) {
            __exitTimer.stop();
            __private.exit = false;
        } else {
            __exitTimer.restart();
        }
    }

    component HoverIcon: HusIconText {
        signal clicked()
        property bool hovered: false

        colorIcon: hovered ? HusTheme.HusScrollBar.colorIconHover : HusTheme.HusScrollBar.colorIcon
        opacity: __private.visible ? 1 : 0

        Behavior on opacity { enabled: control.animationEnabled; NumberAnimation { duration: HusTheme.Primary.durationFast } }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            onEntered: parent.hovered = true;
            onExited: parent.hovered = false;
            onClicked: parent.clicked();
        }
    }

    QtObject {
        id: __private
        property bool visible: control.hovered || control.pressed || !exit
        property bool exit: true
    }

    Timer {
        id: __exitTimer
        interval: 800
        onTriggered: __private.exit = true;
    }

    Accessible.role: Accessible.ScrollBar
    Accessible.description: control.contentDescription
}
