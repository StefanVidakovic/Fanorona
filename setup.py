import cx_Freeze
import pygame




executables = [cx_Freeze.Executable("pygameVideo15.py")]

cx_Freeze.setup(
    name="Fanorona",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["racecar.png"]}},
    executables = executables

    )
