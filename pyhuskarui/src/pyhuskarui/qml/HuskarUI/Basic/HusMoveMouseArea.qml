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

MouseArea {
    id: root

    property var target: undefined
    property real minimumX: -Number.MAX_VALUE
    property real maximumX: Number.MAX_VALUE
    property real minimumY: -Number.MAX_VALUE
    property real maximumY: Number.MAX_VALUE

    objectName: '__HusMoveMouseArea__'
    onClicked: (mouse) => mouse.accepted = false;
    onPressed:
        (mouse) => {
            __private.startPos = Qt.point(mouse.x, mouse.y);
            cursorShape = Qt.SizeAllCursor;
        }
    onReleased:
        (mouse) => {
            __private.startPos = Qt.point(mouse.x, mouse.y);
            cursorShape = Qt.ArrowCursor;
        }
    onPositionChanged:
        (mouse) => {
            if (pressed) {
                __private.offsetPos = Qt.point(mouse.x - __private.startPos.x, mouse.y - __private.startPos.y);
                if (target) {
                    // x
                    if (minimumX != Number.NaN && minimumX > (target.x + __private.offsetPos.x)) {
                        target.x = minimumX;
                    } else if (maximumX != Number.NaN && maximumX < (target.x + __private.offsetPos.x)) {
                        target.x = maximumX;
                    } else {
                        target.x = target.x + __private.offsetPos.x;
                    }
                    // y
                    if (minimumY != Number.NaN && minimumY > (target.y + __private.offsetPos.y)) {
                        target.y = minimumY;
                    } else if (maximumY != Number.NaN && maximumY < (target.y + __private.offsetPos.y)) {
                        target.y = maximumY;
                    } else {
                        target.y = target.y + __private.offsetPos.y;
                    }
                }
            }
        }

    QtObject {
        id: __private
        property point startPos: Qt.point(0, 0)
        property point offsetPos: Qt.point(0, 0)
    }
}
