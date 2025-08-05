import time
import threading
from utils.window_utils import *
from PyQt6.QtCore import pyqtSignal, QObject
from settings import DEFAULT_CLICK_INTERVAL

class ClickWorker(QObject):
  status_update = pyqtSignal(str)
  pressing_update = pyqtSignal(bool)

  def __init__(self):
    super().__init__()
    self._is_pressing = False
    self._hwnd = None
    self._interval = DEFAULT_CLICK_INTERVAL
    self._stop_event = threading.Event()

  def start_pressing(self, hwnd, interval):
    if not hwnd:
      return
    
    self._hwnd = hwnd
    try:
      self._interval = float(interval)
      if self._interval <= 0:
        raise ValueError("Interval must be positive")
    except Exception as e:
      self.status_update.emit(f"Invalid interval: {e}")
      return
    
    self._stop_event.clear()
    self._is_pressing = True
    threading.Thread(target=self._press_loop, daemon=True).start()
    self.status_update.emit("Started presssing.")
    self.pressing_update.emit(True)

  def stop_pressing(self):
    self._is_pressing = False
    self._stop_event.set()
    self.status_update.emit("Stopping...")
  
  def _press_loop(self):
    while self._is_pressing and not self._stop_event.is_set():
      hwnd = self._hwnd
      if is_window_focused(hwnd) and is_cursor_in_window(hwnd) and is_mouse_button_pressed():
        time.sleep(0.01)
        continue
      position = (318, 492)
      click_position(hwnd, position[0], position[1])
      if self._stop_event.wait(self._interval):
        break
    self._is_pressing = False
    self.status_update.emit("Ended pressing thread.")
    self.pressing_update.emit(False)