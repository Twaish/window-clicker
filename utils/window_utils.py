import win32api
import win32con
import win32gui

def enum_windows_callback(hwnd, windows):
  if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
    window_title = win32gui.GetWindowText(hwnd)
    windows.append((hwnd, window_title))

def get_all_window_titles_and_handles():
  windows = []
  win32gui.EnumWindows(enum_windows_callback, windows)
  return [win for win in windows if win32gui.IsWindowVisible(win[0])]

def click_position(hwnd, x, y):
  lParam = (y << 16) | x
  win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, lParam)
  win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
  win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)

def send_string(hwnd, key):
  if key:
    def send(handle, param):
      for char in key:
        win32gui.SendMessage(handle, win32con.WM_CHAR, ord(char), 0)
    win32gui.EnumChildWindows(hwnd, send, 0)

def focus_window(hwnd):
  if win32gui.IsIconic(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
  
  win32gui.SetForegroundWindow(hwnd)