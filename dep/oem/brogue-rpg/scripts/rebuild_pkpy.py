import os, sys
import shutil

assert os.path.exists('pocketpy')

def run(cmd: str):
    print(cmd)
    assert os.system(cmd) == 0

os.chdir('pocketpy')
run('git pull origin main')
run('git submodule update --init --recursive')

shutil.rmtree('build', ignore_errors=True)

args = [
    'python cmake_build.py Release',
    '-DPK_BUILD_STATIC_MAIN=ON',
    '-DPK_ENABLE_DETERMINISM=ON',
    '-DPK_ENABLE_WATCHDOG=ON',
    '-DPK_ENABLE_MIMALLOC=OFF',
]

run(' '.join(args))

os.chdir('..')

