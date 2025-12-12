# -*- coding: UTF-8 -*-

"""
!/usr/bin/python 3.12
==============================================================================
@Time    : 2025/12/12 21:48
@Author  : Ephemeral
@Email   : mai.ephemeral@qq.com
@PROJECT : PyHuskarUI
@File    : logger
@Software: PyCharm
@Version:  ***
@Description: ***
==============================================================================
"""
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