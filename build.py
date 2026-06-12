# in cmd, run: py build.py build

from cx_Freeze import setup, Executable

build_options = {
# Only real packages here
"packages": ["pygame", "tkinter"],          # add "tkinter" only if you actually import it
# Single-file modules go here
"includes": ["os", "sys", "csv", "random", "math", "datetime"],
"include_files": [("assets", "assets")],
"excludes": ["numpy", "pip", "cx_Freeze"],
# Uncomment if you still hit RecursionError:
# "zip_include_packages": []
}

executables = [
Executable(
"rod-and-disk.py",            # rename your script file accordingly
icon="icon.ico",
base="Win32GUI",              # for a GUI app on Windows; remove if you want a console
target_name="rod-and-disk-demo-yiling.exe"
)
]

setup(
name="Rod and Disk",
options={"build_exe": build_options},
executables=executables
)