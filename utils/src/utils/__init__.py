from pathlib import Path

from .update_resource import (
    uv_run,
    gen_qsbs,
    gen_qrc,
    gen_qmldir,
    update_qrcs,
    replace_license,
    gen_qmltypes,
    gen_pyis,
    del_pyis,
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

    del_pyis(huaskui)
    gen_pyis(huaskui)
    del_pyis(gallery)
    gen_pyis(gallery)


def package():
    cwd = (Path(__file__).parent / "../../../").resolve()
    gallery = cwd / "gallery"

    uv_run(
        [
            "nuitka",
            "--standalone",
            "--windows-console-mode=disable",
            "--show-memory",
            "--enable-plugin=pyside6",
            "--include-qt-plugins=qml",
            "--show-progress",
            "--output-dir=./package",
            "--output-folder-name=package",
            "--output-filename=PyHuskarUI-Gallery",
            f"--macos-app-icon={gallery}/images/huskarui_icon.icns"
            f"--windows-icon-from-ico={gallery}/images/huskarui_icon.ico",
            f"{gallery}/main.py",
        ]
    )
    
    excludeFiles = [
        "opengl32sw*",
        "qt6charts*",
        "qt6widgets*",
        "qt6web*",
        "qt6quick3d*",
        "qt6location*",
        "qt6positioning*",
        "qt6pdf*",
        "qt6quicktimeline",
        "qt6datavisualization*",
        "qt63d*",
        "qt6scxml*",
        "qt6virtualkeyboard*",
        "qt6sql*",
        "qt6multimedia*",
        "qt6shadertools*",
        "qt6spatialaudio*",
        "qt6statemachine*",
        "qt6test*",
        "qt6sensors*",
        "qt6remoteobjects*",
        "qt6texttospeech*",
        "qt6quicktest*",
        "qt6quicktimeline*",
        "qt6quickvectorimage*",
        "qt6quickcontrols2fusion*",
        "qt6quickcontrols2imagine*",
        "qt6quickcontrols2material*",
        "qt6quickcontrols2universal*",
        "PySide6/QtWidgets.pyd",
        "PySide6/qml/Qt3D",
        "PySide6/qml/Qt5Compat",
        "PySide6/qml/QtCharts",
        "PySide6/qml/QtDataVisualization",
        "PySide6/qml/QtLocation",
        "PySide6/qml/QtPositioning",
        "PySide6/qml/QtMultimedia",
        "PySide6/qml/QtQuick3D",
        "PySide6/qml/QtRemoteObjects",
        "PySide6/qml/QtScxml",
        "PySide6/qml/QtSensors",
        "PySide6/qml/QtTest",
        "PySide6/qml/QtTextToSpeech",
        "PySide6/qml/QtWebChannel",
        "PySide6/qml/QtWebEngine",
        "PySide6/qml/QtWebSockets",
        "PySide6/qml/QtWebView",
    ]

    for file in excludeFiles:
        for p in Path("./package/package.dist").glob(file):
            if p.is_dir():
                import shutil
                shutil.rmtree(p)
            else:
                p.unlink()
