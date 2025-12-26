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

T.CheckBox {
    id: control

    property bool animationEnabled: HusTheme.animationEnabled
    property bool effectEnabled: true
    property int hoverCursorShape: Qt.PointingHandCursor
    property int indicatorSize: 18
    property color colorText: enabled ? themeSource.colorText : themeSource.colorTextDisabled
    property color colorIndicator: {
        if (enabled) {
            return (checkState !== Qt.Unchecked) ? hovered ? themeSource.colorIndicatorCheckedHover :
                                                             themeSource.colorIndicatorChecked : themeSource.colorIndicator
        } else {
            return themeSource.colorIndicatorDisabled;
        }
    }
    property color colorIndicatorBorder: enabled ?
                                             (hovered || checked) ? themeSource.colorIndicatorBorderChecked :
                                                                    themeSource.colorIndicatorBorder : themeSource.colorIndicatorDisabled
    property HusRadius radiusIndicator: HusRadius { all: themeSource.radiusIndicator }
    property string contentDescription: ''
    property var themeSource: HusTheme.HusCheckBox

    Behavior on colorText { enabled: control.animationEnabled; ColorAnimation { duration: HusTheme.Primary.durationMid } }
    Behavior on colorIndicator { enabled: control.animationEnabled; ColorAnimation { duration: HusTheme.Primary.durationMid } }
    Behavior on colorIndicatorBorder { enabled: control.animationEnabled; ColorAnimation { duration: HusTheme.Primary.durationFast } }

    objectName: '__HusCheckBox__'
    implicitWidth: implicitContentWidth + leftPadding + rightPadding
    implicitHeight: Math.max(implicitContentHeight, implicitIndicatorHeight) + topPadding + bottomPadding
    font.family: themeSource.fontFamily
    font.pixelSize: parseInt(themeSource.fontSize)
    spacing: 6
    indicator: Item {
        x: control.leftPadding
        implicitWidth: __bg.width
        implicitHeight: __bg.height
        anchors.verticalCenter: parent.verticalCenter

        Rectangle {
            id: __effect
            width: __bg.width
            height: __bg.height
            radius: __bg.radius
            anchors.centerIn: parent
            visible: control.effectEnabled
            color: 'transparent'
            border.width: 0
            border.color: control.enabled ? control.themeSource.colorEffectBg : 'transparent'
            opacity: 0.2

            ParallelAnimation {
                id: __animation
                onFinished: __effect.border.width = 0;
                NumberAnimation {
                    target: __effect; property: 'width'; from: __bg.width + 2; to: __bg.width + 10;
                    duration: HusTheme.Primary.durationFast
                    easing.type: Easing.OutQuart
                }
                NumberAnimation {
                    target: __effect; property: 'height'; from: __bg.height + 2; to: __bg.height + 10;
                    duration: HusTheme.Primary.durationFast
                    easing.type: Easing.OutQuart
                }
                NumberAnimation {
                    target: __effect; property: 'opacity'; from: 0.1; to: 0;
                    duration: HusTheme.Primary.durationSlow
                }
            }

            Connections {
                target: control
                function onReleased() {
                    if (control.animationEnabled && control.effectEnabled) {
                        __effect.border.width = 6;
                        __animation.restart();
                    }
                }
            }
        }

        HusRectangleInternal {
            id: __bg
            width: control.indicatorSize
            height: control.indicatorSize
            radius: control.radiusIndicator.all
            topLeftRadius: control.radiusIndicator.topLeft
            topRightRadius: control.radiusIndicator.topRight
            bottomLeftRadius: control.radiusIndicator.bottomLeft
            bottomRightRadius: control.radiusIndicator.bottomRight
            color: 'transparent'
            border.color: control.colorIndicatorBorder
            border.width: 1
            anchors.centerIn: parent

            /*! 勾选背景 */
            HusRectangleInternal {
                id: __checkedBg
                anchors.fill: parent
                color: control.colorIndicator
                visible: opacity > 0
                opacity: enabled ? (control.checkState === Qt.Checked ? 1 : 0) : 1
                radius: parent.radius - 1
                topLeftRadius: Math.max(0, parent.topLeftRadius - 1)
                topRightRadius: Math.max(0, parent.topRightRadius - 1)
                bottomLeftRadius: Math.max(0, parent.bottomLeftRadius - 1)
                bottomRightRadius: Math.max(0, parent.bottomRightRadius - 1)

                Behavior on opacity {
                    enabled: control.animationEnabled
                    NumberAnimation { duration: HusTheme.Primary.durationFast }
                }
            }

            /*! 勾选标记 */
            Item {
                id: __checkMarkContainer
                anchors.centerIn: parent
                width: parent.width * 0.6
                height: parent.height * 0.6
                visible: opacity > 0
                scale: control.checkState === Qt.Checked ? 1.1 : 0.2
                opacity: control.checkState === Qt.Checked ? 1.0 : 0.0

                Behavior on scale {
                    enabled: control.animationEnabled && __checkMark.animationEnabled
                    NumberAnimation { easing.overshoot: 2.5; easing.type: Easing.OutBack; duration: HusTheme.Primary.durationSlow }
                }

                Behavior on opacity {
                    enabled: control.animationEnabled && __checkMark.animationEnabled
                    NumberAnimation { duration: HusTheme.Primary.durationFast }
                }

                Canvas {
                    id: __checkMark
                    anchors.fill: parent
                    visible: control.checkState === Qt.Checked

                    property bool animationEnabled: false
                    property real animationProgress: control.checkState === Qt.Checked ? 1 : 0
                    property real lineWidth: 2
                    property color checkColor: control.enabled ? '#fff' : control.themeSource.colorIndicatorDisabled

                    onAnimationProgressChanged: requestPaint();
                    onCheckColorChanged: requestPaint();
                    onVisibleChanged: requestPaint();
                    Component.onCompleted: animationEnabled = true;

                    onPaint: {
                        const ctx = getContext('2d');
                        ctx.clearRect(0, 0, width, height);

                        ctx.lineWidth = lineWidth;
                        ctx.strokeStyle = checkColor;
                        ctx.fillStyle = 'transparent';
                        ctx.lineCap = 'round';
                        ctx.lineJoin = 'round';

                        const startX = width * 0.2;
                        const midPointX = width * 0.4;
                        const endX = width * 0.8;
                        const midPointY = height * 0.75;
                        const startY = height * 0.5;
                        const endY = height * 0.2;

                        ctx.beginPath();

                        if (animationProgress > 0) {
                            ctx.moveTo(startX, startY);
                            if (animationProgress < 0.5) {
                                const currentX = startX + (midPointX - startX) * (animationProgress * 2);
                                const currentY = startY + (midPointY - startY) * (animationProgress * 2);
                                ctx.lineTo(currentX, currentY);
                            } else {
                                const t = (animationProgress - 0.5) * 2;
                                const currentX = midPointX + (endX - midPointX) * t;
                                const currentY = midPointY + (endY - midPointY) * t;
                                ctx.lineTo(midPointX, midPointY);
                                ctx.lineTo(currentX, currentY);
                            }
                        }

                        ctx.stroke();
                    }

                    Behavior on animationProgress {
                        enabled: control.animationEnabled && __checkMark.animationEnabled
                        NumberAnimation {
                            duration: HusTheme.Primary.durationSlow
                            easing.type: Easing.OutCubic
                        }
                    }
                }
            }

            /*! 部分选择状态 */
            Rectangle {
                id: __partialCheckMark
                x: (parent.width - width) / 2
                y: (parent.height - height) / 2
                width: parent.width * 0.5
                height: parent.height * 0.5
                color: control.colorIndicator
                visible: control.checkState === Qt.PartiallyChecked
                radius: parent.radius * 0.5

                Behavior on opacity {
                    enabled: control.animationEnabled && __checkMark.animationEnabled
                    NumberAnimation { duration: HusTheme.Primary.durationFast }
                }
            }
        }
    }
    contentItem: HusText {
        text: control.text
        font: control.font
        color: control.colorText
        verticalAlignment: Text.AlignVCenter
        leftPadding: control.indicator.width + (text.length > 0 ? control.spacing : 0)

        Behavior on color {
            enabled: control.animationEnabled
            ColorAnimation { duration: HusTheme.Primary.durationMid }
        }
    }
    background: Item { }

    HoverHandler {
        cursorShape: control.hoverCursorShape
    }

    Accessible.role: Accessible.CheckBox
    Accessible.name: control.text
    Accessible.description: control.contentDescription
    Accessible.onPressAction: control.clicked();
}
