import sys
from cx_Freeze import setup, Executable

build_exe_options = {}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="YTPL",
      version="0.7",
      description="My GUI application!",
      options={"build_exe": build_exe_options},
      executables=[Executable("app.py", base=base)])
