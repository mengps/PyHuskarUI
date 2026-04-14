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
import QtQuick.Shapes
import HuskarUI.Basic

T.GroupBox {
    id: control

    property real borderWidth: 1 / Screen.devicePixelRatio
    property color colorTitle: enabled ? themeSource.colorTitle :
                                         themeSource.colorTitleDisabled
    property color colorBg: 'transparent'
    property color colorBorder: enabled ? themeSource.colorBorder :
                                          themeSource.colorBorderDisabled
    property HusRadius radiusBg: HusRadius { all: HusTheme.Primary.radiusPrimary }
    property string sizeHint: 'normal'
    property real sizeRatio: HusTheme.sizeHint[sizeHint]
    property var themeSource: HusTheme.HusGroupBox

    objectName: '__HusGroupBox__'
    implicitWidth: Math.max(implicitBackgroundWidth + leftInset + rightInset,
                            contentWidth + leftPadding + rightPadding,
                            implicitLabelWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset,
                             contentHeight + topPadding + bottomPadding)

    padding: 12 * sizeRatio
    topPadding: padding + (implicitLabelWidth > 0 ? implicitLabelHeight * 0.5 : 0)
    font {
        family: themeSource.fontFamily
        pixelSize: parseInt(themeSource.fontSize) * sizeRatio
    }
    label: HusText {
        x: control.leftPadding
        width: control.availableWidth
        text: control.title
        font: control.font
        color: control.colorTitle
        elide: Text.ElideRight
        verticalAlignment: Text.AlignVCenter
    }
    background: Item {
        y: control.topPadding - control.bottomPadding
        width: parent.width
        height: parent.height - control.topPadding + control.bottomPadding

        Shape {
            id: __shape
            anchors.fill: parent
            
            ShapePath {
                id: __path
                strokeColor: control.colorBorder
                strokeWidth: control.borderWidth
                fillColor: control.colorBg
                
                property real inset: control.borderWidth * 0.5
                property real w: __shape.width - inset
                property real h: __shape.height - inset
                
                property real rTL: Math.max(0.001, control.radiusBg.topLeft)
                property real rTR: Math.max(0.001, control.radiusBg.topRight)
                property real rBR: Math.max(0.001, control.radiusBg.bottomRight)
                property real rBL: Math.max(0.001, control.radiusBg.bottomLeft)
                
                property real labelWidth: control.implicitLabelWidth
                property real gapStartX: control.leftPadding - 4 * control.sizeRatio
                property real gapEndX: control.leftPadding + labelWidth + 4 * control.sizeRatio
                
                property real safeGapStartX: labelWidth <= 0 ? inset + rTL : Math.min(w - rTR, Math.max(inset + rTL, gapStartX))
                property real safeGapEndX: labelWidth <= 0 ? inset + rTL : Math.min(w - rTR, Math.max(inset + rTL, gapEndX))

                startX: safeGapEndX
                startY: inset
                
                PathLine { x: __path.w - __path.rTR; y: __path.inset }
                PathArc {
                    x: __path.w; y: __path.inset + __path.rTR
                    radiusX: __path.rTR; radiusY: __path.rTR
                    useLargeArc: false
                }
                PathLine { x: __path.w; y: __path.h - __path.rBR }
                PathArc {
                    x: __path.w - __path.rBR; y: __path.h
                    radiusX: __path.rBR; radiusY: __path.rBR
                    useLargeArc: false
                }
                PathLine { x: __path.inset + __path.rBL; y: __path.h }
                PathArc {
                    x: __path.inset; y: __path.h - __path.rBL
                    radiusX: __path.rBL; radiusY: __path.rBL
                    useLargeArc: false
                }
                PathLine { x: __path.inset; y: __path.inset + __path.rTL }
                PathArc {
                    x: __path.inset + __path.rTL; y: __path.inset
                    radiusX: __path.rTL; radiusY: __path.rTL
                    useLargeArc: false
                }
                PathLine { x: __path.safeGapStartX; y: __path.inset }
            }
        }
    }

    QtObject {
        id: __private
        property real implicitLabelHeight: control.title === '' ? 0 : control.implicitLabelHeight
    }
}
