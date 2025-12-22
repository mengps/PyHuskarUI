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

Rectangle {
    id: control

    property var targetWindow: null
    property HusWindowAgent windowAgent: null

    property alias layoutDirection: __row.layoutDirection

    property string winIcon: ''
    property alias winIconWidth: __winIconLoader.width
    property alias winIconHeight: __winIconLoader.height
    property alias showWinIcon: __winIconLoader.visible

    property string winTitle: targetWindow?.title ?? ''
    property font winTitleFont: Qt.font({
                                            family: HusTheme.Primary.fontPrimaryFamily,
                                            pixelSize: 14
                                        })
    property color winTitleColor: HusTheme.Primary.colorTextBase
    property alias showWinTitle: __winTitleLoader.visible

    property bool showReturnButton: false
    property bool showThemeButton: false
    property bool topButtonChecked: false
    property bool showTopButton: false
    property bool showMinimizeButton: Qt.platform.os !== 'osx'
    property bool showMaximizeButton: Qt.platform.os !== 'osx'
    property bool showCloseButton: Qt.platform.os !== 'osx'

    property var returnCallback: () => { }
    property var themeCallback: () => { HusTheme.darkMode = HusTheme.isDark ? HusTheme.Light : HusTheme.Dark; }
    property var topCallback: checked => { }
    property var minimizeCallback:
        () => {
            if (targetWindow) {
                HusApi.setWindowState(targetWindow, Qt.WindowMinimized);
            }
        }
    property var maximizeCallback:
        () => {
            if (!targetWindow) return;

            if (targetWindow.visibility === Window.Maximized ||
                targetWindow.visibility === Window.FullScreen) {
                targetWindow.showNormal();
            } else {
                targetWindow.showMaximized();
            }
        }
    property var closeCallback:
        () => {
            if (targetWindow) targetWindow.close();
        }
    property string contentDescription: winTitle

    property Component winIconDelegate: Image {
        source: control.winIcon
        sourceSize.width: width
        sourceSize.height: height
        mipmap: true
    }
    property Component winTitleDelegate: HusText {
        text: winTitle
        color: winTitleColor
        font: winTitleFont
    }
    property Component winPresetButtonsDelegate: Row {
        Connections {
            target: control
            function onWindowAgentChanged() {
                control.addInteractionItem(__themeButton);
                control.addInteractionItem(__topButton);
            }
        }

        HusCaptionButton {
            id: __themeButton
            height: parent.height
            visible: control.showThemeButton
            noDisabledState: true
            iconSource: HusTheme.isDark ? HusIcon.MoonOutlined : HusIcon.SunOutlined
            iconSize: 14
            contentDescription: qsTr('明暗主题切换')
            onClicked: control.themeCallback();
        }

        HusCaptionButton {
            id: __topButton
            height: parent.height
            visible: control.showTopButton
            noDisabledState: true
            iconSource: HusIcon.PushpinOutlined
            iconSize: 14
            checkable: true
            checked: control.topButtonChecked
            contentDescription: qsTr('置顶')
            onClicked: control.topCallback(checked);
        }
    }
    property Component winExtraButtonsDelegate: Item { }
    property Component winButtonsDelegate: Row {
        Connections {
            target: control
            function onWindowAgentChanged() {
                if (windowAgent) {
                    windowAgent.setSystemButton(HusWindowAgent.Minimize, __minimizeButton);
                    windowAgent.setSystemButton(HusWindowAgent.Maximize, __maximizeButton);
                    windowAgent.setSystemButton(HusWindowAgent.Close, __closeButton);
                }
            }
        }

        HusCaptionButton {
            id: __minimizeButton
            height: parent.height
            visible: control.showMinimizeButton
            noDisabledState: true
            iconSource: HusIcon.LineOutlined
            iconSize: 14
            contentDescription: qsTr('最小化')
            onClicked: control.minimizeCallback();
        }

        HusCaptionButton {
            id: __maximizeButton
            height: parent.height
            noDisabledState: true
            iconSize: 14
            contentItem: HusIconText {
                iconSource: HusIcon.SwitcherTwotonePath3
                iconSize: __maximizeButton.iconSize
                colorIcon: __maximizeButton.colorIcon
                verticalAlignment: Text.AlignVCenter
                visible: targetWindow

                HusIconText {
                    anchors.centerIn: parent
                    iconSource: HusIcon.SwitcherTwotonePath2
                    iconSize: __maximizeButton.iconSize
                    colorIcon: __maximizeButton.colorIcon
                    verticalAlignment: Text.AlignVCenter
                    visible: targetWindow && targetWindow.visibility === Window.Maximized
                }
            }
            contentDescription: qsTr('最大化')
            onClicked: control.maximizeCallback();
        }

        HusCaptionButton {
            id: __closeButton
            height: parent.height
            visible: control.showCloseButton
            noDisabledState: true
            iconSource: HusIcon.CloseOutlined
            iconSize: 14
            isError: true
            contentDescription: qsTr('关闭')
            onClicked: control.closeCallback();
        }
    }

    objectName: '__HusCaptionBar__'
    color: 'transparent'

    function addInteractionItem(item) {
        if (windowAgent)
            windowAgent.setHitTestVisible(item, true);
    }

    function removeInteractionItem(item) {
        if (windowAgent)
            windowAgent.setHitTestVisible(item, false);
    }

    RowLayout {
        id: __row
        anchors.fill: parent
        spacing: 0

        HusCaptionButton {
            id: __returnButton
            Layout.alignment: Qt.AlignVCenter
            noDisabledState: true
            iconSource: HusIcon.ArrowLeftOutlined
            iconSize: parseInt(HusTheme.HusCaptionButton.fontSize) + 2
            visible: control.showReturnButton
            onClicked: control.returnCallback();
            contentDescription: qsTr('返回')
        }

        Item {
            id: __title
            Layout.fillWidth: true
            Layout.fillHeight: true
            Component.onCompleted: {
                if (windowAgent)
                    windowAgent.setTitleBar(__title);
            }

            Row {
                height: parent.height
                anchors.left: Qt.platform.os === 'osx' ? undefined : parent.left
                anchors.leftMargin: Qt.platform.os === 'osx' ? 0 : 8
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: Qt.platform.os === 'osx' ? parent.horizontalCenter : undefined
                spacing: 5

                Loader {
                    id: __winIconLoader
                    width: 20
                    height: 20
                    anchors.verticalCenter: parent.verticalCenter
                    sourceComponent: winIconDelegate
                }

                Loader {
                    id: __winTitleLoader
                    anchors.verticalCenter: parent.verticalCenter
                    sourceComponent: winTitleDelegate
                }
            }
        }

        Loader {
            Layout.fillHeight: true
            Layout.alignment: Qt.AlignVCenter
            sourceComponent: winPresetButtonsDelegate
        }

        Loader {
            Layout.fillHeight: true
            Layout.alignment: Qt.AlignVCenter
            sourceComponent: winExtraButtonsDelegate
        }

        Loader {
            Layout.fillHeight: true
            Layout.alignment: Qt.AlignVCenter
            sourceComponent: winButtonsDelegate
        }
    }

    Accessible.role: Accessible.TitleBar
    Accessible.name: control.contentDescription
    Accessible.description: control.contentDescription
}
