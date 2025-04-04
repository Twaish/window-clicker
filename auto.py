import time
import win32process
import win32api
import win32gui
import threading
import tkinter as tk
from tkinter import ttk
from utils.window_utils import *

DEFAULT_INTERVAL = 1.0
SLEEP_DURATION = 0.01

class WindowClicker:
  def __init__(self, root):
    self.root = root
    root.title("Window Clicker")
    root.geometry("450x400")
    
    self.windows = []
    self.window_titles = []
    self.hwnd = None
    self.selected_window = None

    self.press_manager = PressManager()
    self.create_widgets()
    self.refresh_window_list()


  def refresh_window_list(self):
    self.windows = get_all_window_titles_and_handles()
    self.window_titles = [title for _, title in self.windows]
    self.window_selector['values'] = self.window_titles
    self.window_selector.set('')
  
  def create_widgets(self):
    tk.Label(self.root, text="Select a Window:").pack(pady=10)
    self.window_selector = ttk.Combobox(self.root, values=self.window_titles, state='readonly')
    self.window_selector.pack(pady=10)
    self.window_selector.bind("<<ComboboxSelected>>", self.on_window_select)

    tk.Label(self.root, text="Set Interval (seconds):").pack(pady=10)
    self.interval_entry = tk.Entry(self.root)
    self.interval_entry.pack(pady=10)
    self.interval_entry.insert(0, str(DEFAULT_INTERVAL))
    
    self.refresh_button = tk.Button(self.root, text="Refresh Windows", command=self.refresh_window_list)
    self.refresh_button.pack(pady=10)

    self.window_details = tk.StringVar()
    tk.Label(self.root, textvariable=self.window_details, justify=tk.LEFT).pack(pady=10)

    self.focus_button = tk.Button(
      self.root, 
      text="Focus Selected Window", 
      command=lambda: focus_window(self.get_selected_window()[0])
    )
    self.focus_button.pack(pady=10)

    self.press_button = tk.Button(self.root, text="Start Pressing", command=self.start_pressing_with_interval)
    self.press_button.pack(pady=10)

  def on_window_select(self, _):
    hwnd, title = self.get_selected_window()
    if hwnd is None:
      self.window_details.set("No window selected.")
      return
    
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    self.window_details.set(f"Selected Window: \"{title}\"\nHandle: {hwnd}\nProcess ID: {pid}")
    self.hwnd = hwnd

  def start_pressing_with_interval(self):
    if self.press_manager.is_pressing:
      self.press_manager.stop_pressing()
      self.press_button.config(text="Start Pressing")
      return
    
    if not self.hwnd:
      print("No window selected")
      return
    
    interval = float(self.interval_entry.get())
    if interval <= 0:
      print("Interval must be positive.")
      return

    self.press_button.config(text="Stop Pressing")
    self.root.after(100, lambda: self.press_manager.start_pressing(self.hwnd, interval))

  def get_selected_window(self):
    selected_index = self.window_selector.current()
    return self.windows[selected_index] if selected_index >= 0 else (None, None)

class PressManager:
  def __init__(self):
    self.is_pressing = False
    self.stop_event = threading.Event()
    self.thread = None

  def start_pressing(self, hwnd, interval):
    if hwnd:
      self.is_pressing = True
      self.stop_event.clear()
      self.thread = threading.Thread(target=self.press_daemon, args=(hwnd, interval), daemon=True)
      self.thread.start()

  def stop_pressing(self):
    self.is_pressing = False
    self.stop_event.set()
    if self.thread:
      self.thread.join(timeout=1.0)

  def press_daemon(self, hwnd, interval = DEFAULT_INTERVAL, position = (0, 0)):
    while self.is_pressing:
      if is_window_focused(hwnd) and is_cursor_in_window(hwnd) and is_mouse_button_pressed():
        time.sleep(SLEEP_DURATION)
        continue
      
      position = (318, 492)
      click_position(hwnd, position[0], position[1])
      if self.stop_event.wait(interval):
        break
    print("ENDED THREAD")

if __name__ == "__main__":
  try:
    root = tk.Tk()
    app = WindowClicker(root)
    root.mainloop()
  except KeyboardInterrupt:
    exit()