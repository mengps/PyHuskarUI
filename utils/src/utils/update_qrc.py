import os
import subprocess
from pathlib import Path


def generate_qrc(dir_name: Path) -> None:
    """generate qrc file"""


def generate_rc(dir_name: Path) -> None:
    """generate *_rc.py file"""

    qrc_files = [
        file for file in os.listdir(dir_name) if file.endswith(".qrc")
    ]
    for qrc_file in qrc_files:
        qrc_name = os.path.splitext(qrc_file)[0]
        qrc_file = os.path.join(dir_name, qrc_file)
        output_file = os.path.join(dir_name, qrc_name + "_rc.py")

        if not os.path.exists(qrc_file):
            print(f"qrc file not found: {qrc_file}")
            return

        try:
            subprocess.run(
                ["pyside6-rcc", qrc_file, "-o", output_file],
                check = True,
                capture_output = True,
                text = True,
            )
            print(f"successfully generated: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"generate_resource error: {e}")
            print(f"error output: {e.stderr}")
        except FileNotFoundError:
            print(f"pyside6-rcc not found!")


if __name__ == "__main__":
    from importlib.resources import files

    gallery = (Path(__file__).parent / "../../../gallery").resolve()

    generate_rc(gallery)
    generate_rc(files("pyhuskarui"))
