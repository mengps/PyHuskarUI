from PySide6.QtCore import QObject

QML_IMPORT_NAME: str
QML_IMPORT_MAJOR_VERSION: int

class HusRadiusGenerator(QObject):
    def __init__(self, parent=None) -> None: ...
    @staticmethod
    def generateRadius(radius_base: int) -> list[int]: ...
