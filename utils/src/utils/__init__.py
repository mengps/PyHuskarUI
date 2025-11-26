from importlib.resources import files
from pathlib import Path

from .update_qmldir import generate_qmldir
from .update_qrc import generate_rc
from .update_shader import generate_qsb


def init():
    gallery = (Path(__file__).parent / "../../../gallery").resolve()

    generate_qmldir(files("pyhuskarui") / "qml/HuskarUI/Basic",
                    "HuskarUI.Basic", ":qt/", "1.0", "qml/HuskarUI/Basic")

    generate_qsb(gallery)
    generate_qsb(files("pyhuskarui"))

    generate_rc(gallery)
    generate_rc(files("pyhuskarui"))
