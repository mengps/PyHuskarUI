import os
import subprocess

def generate_qsb(dir_name):
    """generate qsb file"""
    
    for file in os.listdir(dir_name):
        file_path = os.path.join(dir_name, file)
        if os.path.isdir(file_path):
            generate_qsb(file_path)
    
    shader_files = [file for file in os.listdir(dir_name) if file.endswith(".vert") or file.endswith(".frag")]
    
    if not shader_files:
        return
            
    for shader_file in shader_files:
        shader_file = os.path.join(dir_name, shader_file)
        output_file = shader_file + ".qsb"

        if not os.path.exists(shader_file):
            print(f"shader file not found: {shader_file}")
            return

        try:
            subprocess.run(["pyside6-qsb", 
                            "--glsl", "100es,120,150", 
                            "--hlsl", "50", 
                            "--msl", "12", "-o", 
                            output_file, shader_file],
                           check = True,
                           capture_output = True,
                           text = True)
            print(f"successfully generated: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"generate_resource error: {e}")
            print(f"error output: {e.stderr}")
        except FileNotFoundError:
            print(f"pyside6-rcc not found!")


if __name__ == "__main__":
    generate_qsb("gallery")
    generate_qsb("huskarui")
