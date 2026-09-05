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

HusPopup {
    id: control

    property bool animationEnabled: HusTheme.animationEnabled

    property alias scaleMin: __panel.scaleMin
    property alias scaleMax: __panel.scaleMax
    property alias scaleStep: __panel.scaleStep

    readonly property alias currentScale: __panel.scale
    readonly property alias currentRotation: __panel.rotation

    property alias items: __panel.items
    property alias currentIndex: __panel.currentIndex
    readonly property alias count: __panel.count

    property alias sourceDelegate: __panel.sourceDelegate
    property Component closeDelegate: HusIconButton {
        topPadding: 10
        bottomPadding: 10
        animationEnabled: control.animationEnabled
        effectEnabled: false
        iconSource: HusIcon.CloseOutlined
        iconSize: 20
        shape: HusButton.Shape_Circle
        type: HusButton.Type_Default
        colorIcon: control.themeSource.colorButtonTextHover
        colorBg: hovered ? control.themeSource.colorButtonBgHover : control.themeSource.colorButtonBg
        borderBg.color: colorBg
        onClicked: control.close();
    }
    property alias prevDelegate: __panel.sourceDelegate
    property alias nextDelegate: __panel.nextDelegate
    property alias indicatorDelegate: __panel.indicatorDelegate
    property alias operationDelegate: __panel.operationDelegate

    property alias panel: __panel

    function get(index: int): var {
        return __panel.get(index);
    }

    function set(index: int, object: var) {
        __panel.set(index, object);
    }

    function setProperty(index: int, propertyName: string, value: var) {
        __panel.setProperty(index, propertyName, value);
    }

    function move(from: int, to: int, count = 1) {
        __panel.move(from, to, count);
    }

    function insert(index: int, object: var) {
        __panel.insert(index, object);
    }

    function append(object: var) {
        __panel.append(object);
    }

    function remove(index: int, count = 1) {
        __panel.remove(index, count);
    }

    function clear() {
        __panel.clear();
    }

    function zoomIn() {
        __panel.zoomIn();
    }

    function zoomOut() {
        __panel.zoomOut();
    }

    function flipX() {
        __panel.flipX();
    }

    function flipY() {
        __panel.flipY();
    }

    function rotate(angle: real) {
        __panel.rotate(angle);
    }

    function toCenter() {
        __panel.toCenter();
    }

    function resetTransform() {
        __panel.resetTransform();
    }

    function incrementCurrentIndex() {
        __panel.incrementCurrentIndex();
    }

    function decrementCurrentIndex() {
        __panel.decrementCurrentIndex();
    }

    objectName: '__HusImagePreview__'
    themeSource: HusTheme.HusImagePreview
    width: parent.width
    height: parent.height
    closePolicy: T.Popup.NoAutoClose
    parent: T.Overlay.overlay
    modal: true
    focus: true
    onAboutToShow: {
        control.resetTransform();
        __private.visible = true;
        __panel.forceActiveFocus();
    }
    onAboutToHide: {
        __private.visible = false;
    }
    contentItem: HusImagePreviewPanel {
        id: __panel
        animationEnabled: control.animationEnabled
        themeSource: control.themeSource
        minViewHeight: height - 200
        onClicked:
            inImage => {
                if (!inImage) {
                    control.close();
                }
            }
        onDoubleClicked:
            inImage => {
                if (currentScale > 1.0) {
                    currentScale = 1.0;
                    toCenter();
                } else {
                    zoomIn();
                }
            }

        Keys.onPressed: function(event) {
            if (event.key === Qt.Key_Left) {
                decrementCurrentIndex();
            } else if (event.key === Qt.Key_Right) {
                incrementCurrentIndex();
            } else if (event.key === Qt.Key_Escape) {
                control.close();
            }
        }

        Loader {
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.margins: 30
            sourceComponent: control.closeDelegate
        }
    }
    background: Item { }

    QtObject {
        id: __private

        property bool visible: false
    }
}
