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

T.Control {
    id: control

    property bool animationEnabled: HusTheme.animationEnabled
    property var options: []
    property alias currentIndex: __listView.currentIndex
    readonly property var currentValue: get(currentIndex)?.value
    readonly property int count: __listModel.count
    property bool block: false
    property int orientation: Qt.Horizontal
    property real defaultItemHeight: 26 * sizeRatio
    property int iconSpacing: 5
    property font iconFont: Qt.font({
                                        family: 'HuskarUI-Icons',
                                        pixelSize: control.font.pixelSize
                                    })
    property color colorBg: HusTheme.isDark ? themeSource.colorBgDark : themeSource.colorBg
    property color colorIndicatorBg: themeSource.colorIndicatorBg
    property color colorBorder: themeSource.colorBorder
    property HusRadius radiusBg: HusRadius { all: themeSource.radiusBg }
    property string sizeHint: 'normal'
    property real sizeRatio: HusTheme.sizeHint[sizeHint]
    property var themeSource: HusTheme.HusSegmented

    property Component indicatorDelegate: HusRectangleInternal {
        id: __indicator
        color: control.colorIndicatorBg
        radius: control.radiusBg.all
        topLeftRadius: control.radiusBg.topLeft
        topRightRadius: control.radiusBg.topRight
        bottomLeftRadius: control.radiusBg.bottomLeft
        bottomRightRadius: control.radiusBg.bottomRight

        Behavior on color { enabled: control.animationEnabled; ColorAnimation { duration: HusTheme.Primary.durationFast } }
    }
    property Component itemDelegate: Item {
        id: __itemDelegate
        width: __row.implicitWidth + (control.orientation === Qt.Horizontal ? 20 * control.sizeRatio : 0)
        height: __row.implicitHeight + (control.orientation === Qt.Horizontal ? 0 : 8 * control.sizeRatio)

        property bool hasIcon: model.iconSource !== 0 && model.iconSource !== ''

        Row {
            id: __row
            anchors.centerIn: parent
            spacing: control.iconSpacing

            Loader {
                id: __icon
                height: Math.max(__icon.implicitHeight, __label.implicitHeight)
                anchors.verticalCenter: parent.verticalCenter
                active: __itemDelegate.hasIcon
                sourceComponent: control.iconDelegate
                property int index: __itemDelegate.parent.index
                property var model: __itemDelegate.parent.model
                property bool hovered: __itemDelegate.parent.hovered
                property bool pressed: __itemDelegate.parent.pressed
                property bool isCurrent: __itemDelegate.parent.isCurrent
            }

            HusText {
                id: __label
                anchors.verticalCenter: parent.verticalCenter
                text: model.label
                font: control.font
                color: {
                    if (enabled ) {
                        return (hovered || isCurrent) ? control.themeSource.colorTextSelected :
                                                        control.themeSource.colorText;
                    } else {
                        return control.themeSource.colorTextDisabled;
                    }
                }
            }
        }
    }
    property Component iconDelegate: HusIconText {
        font: control.iconFont
        colorIcon: {
            if (enabled ) {
                return (hovered || isCurrent) ? control.themeSource.colorTextSelected :
                                                control.themeSource.colorText;
            } else {
                return control.themeSource.colorTextDisabled;
            }
        }
        iconSource: model ? model.iconSource : 0
        verticalAlignment: Text.AlignVCenter

        Behavior on color { enabled: control.animationEnabled; ColorAnimation { duration: HusTheme.Primary.durationFast } }
    }
    property Component toolTipDelegate: HusToolTip {
        text: model.toolTip
        visible: hovered
    }

    function get(index: int): var {
        return __listModel.get(index);
    }

    function set(index: int, object: var) {
        __listModel.set(index, __private.initObject(object));
    }

    function setProperty(index: int, propertyName: string, value: var) {
        __listModel.setProperty(index, propertyName, value);
    }

    function move(from: int, to: int, count = 1) {
        __listModel.move(from, to, count);
    }

    function insert(index: int, object: var) {
        __listModel.insert(index, __private.initObject(object));
    }

    /*! [QtBug] Can't assign to existing role 'value' of different type [String -> VariantMap] */
    function append(object: var) {
        __listModel.append(__private.initObject(object));
    }

    function remove(index: int, count = 1) {
        __listModel.remove(index, count);
    }

    function clear() {
        __listModel.clear();
    }

    onOptionsChanged: {
        clear();
        for (let object of options) {
            append(object);
        }
    }

    objectName: '__HusSegmented__'
    implicitWidth: block ? parent.width : Math.max(implicitBackgroundWidth + leftInset + rightInset,
                                                   implicitContentWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset,
                             implicitContentHeight + topPadding + bottomPadding)
    padding: 2 * sizeRatio
    font {
        family: themeSource.fontFamily
        pixelSize: parseInt(themeSource.fontSize) * sizeRatio
    }
    background: HusRectangleInternal {
        color: control.colorBg
        border.color: control.colorBorder
        radius: control.radiusBg.all
        topLeftRadius: control.radiusBg.topLeft
        topRightRadius: control.radiusBg.topRight
        bottomLeftRadius: control.radiusBg.bottomLeft
        bottomRightRadius: control.radiusBg.bottomRight

        Behavior on color { enabled: control.animationEnabled; ColorAnimation { duration: HusTheme.Primary.durationFast } }
    }
    contentItem: Item {
        id: __contentItem
        implicitWidth: __listView.orientation === ListView.Horizontal ? __listView.width : 120 * sizeRatio
        implicitHeight: __listView.orientation === ListView.Horizontal ? control.defaultItemHeight : __listView.height

        ListView {
            id: __listView
            width: orientation === ListView.Horizontal ? (block ? parent.width : contentWidth) : parent.width
            height: orientation === ListView.Horizontal ? parent.height : (block ? parent.height : contentHeight)
            orientation: control.orientation === Qt.Horizontal ? ListView.Horizontal : ListView.Vertical
            highlightMoveDuration: control.animationEnabled ? HusTheme.Primary.durationSlow : 0
            highlightResizeDuration: control.animationEnabled ? HusTheme.Primary.durationSlow : 0
            boundsBehavior: Flickable.StopAtBounds
            spacing: control.spacing
            onContentWidthChanged: if (orientation === ListView.Horizontal) cacheBuffer = contentWidth;
            onContentHeightChanged: if (orientation === ListView.Vertical) cacheBuffer = contentHeight;
            currentIndex: 0
            model: ListModel { id: __listModel }
            highlight: control.indicatorDelegate
            delegate: HusRectangleInternal {
                id: __rootItem
                implicitWidth: {
                    if (__listView.orientation === ListView.Horizontal) {
                        if (control.block) {
                            return ((__contentItem.width - __listModel.count * __listView.spacing) / __listModel.count );
                        } else {
                            return __itemLoader.implicitWidth;
                        }
                    } else {
                        return __listView.width;
                    }
                }
                implicitHeight: {
                    if (__listView.orientation === ListView.Horizontal) {
                        return __listView.height;
                    } else {
                        if (control.block) {
                            return ((__contentItem.height - __listModel.count * __listView.spacing) / __listModel.count );
                        } else {
                            return __itemLoader.implicitHeight;
                        }
                    }
                }
                topLeftRadius: index === 0 ? control.radiusBg.topLeft : control.radiusBg.all
                topRightRadius: index === (__listModel.count - 1) ? control.radiusBg.topRight : control.radiusBg.all
                bottomLeftRadius: index === 0 ? control.radiusBg.bottomLeft : control.radiusBg.all
                bottomRightRadius: index === (__listModel.count - 1) ? control.radiusBg.bottomRight : control.radiusBg.all
                color: {
                    if (enabled && !isCurrent) {
                        return pressed ? control.themeSource.colorItemBgActive :
                                         hovered ? control.themeSource.colorItemBgHover :
                                                   control.themeSource.colorItemBg;
                    } else {
                        return 'transparent';
                    }
                }
                enabled: model.enabled

                required property int index
                required property var model
                readonly property bool pressed: __tapHandler.pressed
                readonly property bool hovered: __hoverHandler.hovered
                readonly property bool isCurrent: control.currentIndex === index

                Behavior on color { enabled: control.animationEnabled; ColorAnimation { duration: HusTheme.Primary.durationFast } }

                HoverHandler {
                    id: __hoverHandler
                    cursorShape: Qt.PointingHandCursor
                }

                TapHandler {
                    id: __tapHandler
                    cursorShape: Qt.PointingHandCursor
                    onTapped: {
                        __listView.currentIndex = index;
                    }
                }

                Loader {
                    id: __itemLoader
                    anchors.centerIn: parent
                    sourceComponent: control.itemDelegate
                    property alias index: __rootItem.index
                    property alias model: __rootItem.model
                    property alias hovered: __rootItem.hovered
                    property alias pressed: __rootItem.pressed
                    property alias isCurrent: __rootItem.isCurrent
                }

                Loader {
                    anchors.fill: parent
                    active: model.toolTip !== ''
                    sourceComponent: control.toolTipDelegate
                    property alias index: __rootItem.index
                    property alias model: __rootItem.model
                    property alias hovered: __rootItem.hovered
                    property alias pressed: __rootItem.pressed
                    property alias isCurrent: __rootItem.isCurrent
                }
            }
        }
    }

    QtObject {
        id: __private

        function initObject(object: var): var {
            if (typeof object !== 'object') {
                return initObject({ label: String(object) });
            } else {
                if (!object.hasOwnProperty('label')) object.label = '';
                if (!object.hasOwnProperty('value')) object.value = object.label;
                if (!object.hasOwnProperty('enabled')) object.enabled = true;
                if (!object.hasOwnProperty('toolTip')) object.toolTip = '';
                if (!object.hasOwnProperty('iconSource')) object.iconSource = 0;

                return object;
            }
        }
    }
}
