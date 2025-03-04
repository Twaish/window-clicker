import time
import win32process
import win32api
import win32gui
import threading
import tkinter as tk
from tkinter import ttk
from utils.window_utils import *

def on_window_select(event):
  selected_index = window_selector.current()
  selected_window = windows[selected_index]
  hwnd, title = selected_window
  _, pid = win32process.GetWindowThreadProcessId(hwnd)
  window_details.set(f"Selected Window: \"{title}\"\nHandle: {hwnd}\nProcess ID: {pid}")

def on_combo_select(event):
  selected_index = combo_selector.current()
  selected_combo = combos[selected_index]
  title, sequence = selected_combo
  print(f"SELECTED: {title}")
  press_manager.set_buttons(sequence)

def get_selected_window_handle():
  selected_index = window_selector.current()
  return windows[selected_index][0] if selected_index >= 0 else None

def focus_selected_window():
  hwnd = get_selected_window_handle()
  if hwnd:
    focus_window(hwnd)

class PressManager:
  def __init__(self):
    self.pressing = False
    self.thread = None
    self.interval = 1

  def set_interval(self, interval):
    self.interval = interval

  def toggle_pressing(self):
    if self.pressing:
      self.stop_pressing()
    else:
      self.start_pressing()

  def start_pressing(self):
    hwnd = get_selected_window_handle()
    if hwnd:
      self.pressing = True
      self.thread = threading.Thread(target=self.press_daemon, args=(hwnd,), daemon=True)
      self.thread.start()
      press_button.config(text="Stop Pressing")

  def stop_pressing(self):
    self.pressing = False
    if self.thread:
      self.thread.join(timeout=1.0)
    press_button.config(text="Start Pressing")

  def is_cursor_in_window(self, hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    x_left, y_top, x_right, y_bottom = rect
    cursor_x, cursor_y = win32api.GetCursorPos()
    return x_left <= cursor_x <= x_right and y_top <= cursor_y <= y_bottom

  def is_window_focused(self, hwnd):
    self.window_focused = hwnd == win32gui.GetForegroundWindow()
    return self.window_focused

  def is_mouse_button_pressed(self):
    return win32api.GetAsyncKeyState(0x01)

  def press_daemon(self, hwnd):
    while self.pressing:
      if self.is_window_focused(hwnd) and self.is_cursor_in_window(hwnd) and self.is_mouse_button_pressed():
        time.sleep(0.01)
        continue

      click_position(hwnd, 0, 0)
      time.sleep(self.interval)
    print("ENDED THREAD")


if __name__ == "__main__":
  root = tk.Tk()
  root.title("Window Selector")
  root.geometry("450x400")

  windows = get_all_window_titles_and_handles()
  window_titles = [title for _, title in windows]

  tk.Label(root, text="Select a Window:").pack(pady=10)
  window_selector = ttk.Combobox(root, values=window_titles, state='readonly')
  window_selector.pack(pady=10)
  window_selector.bind("<<ComboboxSelected>>", on_window_select)

  tk.Label(root, text="Set Interval (seconds):").pack(pady=10)
  interval_entry = tk.Entry(root)
  interval_entry.pack(pady=10)
  interval_entry.insert(0, "1")

  window_details = tk.StringVar()
  tk.Label(root, textvariable=window_details, justify=tk.LEFT).pack(pady=10)

  focus_button = tk.Button(root, text="Focus Selected Window", command=focus_selected_window)
  focus_button.pack(pady=10)

  press_manager = PressManager()
  def start_pressing_with_interval():
    try:
      interval = float(interval_entry.get())
      press_manager.set_interval(interval)
      press_manager.toggle_pressing()
    except ValueError:
      print("Invalid interval value")
  press_button = tk.Button(root, text="Start Pressing", command=start_pressing_with_interval)
  press_button.pack(pady=10)

  try:
    root.mainloop()
  except KeyboardInterrupt:
    exit()