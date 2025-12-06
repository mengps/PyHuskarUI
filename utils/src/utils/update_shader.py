import os
import subprocess
from pathlib import Path

from loguru import logger


def generate_qsb(dir_name: Path):
    """generate qsb file"""

    for file in os.listdir(dir_name):
        file_path = os.path.join(dir_name, file)
        if os.path.isdir(file_path):
            generate_qsb(file_path)

    shader_files = [
        file for file in os.listdir(dir_name)
        if file.endswith(".vert") or file.endswith(".frag")
    ]

    if not shader_files:
        return

    for shader_file in shader_files:
        shader_file = os.path.join(dir_name, shader_file)
        output_file = shader_file + ".qsb"

        if not os.path.exists(shader_file):
            logger.error(f"shader file not found: {shader_file}")
            return

        try:
            subprocess.run(
                [
                    "pyside6-qsb",
                    "--glsl",
                    "100es,120,150",
                    "--hlsl",
                    "50",
                    "--msl",
                    "12",
                    "-o",
                    output_file,
                    shader_file,
                ],
                check = True,
                capture_output = True,
                text = True,
            )
            logger.error(f"successfully generated: {output_file}")
        except subprocess.CalledProcessError as e:
            logger.error(f"generate_resource error: {e}")
            logger.error(f"error output: {e.stderr}")
        except FileNotFoundError:
            logger.error("pyside6-rcc not found!")


if __name__ == "__main__":
    from importlib.resources import files

    gallery = (Path(__file__).parent / "../../../gallery").resolve()

    generate_qsb(gallery)
    generate_qsb(files("pyhuskarui"))
