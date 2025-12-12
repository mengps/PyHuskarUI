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

AnimatedImage {
    id: control

    property bool animationEnabled: HusTheme.animationEnabled
    property bool previewEnabled: true
    readonly property alias hovered: __hoverHandler.hovered
    property int hoverCursorShape: Qt.PointingHandCursor
    property string fallback: ''
    property string placeholder: ''
    property var items: []

    objectName: '__HusAnimatedImage__'
    onSourceChanged: {
        if (items.length == 0) {
            __private.previewItems = [{ url: source }];
        }
    }
    onItemsChanged: {
        if (items.length > 0) {
            __private.previewItems = [...items];
        }
    }

    QtObject {
        id: __private
        property var previewItems: []
    }

    Loader {
        anchors.centerIn: parent
        active: control.status === Image.Error && control.fallback !== ''
        sourceComponent: Image {
            source: control.fallback
            Component.onCompleted: {
                __private.previewItems = [{ url: control.fallback }]
            }
        }
    }

    Loader {
        anchors.centerIn: parent
        active: control.status === Image.Loading && control.placeholder !== ''
        sourceComponent: Image {
            source: control.placeholder
        }
    }

    Loader {
        anchors.fill: parent
        active: control.previewEnabled
        sourceComponent: Rectangle {
            color: HusTheme.Primary.colorTextTertiary
            opacity: control.hovered ? 1.0 : 0.0

            Behavior on color { enabled: control.animationEnabled; ColorAnimation { duration: HusTheme.Primary.durationMid } }
            Behavior on opacity { enabled: control.animationEnabled; NumberAnimation { duration: HusTheme.Primary.durationMid } }

            Row {
                anchors.centerIn: parent
                spacing: 5

                HusIconText {
                    anchors.verticalCenter: parent.verticalCenter
                    colorIcon: HusTheme.HusImage.colorText
                    iconSource: HusIcon.EyeOutlined
                    iconSize: parseInt(HusTheme.HusImage.fontSize) + 2
                }

                HusText {
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr('预览')
                    color: HusTheme.HusImage.colorText
                }
            }

            HusImagePreview {
                id: __preview
                animationEnabled: control.animationEnabled
                items: __private.previewItems
                sourceDelegate: AnimatedImage {
                    source: sourceUrl
                    fillMode: Image.PreserveAspectFit
                    onStatusChanged: {
                        if (status === Image.Ready)
                            __preview.resetTransform();
                    }
                }
            }

            TapHandler {
                onTapped: {
                    if (!__preview.opened) {
                        __preview.open();
                    }
                }
            }
        }
    }

    HoverHandler {
        id: __hoverHandler
        cursorShape: control.hoverCursorShape
    }
}
