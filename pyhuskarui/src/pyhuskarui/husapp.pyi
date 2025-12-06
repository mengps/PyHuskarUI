from .qml_rc import *
from .resources_rc import *
from .shaders_rc import *
from .utils.husapi import *
from .utils.husasynchasher import *
from .theme.hustheme import *
from .theme.huscolorgenerator import *
from .theme.husthemefunctions import *
from .theme.husradiusgenerator import *
from .theme.hussizegenerator import *
from .theme.hussystemthemehelper import *
from .controls.husiconfont import *
from .controls.husqrcode import *
from .controls.husrectangle import *
from .controls.huswatermark import *
from .controls.huswindowagent import *
from PySide6.QtCore import QObject
from PySide6.QtQml import QQmlEngine as QQmlEngine

QML_IMPORT_NAME: str
QML_IMPORT_MAJOR_VERSION: int

class HusApp(QObject):
    def __init__(self, parent: QObject = None) -> None: ...
    @staticmethod
    def initialize(engine: QQmlEngine) -> None: ...
    @staticmethod
    def libName() -> str: ...
    @staticmethod
    def libVersion() -> str: ...
