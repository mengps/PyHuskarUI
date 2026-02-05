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

    enum ImageStyle
    {
        Style_None = 0,
        Style_Default = 1,
        Style_Simple = 2
    }

    property int imageStyle: HusEmpty.Style_Default
    property string imageSource: {
        switch (imageStyle) {
        case HusEmpty.Style_None: return '';
        case HusEmpty.Style_Default: return 'qrc:/HuskarUI/resources/images/empty-default.svg';
        case HusEmpty.Style_Simple: return 'qrc:/HuskarUI/resources/images/empty-simple.svg';
        }
    }
    property int imageWidth: {
        switch (imageStyle) {
        case HusEmpty.Style_None: return width / 3;
        case HusEmpty.Style_Default: return 92;
        case HusEmpty.Style_Simple: return 64;
        }
    }
    property int imageHeight: {
        switch (imageStyle) {
        case HusEmpty.Style_None: return height / 3;
        case HusEmpty.Style_Default: return 76;
        case HusEmpty.Style_Simple: return 41;
        }
    }
    property bool showDescription: true
    property string description: ''
    property int descriptionSpacing: 12
    property alias descriptionFont: control.font
    property color colorDescription: themeSource.colorDescription
    property var themeSource: HusTheme.HusEmpty

    property Component imageDelegate: Image {
        width: control.imageWidth
        height: control.imageHeight
        source: control.imageSource
        sourceSize: Qt.size(width, height)
    }
    property Component descriptionDelegate: HusText {
        text: control.description
        font: control.descriptionFont
        color: control.colorDescription
        horizontalAlignment: Text.AlignHCenter
    }

    objectName: '__HusEmpty__'
    implicitWidth: Math.max(implicitBackgroundWidth + leftInset + rightInset,
                            implicitContentWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset,
                             implicitContentHeight + topPadding + bottomPadding)
    font {
        family: themeSource.fontFamily
        pixelSize: parseInt(themeSource.fontSize) - 1
    }
    contentItem: Item {
        implicitWidth: 200
        implicitHeight: 200

        ColumnLayout {
            anchors.centerIn: parent
            spacing: control.descriptionSpacing

            Loader {
                Layout.alignment: Qt.AlignHCenter
                Layout.fillWidth: true
                visible: active
                active: control.imageSource !== '' || control.imageStyle !== HusEmpty.Style_None
                sourceComponent: control.imageDelegate
            }

            Loader {
                Layout.alignment: Qt.AlignHCenter
                Layout.fillWidth: true
                visible: active
                active: control.showDescription
                sourceComponent: control.descriptionDelegate
            }
        }
    }
}
