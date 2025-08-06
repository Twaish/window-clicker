import datetime

from cx_Freeze import Executable, setup

from settings import APP_NAME, BUILD_VERSION

build_options = {
  "packages": [
    "pages.macro_page",
    "pages.window_clicker_page",
  ],
  "silent_level": 1,
  "silent": True,
  "zip_exclude_packages": ["*"],
  "build_exe": "dist",
  "include_msvcr": True,
  "optimize": 1,
  "include_files": [
    ("assets/logo.png", "assets/logo.png"),
    ("assets/style.css", "assets/style.css"),
  ],
}

executables = [
  Executable(
    "main.py",
    base="gui",
    icon="assets/logo.ico",
    shortcut_name=APP_NAME,
    shortcut_dir="MyProgramMenu",
    copyright=f"Copyright (C) {datetime.datetime.now().year} Twaish",
    target_name=APP_NAME.lower(),
  ),
]

setup(
  name=APP_NAME.lower(),
  version=BUILD_VERSION,
  author="Twaish",
  description=f"{APP_NAME} - Macro Application",
  executables=executables,
  options={
    "build_exe": build_options,
  },
)