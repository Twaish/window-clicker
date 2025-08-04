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

def focus_window(hwnd):
  if not hwnd:
    return

  if win32gui.IsIconic(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
  
  win32gui.SetForegroundWindow(hwnd)

def is_window_focused(hwnd):
  return hwnd == win32gui.GetForegroundWindow()

def is_mouse_button_pressed():
  return win32api.GetAsyncKeyState(0x01)

def is_cursor_in_window(hwnd):
  rect = win32gui.GetWindowRect(hwnd)
  x_left, y_top, x_right, y_bottom = rect
  cursor_x, cursor_y = win32api.GetCursorPos()
  return x_left <= cursor_x <= x_right and y_top <= cursor_y <= y_bottom
