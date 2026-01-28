import sys
from pathlib import Path
from shutil import rmtree

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
from .extract_docs import extract_all_docs, save_docs_to_json
from .generate_markdown import generate_markdown


def init():
    cwd = (Path(__file__) / "../../../../").resolve()
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
    cwd = (Path(__file__) / "../../../../").resolve()
    gallery = cwd / "gallery"
    dist = Path("./package/package.dist")
    target = dist.parent / "PyHuskarUI-Gallery"
    args = [
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
        f"--macos-app-icon={gallery}/images/huskarui_new_square.icns",
        f"--windows-icon-from-ico={gallery}/images/huskarui_new_square.ico",
    ]
    if sys.platform.startswith("darwin"):
        args.extend(["--macos-create-app-bundle", "--disable-ccache"])
        dist = Path("./package/package.app")
        target = dist.parent / "PyHuskarUI-Gallery.app"

    args.extend(
        [
            f"{gallery}/main.py",
        ]
    )

    uv_run(args)

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
        for p in dist.glob(file):
            if p.is_dir():
                rmtree(p)
            else:
                p.unlink()
    dist.rename(target)


def gen_docs():
    cwd = (Path(__file__) / "../../../../").resolve()
    docs_dir = cwd / "docs"
    if docs_dir.exists():
        rmtree(docs_dir)
    examples_dir = cwd / "gallery/qml/Examples"
    output_meta_path = cwd / "docs/guide.metainfo.json"
    docs = extract_all_docs(examples_dir, cwd)
    save_docs_to_json(docs, output_meta_path)
    generate_markdown(str(output_meta_path))
