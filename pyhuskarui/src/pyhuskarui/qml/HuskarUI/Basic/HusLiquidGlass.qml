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

Item {
    id: control

    property alias sourceItem: __source.sourceItem
    property alias sourceRect: __source.sourceRect
    property real refraction: 0.026
    property real bevelDepth: 0.119
    property real bevelWidth: 0.057
    property real frost: 0.0
    property bool animated: true
    property real specularIntensity: 1.0
    property real tiltX: 0.0
    property real tiltY: 0.0
    property real magnify: 1.0
    property HusRadius radiusBg: HusRadius { all: 0 }

    objectName: '__HusLiquidGlass__'

    readonly property real __srcScale: {
        const magnifyPad = Math.max(1.0 / Math.max(control.magnify, 0.001), 1.0);
        const refrPad = 1.0 + 2.0 * (control.refraction + control.bevelDepth);
        return Math.max(magnifyPad, refrPad, 1.1);
    }

    ShaderEffectSource {
        id: __source
        anchors.fill: parent
        visible: false
        sourceRect: Qt.rect(
            control.x - control.width * (control.__srcScale - 1.0) * 0.5,
            control.y - control.height * (control.__srcScale - 1.0) * 0.5,
            control.width * control.__srcScale,
            control.height * control.__srcScale
        )
    }

    ShaderEffect {
        id: __shaderEffect
        anchors.fill: parent

        property variant source: __source
        property vector2d resolution: Qt.vector2d(control.width, control.height)
        property real refraction: control.refraction
        property real bevelDepth: control.bevelDepth
        property real bevelWidth: control.bevelWidth
        property real frost: control.frost
        property real radius: control.radiusBg.all
        property real specularIntensity: control.specularIntensity
        property real tiltX: control.tiltX
        property real tiltY: control.tiltY
        property real magnify: control.magnify
        property real iTime: 0.0

        NumberAnimation on iTime {
            running: control.animated && control.specularIntensity > 0.0
            loops: Animation.Infinite
            from: 0
            to: 360000      // 360000 seconds = 100 hours
            duration: 360000000  // real-time: 1 unit = 1 second
        }

        vertexShader: 'qrc:/HuskarUI/shaders/husliquidglass.vert.qsb'
        fragmentShader: 'qrc:/HuskarUI/shaders/husliquidglass.frag.qsb'
    }
}
