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

HusInput {
    id: control

    signal search(input: string)
    signal select(option: var)

    property var options: []
    property var filterOption: (input, option) => true
    readonly property int count: options.length
    property string textRole: 'label'
    property string valueRole: 'value'
    property bool showToolTip: false
    property int defaultPopupMaxHeight: 240 * control.sizeRatio
    property int defaultOptionSpacing: 0

    property Component labelDelegate: HusText {
        text: textData
        color: control.themeSource.colorItemText
        font {
            family: control.themeSource.fontFamily
            pixelSize: parseInt(control.themeSource.fontSize)
            weight: highlighted ? Font.DemiBold : Font.Normal
        }
        elide: Text.ElideRight
        verticalAlignment: Text.AlignVCenter
    }
    property Component labelBgDelegate: Rectangle {
        radius: control.themeSource.radiusLabelBg
        color: highlighted ? control.themeSource.colorItemBgActive :
                             (hovered || selected) ? control.themeSource.colorItemBgHover :
                                                     control.themeSource.colorItemBg;

        Behavior on color { enabled: control.animationEnabled; ColorAnimation { duration: HusTheme.Primary.durationMid } }
    }

    function clearInput() {
        control.clear();
        control.textEdited();
        __popupListView.currentIndex = __popupListView.selectedIndex = -1;
    }

    function openPopup() {
        if (!__popup.opened)
            __popup.open();
    }

    function closePopup() {
        __popup.close();
    }

    function filter() {
        __private.model = options.filter(option => filterOption(text, option) === true);
        __popupListView.currentIndex = __popupListView.selectedIndex = -1;
    }

    onClickClear: {
        control.clearInput();
    }
    onOptionsChanged: {
        control.filter();
    }
    onFilterOptionChanged: {
        control.filter();
    }
    onTextEdited: {
        control.search(text);
        control.filter();
        if (__private.model.length > 0)
            control.openPopup();
        else
            control.closePopup();
    }
    Keys.onPressed: function(event) {
        if (event.key === Qt.Key_Escape) {
            control.closePopup();
        } else if (event.key === Qt.Key_Up) {
            control.openPopup();
            if (__popupListView.selectedIndex > 0) {
                __popupListView.selectedIndex -= 1;
                __popupListView.positionViewAtIndex(__popupListView.selectedIndex, ListView.Contain);
            } else {
                __popupListView.selectedIndex = __popupListView.count - 1;
                __popupListView.positionViewAtIndex(__popupListView.selectedIndex, ListView.Contain);
            }
        } else if (event.key === Qt.Key_Down) {
            control.openPopup();
            __popupListView.selectedIndex = (__popupListView.selectedIndex + 1) % __popupListView.count;
            __popupListView.positionViewAtIndex(__popupListView.selectedIndex, ListView.Contain);
        } else if (event.key === Qt.Key_Enter || event.key === Qt.Key_Return) {
            if (__popupListView.selectedIndex !== -1) {
                const modelData = __private.model[__popupListView.selectedIndex];
                const textData = modelData[control.textRole];
                const valueData = modelData[control.valueRole] ?? textData;
                control.select(modelData);
                control.text = valueData;
                __popup.close();
                control.filter();
            }
        }
    }

    objectName: '__HusAutoComplete__'
    themeSource: HusTheme.HusAutoComplete
    iconPosition: HusInput.Position_Right
    clearEnabled: 'active'

    Item {
        id: __private
        property var window: Window.window
        property var model: []
    }

    TapHandler {
        enabled: control.enabled && !control.readOnly
        onTapped: {
            if (__private.model.length > 0)
                control.openPopup();
        }
    }

    HusPopup {
        id: __popup
        y: control.height + 6
        implicitWidth: control.width
        implicitHeight: implicitContentHeight + topPadding + bottomPadding
        leftPadding: 4 * control.sizeRatio
        rightPadding: 4 * control.sizeRatio
        topPadding: 6 * control.sizeRatio
        bottomPadding: 6 * control.sizeRatio
        animationEnabled: control.animationEnabled
        closePolicy: T.Popup.NoAutoClose | T.Popup.CloseOnEscape | T.Popup.CloseOnPressOutsideParent
        transformOrigin: isTop ? Item.Bottom : Item.Top
        enter: Transition {
            NumberAnimation {
                property: 'scale'
                from: 0.9
                to: 1.0
                easing.type: Easing.OutQuad
                duration: control.animationEnabled ? HusTheme.Primary.durationMid : 0
            }
            NumberAnimation {
                property: 'opacity'
                from: 0.0
                to: 1.0
                easing.type: Easing.OutQuad
                duration: control.animationEnabled ? HusTheme.Primary.durationMid : 0
            }
        }
        exit: Transition {
            NumberAnimation {
                property: 'scale'
                from: 1.0
                to: 0.9
                easing.type: Easing.InQuad
                duration: control.animationEnabled ? HusTheme.Primary.durationMid : 0
            }
            NumberAnimation {
                property: 'opacity'
                from: 1.0
                to: 0.0
                easing.type: Easing.InQuad
                duration: control.animationEnabled ? HusTheme.Primary.durationMid : 0
            }
        }
        contentItem: ListView {
            id: __popupListView
            property int selectedIndex: -1
            implicitHeight: Math.min(control.defaultPopupMaxHeight, contentHeight)
            clip: true
            currentIndex: -1
            model: __private.model
            boundsBehavior: Flickable.StopAtBounds
            spacing: control.defaultOptionSpacing
            delegate: T.ItemDelegate {
                id: __popupDelegate

                required property var modelData
                required property int index

                property var textData: modelData[control.textRole]
                property var valueData: modelData[control.valueRole] ?? textData
                property bool selected: __popupListView.selectedIndex === index

                width: __popupListView.width
                height: implicitContentHeight + topPadding + bottomPadding
                leftPadding: 8 * control.sizeRatio
                rightPadding: 8 * control.sizeRatio
                topPadding: 5 * control.sizeRatio
                bottomPadding: 5 * control.sizeRatio
                highlighted: control.text === valueData
                contentItem: Loader {
                    sourceComponent: control.labelDelegate
                    property alias textData: __popupDelegate.textData
                    property alias valueData: __popupDelegate.valueData
                    property alias modelData: __popupDelegate.modelData
                    property alias hovered: __popupDelegate.hovered
                    property alias highlighted: __popupDelegate.highlighted
                }
                background: Loader {
                    sourceComponent: control.labelBgDelegate
                    property alias textData: __popupDelegate.textData
                    property alias valueData: __popupDelegate.valueData
                    property alias modelData: __popupDelegate.modelData
                    property alias hovered: __popupDelegate.hovered
                    property alias selected: __popupDelegate.selected
                    property alias highlighted: __popupDelegate.highlighted
                }
                onClicked: {
                    control.select(__popupDelegate.modelData);
                    control.text = __popupDelegate.valueData;
                    __popup.close();
                    control.filter();
                }

                HoverHandler {
                    cursorShape: Qt.PointingHandCursor
                }

                Loader {
                    y: __popupDelegate.height
                    anchors.horizontalCenter: parent.horizontalCenter
                    active: control.showToolTip
                    sourceComponent: HusToolTip {
                        showArrow: false
                        visible: __popupDelegate.hovered && !__popupDelegate.pressed
                        text: __popupDelegate.textData
                        position: HusToolTip.Position_Bottom
                    }
                }
            }
            T.ScrollBar.vertical: HusScrollBar { }
        }
        Component.onCompleted: HusApi.setPopupAllowAutoFlip(this);
        property bool isTop: (y + height * 0.5) < control.height * 0.5
    }
}
