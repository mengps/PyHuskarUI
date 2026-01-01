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

HusIconButton {
    id: control

    property bool isError: false
    property bool noDisabledState: false

    objectName: '__HusCaptionButton__'
    leftPadding: 12 * sizeRatio
    rightPadding: 12 * sizeRatio
    active: down
    radiusBg.all: 0
    hoverCursorShape: Qt.ArrowCursor
    type: HusButton.Type_Text
    iconSize: parseInt(HusTheme.HusCaptionButton.fontSize)
    effectEnabled: false
    colorIcon: {
        if (enabled || noDisabledState) {
            return checked ? HusTheme.HusCaptionButton.colorIconChecked :
                             HusTheme.HusCaptionButton.colorIcon;
        } else {
            return HusTheme.HusCaptionButton.colorIconDisabled;
        }
    }
    colorBg: {
        if (enabled || noDisabledState) {
            if (isError) {
                return active ? HusTheme.HusCaptionButton.colorErrorBgActive:
                                hovered ? HusTheme.HusCaptionButton.colorErrorBgHover :
                                          HusTheme.HusCaptionButton.colorErrorBg;
            } else {
                return active ? HusTheme.HusCaptionButton.colorBgActive:
                                hovered ? HusTheme.HusCaptionButton.colorBgHover :
                                          HusTheme.HusCaptionButton.colorBg;
            }
        } else {
            return HusTheme.HusCaptionButton.colorBgDisabled;
        }
    }
}
