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

from PySide6.QtCore import (QObject, Property, Signal, QUrl, QByteArray,
                            QThreadPool, QBuffer, QRunnable, QIODevice,
                            QLoggingCategory, QEnum)
from PySide6.QtNetwork import QNetworkRequest, QNetworkReply
from PySide6.QtQml import QmlElement, qmlEngine
from PySide6.QtCore import QCryptographicHash
from loguru import logger

# 创建日志分类
lcHusAsyncHasher = QLoggingCategory("huskarui.basic.asynchasher")

QML_IMPORT_NAME = "HuskarUI.Basic"
QML_IMPORT_MAJOR_VERSION = 1


class AsyncRunnable(QObject, QRunnable):
    """异步哈希计算任务"""

    progress = Signal(int, int)  # processed, total
    finished = Signal(str)  # hash result

    def __init__(self, device: QIODevice,
                 algorithm: QCryptographicHash.Algorithm):
        QObject.__init__(self)
        QRunnable.__init__(self)
        self._device = device
        self._algorithm = algorithm
        self._stop = False
        self.setAutoDelete(False)

    def cancel(self):
        """取消任务"""
        self._stop = True

    def run(self):
        """执行哈希计算"""
        if not self._device:
            return

        try:
            chunk_size = 4 * 1024 * 1024  # 4MB chunks
            hash_obj = QCryptographicHash(self._algorithm)
            processed = 0
            total = self._device.size()

            while not self._device.atEnd():
                if self._stop:
                    self._device.deleteLater()
                    return

                # 读取数据块
                read_size = min(chunk_size, total - processed)
                data = self._device.read(read_size)
                if not data:
                    break

                hash_obj.addData(data)
                processed += len(data)
                self.progress.emit(processed, total)

            # 发送最终结果
            result = hash_obj.result().toHex().toUpper().toStdString()
            self.finished.emit(result)

        except Exception as e:
            logger.error(f"Hash calculation error: {e}")
        finally:
            self._device.deleteLater()


