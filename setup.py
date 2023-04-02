import sys
import os
from cx_Freeze import setup, Executable

files = ['Dani-Bank_small.ico']

target = Executable(
    script = "main.py",
    base = "Win32GUI",
    icon = "Dani-Bank_small.ico")

setup(
    name = "Dani Bank",
    version = "2.0",
    description = "Modern GUI Banking System",
    author = "Hiruy Habtamu",
    options = {'build_exe': {'include_files':files}},
    executables = [target])
