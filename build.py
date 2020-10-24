import os, shutil, mpy_cross
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
BUILD_SOURCE_DIR = os.path.join(ROOT_PATH, "mgui")
BUILD_TARGET_DIR = os.path.join(ROOT_PATH, "dist", "mgui")
SOURCE_LIST = [
    ("__init__.py", "__init__.mpy"),
    ("mgui_class.py", "mgui_class.mpy"),
    ("mgui_component.py", "mgui_component.mpy"),
    ("mgui_const.py", "mgui_const.mpy"),
    ("mgui_layout.py", "mgui_layout.mpy"),
    ("mgui_parser.py", "mgui_parser.mpy"),
    ("mgui_root.py", "mgui_root.mpy"),
    ("dev/framebuf.py", "dev/framebuf.mpy"),
]

shutil.rmtree(BUILD_TARGET_DIR, ignore_errors=True)
for source, target in SOURCE_LIST:
    print("source:", source, "->", target)
    source_path =  os.path.join(BUILD_SOURCE_DIR, source)
    target_path =  os.path.join(BUILD_TARGET_DIR, target)
    target_dir = os.path.dirname(target_path)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    proc = mpy_cross.run("-O3", "-o", target_path, source_path)
    proc.wait()
    print()
