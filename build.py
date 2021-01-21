import os, sys, subprocess
from mpypack import cli as mpypack_cli

PYTHON_EXE = sys.executable
POPEN_BASE_ARGS = [PYTHON_EXE, "-m", "mpypack.cli"]

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
# BUILD_SOURCE_DIR = os.path.join(ROOT_PATH, "mgui")
# BUILD_TARGET_DIR = os.path.join(ROOT_PATH, "dist", "mgui")
BOARD_TARGET_DIR = "/lib/mgui"

MPYPACK_CONFIG_FILE = os.path.join(ROOT_PATH, mpypack_cli.DEFAULT_CONFIG_FILE)
mpypack_cli.conf.read(MPYPACK_CONFIG_FILE)

def build():
    cmd = list(POPEN_BASE_ARGS)
    cmd.append('build')
    print('building...')
    subprocess.run(cmd)

def flash():
    fe = mpypack_cli.get_file_explorer()
    with fe:
        fe.mkdirs(mpypack_cli.get_config(mpypack_cli.CONFIG_OPTION_REMOTE, BOARD_TARGET_DIR))
    cmd = list(POPEN_BASE_ARGS)
    cmd.append('sync')
    print('flashing...')
    subprocess.run(cmd)

def test():
    flash()
    fe = mpypack_cli.get_file_explorer()
    with fe:
        with open('testmcu.py', 'rb') as f:
            fe.upload('/test.py', f.read())
    cmd = list(POPEN_BASE_ARGS)
    cmd.append('repl')
    print('[REPL MODE]')
    subprocess.run(cmd)

if __name__ == "__main__":
    build()
    if len(sys.argv) > 1:
        if sys.argv[1] == "flash":
            flash()
        if sys.argv[1] == "test":
            test()
