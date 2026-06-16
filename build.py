# in cmd, run: py build.py build

from cx_Freeze import setup, Executable

build_options = {
"packages": ["pygame", "tkinter"],
"includes": ["os", "sys", "csv", "random", "math", "datetime"],
# "include_files": [("assets", "assets")],
"excludes": ["numpy", "pip", "cx_Freeze"]
}

executables = [
Executable(
"rod-and-disk.py",
icon="icon.ico",
base=None,
target_name="rod-and-disk-python.exe"
)
]

setup(
name="Rod and Disk",
options={"build_exe": build_options},
executables=executables
)