@QmlElement
class HusAsyncHasher(QObject):
    """异步哈希计算器"""

    algorithmChanged = Signal()
    asynchronousChanged = Signal()
    hashValueChanged = Signal()
    hashLengthChanged = Signal()
    sourceChanged = Signal()
    sourceTextChanged = Signal()
    sourceDataChanged = Signal()
    sourceObjectChanged = Signal()
    hashProgress = Signal(int, int)  # processed, total
    started = Signal()
    finished = Signal()

    QEnum(QCryptographicHash.Algorithm)

    def __init__(self, parent = None):
        super().__init__(parent)

        # 初始化私有变量
        self._algorithm = QCryptographicHash.Md5
        self._asynchronous = True
        self._hashValue = ""
        self._source = QUrl()
        self._sourceText = ""
        self._sourceData = QByteArray()
        self._sourceObject = None

        # 其他私有变量
        self._reply = None
        self._runnable = None

    def _cleanupRunnable(self):
        """清理运行中的任务"""
        if self._runnable:
            self._runnable.cancel()
            self._runnable.disconnect()
            self._runnable.deleteLater()
            self._runnable = None

    @Property(QCryptographicHash.Algorithm, notify = algorithmChanged)
    def algorithm(self) -> QCryptographicHash.Algorithm:
        return self._algorithm

    @algorithm.setter
    def algorithm(self, algorithm: QCryptographicHash.Algorithm):
        if self._algorithm != algorithm:
            self._algorithm = algorithm
            self.algorithmChanged.emit()
            self.hashLengthChanged.emit()

    @Property(bool, notify = asynchronousChanged)
    def asynchronous(self) -> bool:
        return self._asynchronous

    @asynchronous.setter
    def asynchronous(self, isAsync: bool):
        if self._asynchronous != isAsync:
            self._asynchronous = isAsync
            self.asynchronousChanged.emit()

    @Property(str, notify = hashValueChanged)
    def hashValue(self) -> str:
        return self._hashValue

    @Property(int, notify = hashLengthChanged)
    def hashLength(self) -> int:
        return QCryptographicHash.hashLength(self._algorithm)

    @Property(QUrl, notify = sourceChanged)
    def source(self) -> QUrl:
        return self._source

    @source.setter
    def source(self, source: QUrl):
        if self._source != source:
            self._source = source
            self.sourceChanged.emit()

            self._cleanupRunnable()

            if source.isLocalFile():
                # 本地文件
                from PySide6.QtCore import QFile
                file = QFile(source.toLocalFile())
                if file.open(QIODevice.ReadOnly):
                    self.started.emit()
                    if self._asynchronous:
                        # 异步计算
                        self._runnable = AsyncRunnable(file, self._algorithm)
                        self._runnable.finished.connect(self._setHashValue)
                        self._runnable.progress.connect(self.hashProgress)
                        QThreadPool.globalInstance().start(self._runnable)
                    else:
                        # 同步计算
                        hash_obj = QCryptographicHash(self._algorithm)
                        hash_obj.addData(file)
                        self._setHashValue(
                            hash_obj.result().toHex().toUpper().toStdString())
                        file.deleteLater()
                else:
                    logger.error(f"File Error: {file.errorString()}")
                    file.deleteLater()
            else:
                # 网络文件
                if self._reply:
                    self._reply.abort()

                self.started.emit()
                
                if qmlEngine(self):
                    manager = qmlEngine(self).networkAccessManager()
                    if manager:
                        self._reply = manager.get(QNetworkRequest(source))
                        self._reply.finished.connect(self._on_network_reply_finished)
                    else:
                        logger.error(
                                "HusAsyncHasher without QmlEngine, we cannot get QNetworkAccessManager!"
                            )

    def _on_network_reply_finished(self):
        """网络请求完成"""
        if self._reply.error() == QNetworkReply.NoError:
            if self._asynchronous:
                self._runnable = AsyncRunnable(self._reply, self._algorithm)
                self._runnable.finished.connect(self._setHashValue)
                self._runnable.progress.connect(self.hashProgress)
                QThreadPool.globalInstance().start(self._runnable)
            else:
                hash_obj = QCryptographicHash(self._algorithm)
                hash_obj.addData(self._reply.readAll())
                self._setHashValue(
                    hash_obj.result().toHex().toUpper().toStdString())
                self._reply.deleteLater()
        else:
            logger.error(f"HTTP Request Error: {self._reply.errorString()}")
            self._reply.deleteLater()

        self._reply = None

    @Property(str, notify = sourceTextChanged)
    def sourceText(self) -> str:
        return self._sourceText

    @sourceText.setter
    def sourceText(self, sourceText: str):
        if self._sourceText != sourceText:
            self._sourceText = sourceText
            self.sourceTextChanged.emit()

            self._cleanupRunnable()
            self.started.emit()

            if self._asynchronous:
                # 异步计算
                buffer = QBuffer()
                buffer.setData(sourceText.encode("utf-8"))
                buffer.open(QIODevice.ReadOnly)
                self._runnable = AsyncRunnable(buffer, self._algorithm)
                self._runnable.finished.connect(self._setHashValue)
                self._runnable.progress.connect(self.hashProgress)
                QThreadPool.globalInstance().start(self._runnable)
            else:
                # 同步计算
                hash_obj = QCryptographicHash(self._algorithm)
                hash_obj.addData(sourceText.encode("utf-8"))
                self._setHashValue(
                    hash_obj.result().toHex().toUpper().toStdString())

    @Property(QByteArray, notify = sourceDataChanged)
    def sourceData(self) -> QByteArray:
        return self._sourceData

    @sourceData.setter
    def sourceData(self, sourceData: QByteArray):
        if self._sourceData != sourceData:
            self._sourceData = sourceData
            self.sourceDataChanged.emit()

            self._cleanupRunnable()
            self.started.emit()

            if self._asynchronous:
                # 异步计算
                buffer = QBuffer()
                buffer.setData(sourceData)
                buffer.open(QIODevice.ReadOnly)
                self._runnable = AsyncRunnable(buffer, self._algorithm)
                self._runnable.finished.connect(self._setHashValue)
                self._runnable.progress.connect(self.hashProgress)
                QThreadPool.globalInstance().start(self._runnable)
            else:
                # 同步计算
                hash_obj = QCryptographicHash(self._algorithm)
                hash_obj.addData(sourceData)
                self._setHashValue(
                    hash_obj.result().toHex().toUpper().toStdString())

    @Property(QObject, notify = sourceObjectChanged)
    def sourceObject(self) -> QObject:
        return self._sourceObject

    @sourceObject.setter
    def sourceObject(self, sourceObject: QObject):
        if self._sourceObject != sourceObject:
            self._sourceObject = sourceObject
            self.sourceObjectChanged.emit()
            self.started.emit()
            
            hash_obj = QCryptographicHash(self._algorithm)
            hash_obj.addData(str(id(sourceObject)).encode("utf-8"))
            self._setHashValue(
                hash_obj.result().toHex().toUpper().toStdString())

    def _setHashValue(self, value: str):
        """设置哈希值（内部方法）"""
        self._hashValue = value
        self.hashValueChanged.emit()
        self.finished.emit()

    # 运算符重载
    def __eq__(self, other: "HusAsyncHasher") -> bool:
        return other.getHashValue() == self._hashValue

    def __ne__(self, other: "HusAsyncHasher") -> bool:
        return not self.__eq__(other)

    # 静态方法
    @staticmethod
    def hash(data: QByteArray,
             algorithm: QCryptographicHash.Algorithm) -> QByteArray:
        """静态哈希计算方法"""
        hash_obj = QCryptographicHash(algorithm)
        hash_obj.addData(data)
        return hash_obj.result()
