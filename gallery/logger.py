# PyHuskarUI
#
# Copyright (C) 2025 mengps (MenPenS)
# https://github.com/mengps/PyHuskarUI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import threading
from pathlib import Path

from PySide6.QtCore import QtMsgType, qInstallMessageHandler
from loguru import logger


def __getLevelByMsgType(msg_type):
    return {
        QtMsgType.QtFatalMsg: "CRITICAL",
        QtMsgType.QtCriticalMsg: "ERROR",
        QtMsgType.QtWarningMsg: "WARNING",
        QtMsgType.QtInfoMsg: "INFO",
        QtMsgType.QtDebugMsg: "DEBUG",
    }.get(msg_type, "DEBUG")


def __messageHandler(msg_type, context, message):
    if message == "Retrying to obtain clipboard.":
        return
    level = __getLevelByMsgType(msg_type)

    _str = ""
    if context.file:
        _tmp = Path(context.file).name
        _str = f"[{_tmp}:{context.line}]"

    msg = f"{_str}[{threading.get_ident()}]:{message}"

    logger.log(level, msg)


qInstallMessageHandler(__messageHandler)