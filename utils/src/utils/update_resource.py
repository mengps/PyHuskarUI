import itertools
import subprocess
from pathlib import Path

from loguru import logger


def uv_run(cmd: list):
    uv_cmd = ["uv", "run"]
    uv_cmd.extend(cmd)
    try:
        subprocess.run(
            uv_cmd,
            check = True,
            capture_output = True,
            text = True,
        )
        logger.success(
            f"successfully updated: {' '.join([str(i) for i in cmd])}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error: {e.stderr}")
    except FileNotFoundError:
        logger.error(f"{cmd[2]} not found!")


def gen_qsb(p: Path | str):
    p = Path(p)
    uv_run([
        "pyside6-qsb",
        "--glsl",
        "100 es,120,150",
        "--hlsl",
        "50",
        "--msl",
        "12",
        p,
        "-o",
        p.parent / f"{p.name}.qsb",
    ])


def gen_qsbs(path: Path | str):
    path = Path(path)
    p1 = path.rglob("*.vert")
    p2 = path.rglob("*.frag")
    list(map(gen_qsb, itertools.chain(p1, p2)))


def update_qrc(qrc: Path | str):
    qrc = Path(qrc)
    uv_run([
        "pyside6-rcc",
        qrc,
        "-o",
        qrc.parent / f"{qrc.stem}_rc.py",
    ])


def update_qrcs(path: Path | str):
    path = Path(path)
    qrcs = path.rglob("*.qrc")
    list(map(update_qrc, qrcs))


def update_ts_to_qm(path: Path | str,
                    app_name: str = "app",
                    to_dir: Path | str = ""):
    path = Path(path)
    to_dir = Path(to_dir) if to_dir else path / "i18n"
    to_dir.mkdir(parents = True, exist_ok = True)
    locale_datas = ["zh_CN", "en_US", "zh_TW"]
    pys = path.rglob("*.py")

    for locale in locale_datas:
        p_ts = to_dir / f"{app_name}_{locale}.ts"

        uv_run([
            "pyside6-lupdate",
            f"{path}/resource.qrc",
            *pys,
            "-ts",
            p_ts,
            # "-no-obsolete",
        ])

        uv_run(["pyside6-lrelease", p_ts])


def gen_qmldir(
    folder_path: Path | str,
    qml_module: str = "app",
    version: str = "1.0",
    qml_prefix: str = ":qt/",
):
    folder_path = Path(folder_path)

    _ps = list(folder_path.rglob("*.qml"))
    qmldir = _ps[0].parent / "qmldir"

    with qmldir.open("w", encoding = "utf-8") as f:
        f.write(
            f"module {qml_module}\ntypeinfo plugins.qmltypes\nprefer {qml_prefix}\n"
        )
        for qml in _ps:
            f.write(
                f"{qml.stem} {version} {qml.relative_to(folder_path.parent).as_posix()}\n"
            )


def gen_qrc(path: Path | str, qrc_prefix: str = "/qt/qml"):
    path = Path(path)
    res = path
    qrc = path.parent / f"{path.stem}.qrc"
    excluded_suffixes = [
        ".ui",
        ".qrc",
        ".vert",
        ".frag",
        ".ts",
        ".py",
        ".pyc",
    ]
    resource = [
        i.relative_to(path.parent).as_posix() for i in res.rglob("*")
        if all([i.suffix not in excluded_suffixes,
                i.is_file()])
    ]

    with qrc.open("w", encoding = "utf-8") as f:
        f.write("<RCC>\n")
        f.write(f'    <qresource prefix="{qrc_prefix}">\n')
        for _p in resource:
            f.write(f"        <file>{_p}</file>\n")
        f.write("    </qresource>\n")
        f.write("</RCC>\n")


def replace_license(path: Path | str):
    """
    将 path 下的所有文件开头的 MIT 版权声明替换为 Apache 2.0 版权声明

    Args:
        path: 要处理的目录路径
    """
    path = Path(path)
    apache_license = """/*
 * PyHuskarUI
 *
 * Copyright (C) 2025 mengps (MenPenS)
 * https://github.com/mengps/PyHuskarUI
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
"""

    for file_path in path.rglob("*.qml"):
        try:
            with file_path.open("r", encoding = "utf-8") as f:
                lines = f.readlines()

            if "PyHuskarUI" in lines[0] or "PyHuskarUI" in lines[1]:
                continue

            new_content = apache_license + "".join(lines[22:])

            with file_path.open("w", encoding = "utf-8") as f:
                f.write(new_content)

            logger.success(f"updated license in {file_path}")

        except Exception as e:
            logger.error(f"error processing license {file_path}: {e}")


if __name__ == "__main__":
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
    gen_qrc(gallery / 'images', '/Gallery')
    gen_qrc(gallery / 'shaders', '/Gallery')
    gen_qrc(gallery / 'qml', '/Gallery')
    update_qrcs(gallery)
