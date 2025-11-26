from pathlib import Path
from importlib.resources import files


def generate_qmldir(qml_path: Path, module_name: str, prefer: str,
                    version: str, qml_prefix: str) -> None:
    """generate qmldir file"""
    qmldir_file = Path(qml_path / "qmldir")
    with open(qmldir_file, "w", encoding = "utf-8") as qmldir:
        qmldir.write(f"module {module_name}\n")
        qmldir.write(f"prefer {prefer}\n\n")

        for file in Path(qml_path).iterdir():
            if not file.is_file():
                continue
            file_name = file.name
            file_base_name = file.with_suffix("").name
            if file_base_name == "qmldir":
                continue
            qmldir.write(
                f"{file_base_name} {version} {qml_prefix}/{file_name}\n")

    print(f"successfully generated: {qmldir_file}")


if __name__ == "__main__":
    generate_qmldir(files("pyhuskarui") / "qml/HuskarUI/Basic",
                    "HuskarUI.Basic", ":qt/", "1.0", "qml/HuskarUI/Basic")
