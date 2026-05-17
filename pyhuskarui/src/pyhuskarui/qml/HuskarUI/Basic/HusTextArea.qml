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
import QtQuick.Controls.impl
import QtQuick.Templates as T
import HuskarUI.Basic

T.Control {
    id: control

    signal editingFinished()

    property bool animationEnabled: HusTheme.animationEnabled
    property bool active: __textArea.hovered || __textArea.activeFocus
    property bool resizable: false
    property int minResizeHeight: 30
    property bool autoSize: false
    property int minRows: -1
    property int maxRows: -1
    readonly property alias lineCount: __textArea.lineCount
    property alias length: __textArea.length
    property int maxLength: -1
    property alias readOnly: __textArea.readOnly
    property alias textFormat: __textArea.textFormat
    property alias text: __textArea.text
    property alias placeholderText: __textArea.placeholderText
    property alias colorText: __textArea.color
    property alias colorPlaceholderText: __textArea.placeholderTextColor
    property alias colorSelectedText: __textArea.selectedTextColor
    property alias colorSelection: __textArea.selectionColor
    property color colorBorder: enabled ? active ? themeSource.colorBorderHover :
                                                   themeSource.colorBorder : themeSource.colorBorderDisabled
    property color colorBg: enabled ? themeSource.colorBg : themeSource.colorBgDisabled
    property HusRadius radiusBg: HusRadius { all: themeSource.radiusBg }
    property string contentDescription: ''
    property var themeSource: HusTheme.HusTextArea

    property alias textArea: __textArea
    property alias verScrollBar: __vScrollBar
    property alias horScrollBar: __hScrollBar

    property Component bgDelegate: HusRectangleInternal {
        color: control.colorBg
        border.color: control.colorBorder
        radius: control.radiusBg.all
        topLeftRadius: control.radiusBg.topLeft
        topRightRadius: control.radiusBg.topRight
        bottomLeftRadius: control.radiusBg.bottomLeft
        bottomRightRadius: control.radiusBg.bottomRight
    }

    function scrollToBeginning() {
        __textArea.cursorPosition = 0;
    }

    function scrollToEnd() {
        __textArea.cursorPosition = __textArea.length;
    }

    function clear() {
        __textArea.clear();
    }

    Behavior on colorText { enabled: control.animationEnabled; ColorAnimation { duration: HusTheme.Primary.durationMid } }
    Behavior on colorPlaceholderText { enabled: control.animationEnabled; ColorAnimation { duration: HusTheme.Primary.durationMid } }
    Behavior on colorSelectedText { enabled: control.animationEnabled; ColorAnimation { duration: HusTheme.Primary.durationMid } }
    Behavior on colorBorder { enabled: control.animationEnabled; ColorAnimation { duration: HusTheme.Primary.durationMid } }
    Behavior on colorBg { enabled: control.animationEnabled; ColorAnimation { duration: HusTheme.Primary.durationMid } }

    onTextChanged: __private.removeExcess();
    onMaxLengthChanged: __private.removeExcess();

    objectName: '__HusTextArea__'
    topPadding: 6
    bottomPadding: 6
    leftPadding: 10
    rightPadding: 10
    font {
        family: control.themeSource.fontFamily
        pixelSize: parseInt(control.themeSource.fontSize)
    }
    wheelEnabled: autoSize ? (minRows > 0 && maxRows > 0) : (__vScrollBar.visible || __vScrollBar.active)
    contentItem: Item {
        implicitHeight: {
            if (control.autoSize) {
                if (control.minRows > 0 && control.maxRows > 0) {
                    if (control.lineCount < control.minRows)
                        return __private.minHeight + __textArea.topPadding + __textArea.bottomPadding;
                    else if (lineCount > maxRows) {
                        return __private.maxHeight + __textArea.topPadding + __textArea.bottomPadding;
                    } else {
                        return control.lineCount * __private.lineHeight + __textArea.topPadding + __textArea.bottomPadding;
                    }
                } else {
                    return __textArea.implicitHeight;
                }
            } else {
                return control.minResizeHeight;
            }
        }

        Behavior on implicitHeight {
            enabled: control.animationEnabled && !__resize.pressed
            NumberAnimation {
                duration: HusTheme.Primary.durationMid
            }
        }

        /*! [QtBug] 必须先创建一遍 ScrollBar */
        component SV: T.ScrollView {
            id: __control
            T.ScrollBar.vertical: T.ScrollBar { }
            T.ScrollBar.horizontal: T.ScrollBar { }
        }

        SV {
            id: __scrollView
            focus: true
            anchors.fill: parent
            T.ScrollBar.vertical: HusScrollBar {
                id: __vScrollBar
                parent: __scrollView
                x: __scrollView.mirrored ? 0 : __scrollView.width - width
                y: __scrollView.topPadding
                height: __scrollView.availableHeight
                orientation: Qt.Vertical
                policy: HusScrollBar.AlwaysOn
                animationEnabled: control.animationEnabled
                active: __scrollView.HusScrollBar.horizontal.active
            }
            T.ScrollBar.horizontal: HusScrollBar {
                id: __hScrollBar
                parent: __scrollView
                x: __scrollView.leftPadding
                y: __scrollView.height - height
                width: __scrollView.availableWidth
                orientation: Qt.Horizontal
                policy: T.ScrollBar.AlwaysOn
                animationEnabled: control.animationEnabled
                active: __scrollView.T.ScrollBar.vertical.active
            }
            Component.onCompleted: {
                contentItem.boundsBehavior = Flickable.StopAtBounds;
            }

            T.TextArea {
                id: __textArea
                focus: true
                implicitWidth: Math.max(contentWidth + leftPadding + rightPadding,
                                        implicitBackgroundWidth + leftInset + rightInset,
                                        __placeholder.implicitWidth + leftPadding + rightPadding)
                implicitHeight: Math.max(contentHeight + topPadding + bottomPadding,
                                         implicitBackgroundHeight + topInset + bottomInset,
                                         __placeholder.implicitHeight + topPadding + bottomPadding)
                topPadding: 0
                bottomPadding: 0
                leftPadding: 0
                rightPadding: 0
                wrapMode: T.TextArea.WrapAnywhere
                renderType: HusTheme.textRenderType
                selectByMouse: true
                selectByKeyboard: true
                color: enabled ? control.themeSource.colorText : control.themeSource.colorTextDisabled
                placeholderTextColor: enabled ? themeSource.colorPlaceholderText : themeSource.colorPlaceholderTextDisabled
                selectedTextColor: control.themeSource.colorTextSelected
                selectionColor: control.themeSource.colorSelection
                font: control.font
                onEditingFinished: control.editingFinished();

                PlaceholderText {
                    id: __placeholder
                    x: parent.leftPadding
                    y: parent.topPadding
                    width: parent.width - (parent.leftPadding + parent.rightPadding)
                    height: parent.height - (parent.topPadding + parent.bottomPadding)

                    text: parent.placeholderText
                    font: parent.font
                    color: parent.placeholderTextColor
                    verticalAlignment: parent.verticalAlignment
                    visible: !parent.length && !parent.preeditText && (!parent.activeFocus || parent.horizontalAlignment !== Qt.AlignHCenter)
                    elide: Text.ElideRight
                    renderType: parent.renderType
                }
            }
        }
    }
    background: Loader {
        sourceComponent: control.bgDelegate
    }

    HusIconText {
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.margins: 1
        iconSource: HusIcon.MinusOutlined
        rotation: -45
        visible: control.resizable
        enabled: visible

        HusIconText {
            y: 4
            iconSource: HusIcon.MinusOutlined
            scale: 0.5
        }

        MouseArea {
            id: __resize
            anchors.fill: parent
            hoverEnabled: true
            preventStealing: true
            onEntered: cursorShape = Qt.SizeVerCursor;
            onExited: cursorShape = Qt.ArrowCursor;
            onPressed: mouse => {
                startY = mouseY;
                mouse.accepted = true;
            }
            onReleased: mouse => mouse.accepted = true;
            onPositionChanged: mouse => {
                if (pressed) {
                    const offsetY = mouse.y - startY;
                    control.height = Math.max(control.height + offsetY, control.minResizeHeight);
                    mouse.accepted = true;
                }
            }
            property int startY: 0
        }
    }

    QtObject {
        id: __private

        property real minHeight: lineHeight * control.minRows
        property real maxHeight: lineHeight * control.maxRows
        property real lineHeight: __textArea.contentHeight / __textArea.lineCount

        function removeExcess() {
            if (control.maxLength > 0 && control.length > control.maxLength) {
                __textArea.remove(control.maxLength, control.length);
            }
        }
    }

    Accessible.role: Accessible.EditableText
    Accessible.editable: !control.readOnly
    Accessible.description: control.contentDescription
}
