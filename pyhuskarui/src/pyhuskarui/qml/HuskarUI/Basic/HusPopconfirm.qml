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
import QtQuick.Templates as T
import HuskarUI.Basic

HusPopover {
    id: control

    signal confirm()
    signal cancel()

    property string confirmText: ''
    property string cancelText: ''
    property Component confirmButtonDelegate: HusButton {
        animationEnabled: control.animationEnabled
        padding: 10
        topPadding: 4
        bottomPadding: 4
        text: control.confirmText
        type: HusButton.Type_Primary
        onClicked: control.confirm();
    }
    property Component cancelButtonDelegate: HusButton {
        animationEnabled: control.animationEnabled
        padding: 10
        topPadding: 4
        bottomPadding: 4
        text: control.cancelText
        type: HusButton.Type_Default
        onClicked: control.cancel();
    }

    footerDelegate: Item {
        implicitHeight: __rowLayout.implicitHeight

        RowLayout {
            id: __rowLayout
            anchors.right: parent.right
            spacing: 10
            visible: __confirmLoader.active || __cancelLoader.active

            Loader {
                id: __confirmLoader
                visible: active
                active: control.confirmText !== ''
                sourceComponent: control.confirmButtonDelegate
            }

            Loader {
                id: __cancelLoader
                visible: active
                active: control.cancelText !== ''
                sourceComponent: control.cancelButtonDelegate
            }
        }
    }

    objectName: '__HusPopconfirm__'
    themeSource: HusTheme.HusPopconfirm
}
