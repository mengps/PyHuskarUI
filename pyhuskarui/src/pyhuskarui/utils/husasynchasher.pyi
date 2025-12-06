from PySide6.QtCore import QByteArray, QCryptographicHash, QIODevice, QObject, QRunnable
from _typeshed import Incomplete

lcHusAsyncHasher: Incomplete
QML_IMPORT_NAME: str
QML_IMPORT_MAJOR_VERSION: int

class AsyncRunnable(QObject, QRunnable):
    progress: Incomplete
    finished: Incomplete
    def __init__(self, device: QIODevice, algorithm: QCryptographicHash.Algorithm) -> None: ...
    def cancel(self) -> None: ...
    def run(self) -> None: ...

class HusAsyncHasher(QObject):
    algorithmChanged: Incomplete
    asynchronousChanged: Incomplete
    hashValueChanged: Incomplete
    hashLengthChanged: Incomplete
    sourceChanged: Incomplete
    sourceTextChanged: Incomplete
    sourceDataChanged: Incomplete
    sourceObjectChanged: Incomplete
    hashProgress: Incomplete
    started: Incomplete
    finished: Incomplete
    def __init__(self, parent=None) -> None: ...
    def hashValue(self) -> str: ...
    def hashLength(self) -> int: ...
    def __eq__(self, other: HusAsyncHasher) -> bool: ...
    def __ne__(self, other: HusAsyncHasher) -> bool: ...
    @staticmethod
    def hash(data: QByteArray, algorithm: QCryptographicHash.Algorithm) -> QByteArray: ...
