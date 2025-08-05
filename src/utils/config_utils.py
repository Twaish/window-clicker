import os
import sys
import shutil
from pathlib import Path
from .FALLBACK_CSS import FALLBACK_CSS
from settings import DEFAULT_CONFIG_DIR, DEFAULT_STYLES_FILENAME

def resource_path(relative_path: str) -> str:
  # Resolve path for bundled data when using PyInstaller --onefile
  if hasattr(sys, "_MEIPASS"):
    return os.path.join(sys._MEIPASS, relative_path)
  return os.path.abspath(relative_path)

def ensure_user_stylesheet(assets_dir=None) -> str:
  # Ensure the config directory exists
  DEFAULT_CONFIG_DIR.mkdir(parents=True, exist_ok=True)

  user_stylesheet = DEFAULT_CONFIG_DIR / DEFAULT_STYLES_FILENAME
  if user_stylesheet.exists():
    print(f"Using existing stylesheet at {user_stylesheet}")
    return str(user_stylesheet)
  
  # Try copy from bundled assets
  bundled = Path(assets_dir) / DEFAULT_STYLES_FILENAME if assets_dir else resource_path(DEFAULT_STYLES_FILENAME)
  try:
    shutil.copyfile(bundled, user_stylesheet)
    print(f"Copied default stylesheet to {user_stylesheet}")
    return str(user_stylesheet)
  except Exception as e:
    print(f"Failed to copy bundled stylesheet to user config: {e}")
  
  # Create fallback stylesheet if copy fails
  try:
    with open(user_stylesheet, "w", encoding="utf-8") as f:
      f.write(FALLBACK_CSS)
    print(f"Created fallback stylesheet at {user_stylesheet}")
  except Exception as e2:
    print(f"Failed to create fallback stylesheet: {e2}")
  return str(user_stylesheet)
