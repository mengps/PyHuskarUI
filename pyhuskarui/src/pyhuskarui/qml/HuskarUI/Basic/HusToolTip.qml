/*
 * PyHuskarUI
 *
 * Copyright (C) 2026 mengps (MenPenS)
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

T.ToolTip {
    id: control

    enum Position
    {
        Position_Top = 0,
        Position_Bottom = 1,
        Position_Left = 2,
        Position_Right = 3
    }

    property bool animationEnabled: HusTheme.animationEnabled
    property bool showArrow: false
    property int position: HusToolTip.Position_Top
    property color colorShadow: HusTheme.HusToolTip.colorShadow
    property color colorText: HusTheme.HusToolTip.colorText
    property color colorBg: HusTheme.isDark ? HusTheme.HusToolTip.colorBgDark : HusTheme.HusToolTip.colorBg
    property HusRadius radiusBg: HusRadius { all: HusTheme.HusToolTip.radiusBg }
    property HusBorder borderBg: HusBorder { color: 'transparent' }

    component Arrow: Canvas {
        onWidthChanged: requestPaint();
        onHeightChanged: requestPaint();
        onColorBgChanged: requestPaint();
        onPaint: {
            const ctx = getContext('2d');
            ctx.fillStyle = colorBg;
            ctx.beginPath();
            switch (position) {
            case HusToolTip.Position_Top: {
                ctx.moveTo(0, 0);
                ctx.lineTo(width, 0);
                ctx.lineTo(width * 0.5, height);
            } break;
            case HusToolTip.Position_Bottom: {
                ctx.moveTo(0, height);
                ctx.lineTo(width, height);
                ctx.lineTo(width * 0.5, 0);
            } break;
            case HusToolTip.Position_Left: {
                ctx.moveTo(0, 0);
                ctx.lineTo(0, height);
                ctx.lineTo(width, height * 0.5);
            } break;
            case HusToolTip.Position_Right: {
                ctx.moveTo(width, 0);
                ctx.lineTo(width, height);
                ctx.lineTo(0, height * 0.5);
            } break;
            }
            ctx.closePath();
            ctx.fill();
        }
        property color colorBg: control.colorBg
    }

    x: {
        switch (position) {
        case HusToolTip.Position_Top:
        case HusToolTip.Position_Bottom:
            return (__private.controlParentWidth - implicitWidth) * 0.5;
        case HusToolTip.Position_Left:
            return -implicitWidth - 4;
        case HusToolTip.Position_Right:
            return __private.controlParentWidth + 4;
        }
    }
    y: {
        switch (position) {
        case HusToolTip.Position_Top:
            return -implicitHeight - 4 - (showArrow ? __private.arrowSize.height : 0);
        case HusToolTip.Position_Bottom:
            return __private.controlParentHeight + 4 + (showArrow ? __private.arrowSize.height : 0);
        case HusToolTip.Position_Left:
        case HusToolTip.Position_Right:
            return (__private.controlParentHeight - implicitHeight) * 0.5;
        }
    }

    objectName: '__HusToolTip__'
    implicitWidth: Math.max(implicitBackgroundWidth + leftInset + rightInset,
                            contentWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset,
                             contentHeight + topPadding + bottomPadding)
    delay: 500
    padding: 6
    font {
        family: HusTheme.HusToolTip.fontFamily
        pixelSize: parseInt(HusTheme.HusToolTip.fontSize)
    }
    enter: Transition {
        NumberAnimation { property: 'opacity'; from: 0.0; to: 1.0; duration: control.animationEnabled ? HusTheme.Primary.durationMid : 0 }
    }
    exit: Transition {
        NumberAnimation { property: 'opacity'; from: 1.0; to: 0.0; duration: control.animationEnabled ? HusTheme.Primary.durationMid : 0 }
    }
    closePolicy: T.Popup.CloseOnEscape | T.Popup.CloseOnPressOutsideParent | T.Popup.CloseOnReleaseOutsideParent
    contentItem: HusText {
        text: control.text
        font: control.font
        color: control.colorText
        wrapMode: Text.Wrap
    }
    background: Item {
        id: __bg

        HusShadow {
            anchors.fill: __item
            source: __item
            shadowColor: control.colorShadow
        }

        Item {
            id: __item
            width: parent.width + (__private.isHorizontal ? 0 : __arrow.width)
            height: parent.height + (__private.isHorizontal ? __arrow.height : 0)

            Arrow {
                id: __arrow
                x: __private.isHorizontal ? (-control.x + (__private.controlParentWidth - width) * 0.5) : 0
                y: __private.isHorizontal ? 0 : (-control.y + (__private.controlParentHeight - height)) * 0.5
                width: __private.arrowSize.width
                height: __private.arrowSize.height
                anchors.top: control.position == HusToolTip.Position_Bottom ? parent.top : undefined
                anchors.bottom: control.position == HusToolTip.Position_Top ? parent.bottom : undefined
                anchors.left: control.position == HusToolTip.Position_Right ? parent.left : undefined
                anchors.right: control.position == HusToolTip.Position_Left ? parent.right : undefined

                Connections {
                    target: control
                    function onPositionChanged() {
                        __arrow.requestPaint();
                    }
                }
            }

            HusRectangleInternal {
                width: __bg.width
                height: __bg.height
                color: control.colorBg
                border.width: control.borderBg.width
                border.color: control.borderBg.color
                border.pixelAligned: control.borderBg.pixelAligned
                radius: control.radiusBg.all
                topLeftRadius: control.radiusBg.topLeft
                topRightRadius: control.radiusBg.topRight
                bottomLeftRadius: control.radiusBg.bottomLeft
                bottomRightRadius: control.radiusBg.bottomRight
            }
        }
    }

    QtObject {
        id: __private
        property bool isHorizontal: control.position === HusToolTip.Position_Top || control.position === HusToolTip.Position_Bottom
        property size arrowSize: control.showArrow ? (isHorizontal ? Qt.size(12, 6) : Qt.size(6, 12)) : Qt.size(0, 0)
        property real controlParentWidth: control.parent ? control.parent.width : 0
        property real controlParentHeight: control.parent ? control.parent.height : 0
    }
}
