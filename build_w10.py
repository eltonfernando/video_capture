# -*- coding: utf-8 -*-
import os
from cx_Freeze import setup, Executable
from glob import glob

VERSION = "0.0.3"
for data_db in glob(os.path.join("save_locale", "*.db")):
    os.remove(data_db)

if not os.path.isdir("save_locale"):
    os.mkdir("save_locale")
import numpy


GUI2Exe_Target_1 = Executable(
    script="main.py",
    base="Win32GUI",
    target_name="videoCapure.exe",
)
excludes = ["tkinter"]
includes = ["cv2"]
# namespace_packages=["multiprocessing.pool"]
packages = ["cv2", "numpy"]
path = []

include_files = []  # , (torch_path, "lib")]
setup(
    version=VERSION,
    description="captura de video",
    author="Elton Fernandes dos Santos",
    author_email="eltonfernando90@email.com",
    name="VideoCapture",
    options={
        "build_exe": {
            "includes": includes,
            "excludes": excludes,
            "packages": packages,
            "include_msvcr": True,
            # "namespace_packages":namespace_packages,
            "path": path,
            "include_files": include_files,
        }
    },
    executables=[GUI2Exe_Target_1],
)
