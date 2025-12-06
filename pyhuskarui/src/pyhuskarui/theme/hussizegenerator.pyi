from PySide6.QtCore import QObject

QML_IMPORT_NAME: str
QML_IMPORT_MAJOR_VERSION: int

class HusSizeGenerator(QObject):
    def __init__(self, parent=None) -> None: ...
    @staticmethod
    def generateFontSize(font_size_base: float) -> list[float]: ...
    @staticmethod
    def generateFontLineHeight(font_size_base: float) -> list[float]: ...
