from pathlib import Path

from .update_resource import (
    gen_qsbs,
    gen_qrc,
    gen_qmldir,
    update_qrcs,
    replace_license,
    gen_qmltypes,
)


def init():
    cwd = (Path(__file__).parent / "../../../").resolve()
    gallery = cwd / "gallery"
    huaskui = cwd / "pyhuskarui" / "src" / "pyhuskarui"

    replace_license(huaskui / "qml")

    gen_qsbs(huaskui / "shaders")
    gen_qrc(huaskui / "shaders", "/HuskarUI")
    gen_qmldir(huaskui / "qml", "HuskarUI.Basic", "1.0")
    gen_qrc(huaskui / "qml", "/qt")
    gen_qrc(huaskui / "resources", "/HuskarUI")
    update_qrcs(huaskui)

    gen_qsbs(gallery / "shaders")
    gen_qrc(gallery / "images", "/Gallery")
    gen_qrc(gallery / "shaders", "/Gallery")
    gen_qrc(gallery / "qml", "/Gallery")
    update_qrcs(gallery)

    gen_qmltypes(huaskui, "HuskarUI")
    gen_qmltypes(gallery, "Gallery")
