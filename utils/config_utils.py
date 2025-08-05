import os
import sys
import shutil
from pathlib import Path

def resource_path(relative_path: str) -> str:
  # Resolve path for bundled data when using PyInstaller --onefile
  if hasattr(sys, "_MEIPASS"):
    return os.path.join(sys._MEIPASS, relative_path)
  return os.path.abspath(relative_path)

def ensure_user_stylesheet(app_name="Draco", filename="style.css") -> str:
  xdg = os.environ.get("XDG_CONFIG_HOME")
  if xdg:
    config_dir = Path(xdg) / app_name
  else:
    config_dir = Path.home() / ".config" / app_name

  config_dir.mkdir(parents=True, exist_ok=True)

  user_stylesheet = config_dir / filename

  if not user_stylesheet.exists():
    bundled = resource_path(filename)
    try:
      shutil.copyfile(bundled, user_stylesheet)
      print(f"Copied default stylesheet to {user_stylesheet}")
    except Exception as e:
      print(f"Failed to copy bundled stylesheet to user config: {e}")
  return str(user_stylesheet)
