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
import QtQuick.Layouts
import HuskarUI.Basic

T.Control {
    id: control

    property bool animationEnabled: HusTheme.animationEnabled
    property string title: ''
    property string coverSource: ''
    property int coverFillMode: Image.Stretch
    property real borderWidth: 1
    property int bodyAvatarSize: 40
    property var bodyAvatarIcon: 0 ?? ''
    property string bodyAvatarSource: ''
    property string bodyAvatarText: ''
    property string bodyTitle: ''
    property string bodyDescription: ''
    property font titleFont: Qt.font({
                                         family: themeSource.fontFamily,
                                         pixelSize: parseInt(themeSource.fontSizeTitle),
                                         weight: Font.DemiBold,
                                     })
    property font bodyTitleFont: Qt.font({
                                             family: themeSource.fontFamily,
                                             pixelSize: parseInt(themeSource.fontSizeBodyTitle),
                                             weight: Font.DemiBold,
                                         })
    property font bodyDescriptionFont: Qt.font({
                                                   family: themeSource.fontFamily,
                                                   pixelSize: parseInt(themeSource.fontSizeBodyDescription),
                                               })
    property color colorTitle: themeSource.colorTitle
    property color colorBg: themeSource.colorBg
    property color colorBorder: themeSource.colorBorder
    property color colorBodyAvatar: themeSource.colorBodyAvatar
    property color colorBodyAvatarBg: 'transparent'
    property color colorBodyTitle: themeSource.colorBodyTitle
    property color colorBodyDescription: themeSource.colorBodyDescription
    property HusRadius radiusBg: HusRadius { all: themeSource.radiusBg }
    property var themeSource: HusTheme.HusCard

    property Component titleDelegate: Item {
        height: 60

        RowLayout {
            anchors.fill: parent
            anchors.topMargin: 5
            anchors.bottomMargin: 5
            anchors.leftMargin: 15
            anchors.rightMargin: 15

            HusText {
                Layout.fillWidth: true
                Layout.fillHeight: true
                text: control.title
                font: control.titleFont
                color: control.colorTitle
                wrapMode: Text.WrapAnywhere
                verticalAlignment: Text.AlignVCenter
            }

            Loader {
                Layout.alignment: Qt.AlignVCenter
                sourceComponent: extraDelegate
            }
        }

        HusDivider {
            width: parent.width;
            height: 1
            anchors.bottom: parent.bottom
            animationEnabled: control.animationEnabled
            visible: control.coverSource == ''
        }
    }
    property Component extraDelegate: Item { }
    property Component coverDelegate: Image {
        height: control.coverSource == '' ? 0 : 180
        source: control.coverSource
        fillMode: control.coverFillMode
    }
    property Component bodyDelegate: Item {
        height: 100

        RowLayout {
            anchors.fill: parent

            Item {
                Layout.preferredWidth: __avatar.visible ? 70 : 0
                Layout.fillHeight: true

                HusAvatar {
                    id: __avatar
                    size: control.bodyAvatarSize
                    anchors.centerIn: parent
                    colorBg: control.colorBodyAvatarBg
                    iconSource: control.bodyAvatarIcon
                    imageSource: control.bodyAvatarSource
                    textSource: control.bodyAvatarText
                    colorIcon: control.colorBodyAvatar
                    colorText: control.colorBodyAvatar
                    visible: !((iconSource === 0 || iconSource === '') && imageSource === '' && textSource === '')
                }
            }

            ColumnLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true

                HusText {
                    Layout.fillWidth: true
                    leftPadding: __avatar.visible ? 0 : 15
                    rightPadding: 15
                    text: control.bodyTitle
                    font: control.bodyTitleFont
                    color: control.colorBodyTitle
                    wrapMode: Text.WrapAnywhere
                    visible: control.bodyTitle != ''
                }

                HusText {
                    Layout.fillWidth: true
                    leftPadding: __avatar.visible ? 0 : 15
                    rightPadding: 15
                    text: control.bodyDescription
                    font: control.bodyDescriptionFont
                    color: control.colorBodyDescription
                    wrapMode: Text.WrapAnywhere
                    visible: control.bodyDescription != ''
                }
            }
        }
    }
    property Component actionDelegate: Item { }

    objectName: '__HusCard__'
    width: 300
    implicitWidth: Math.max(implicitBackgroundWidth + leftInset + rightInset,
                            implicitContentWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset,
                             implicitContentHeight + topPadding + bottomPadding)
    clip: true
    contentItem: Column {
        Loader {
            width: parent.width
            sourceComponent: control.titleDelegate
        }

        Loader {
            width: parent.width - 2
            anchors.horizontalCenter: parent.horizontalCenter
            sourceComponent: control.coverDelegate
        }

        Loader {
            width: parent.width - 2
            anchors.horizontalCenter: parent.horizontalCenter
            sourceComponent: control.bodyDelegate
        }

        Loader {
            width: parent.width
            sourceComponent: control.actionDelegate
        }
    }
    background: HusRectangleInternal {
        color: control.colorBg
        border.color: control.colorBorder
        border.width: control.borderWidth
        radius: control.radiusBg.all
        topLeftRadius: control.radiusBg.topLeft
        topRightRadius: control.radiusBg.topRight
        bottomLeftRadius: control.radiusBg.bottomLeft
        bottomRightRadius: control.radiusBg.bottomRight

        Behavior on color { enabled: control.animationEnabled; ColorAnimation { duration: HusTheme.Primary.durationMid } }
    }
}
