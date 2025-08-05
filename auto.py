import sys
import win32process
from PyQt6.QtWidgets import (
  QApplication, QWidget, QLabel, QComboBox, QLineEdit,
  QPushButton, QVBoxLayout, QMessageBox, QTextEdit,
  QHBoxLayout, QMainWindow
)
from utils.window_utils import *
from utils.click_worker import ClickWorker, DEFAULT_INTERVAL
from PyQt6.QtCore import QFileSystemWatcher
from PyQt6.QtGui import QIcon
from utils.config_utils import ensure_user_stylesheet
from utils.FALLBACK_CSS import FALLBACK_CSS

class WindowClicker(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Draco - Macro Application")
    self.setFixedSize(500, 250)
    
    self.stylesheet_path = ensure_user_stylesheet(app_name="draco", filename="style.css")
    self.watcher = QFileSystemWatcher([self.stylesheet_path])
    self.watcher.fileChanged.connect(self.apply_stylesheet)

    self.windows = []
    self.selected_hwnd = None
    self.is_pressing = False
    
    container = QWidget()
    self.setCentralWidget(container)
    
    # Window Selector
    self.window_selector = QComboBox()
    self.window_selector.currentIndexChanged.connect(self.on_window_select)

    self.focus_button = QPushButton("Focus")
    self.focus_button.clicked.connect(self.do_focus)

    self.refresh_button = QPushButton()
    self.refresh_button.setText("Refresh")
    self.refresh_button.setToolTip("Refresh Window List")
    self.refresh_button.clicked.connect(self.refresh_window_list)

    sel_row = QHBoxLayout()
    sel_row.addWidget(QLabel("Window"))
    sel_row.addWidget(self.window_selector)
    sel_row.addWidget(self.focus_button)
    sel_row.addWidget(self.refresh_button)

    # Interval
    self.interval_entry = QLineEdit(str(DEFAULT_INTERVAL))

    self.press_button = QPushButton("Start")
    self.press_button.setProperty("class", "press_button")
    self.press_button.clicked.connect(self.toggle_pressing)
    
    int_row = QHBoxLayout()
    int_row.addWidget(QLabel("Interval (seconds)"))
    int_row.addWidget(self.interval_entry)
    int_row.addWidget(self.press_button)
    
    # Logs
    self.details_box = QTextEdit()
    self.details_box.setReadOnly(True)

    log_col = QVBoxLayout()
    log_col.addWidget(self.details_box)

    # Main Layout
    layout = QVBoxLayout()
    layout.addLayout(sel_row)
    layout.addLayout(int_row)
    layout.addLayout(log_col)
    container.setLayout(layout)

    # Worker
    self.worker = ClickWorker()
    self.worker.status_update.connect(self.on_status_update)
    self.worker.finished.connect(self.on_worker_finished)

    # Setup
    self.apply_stylesheet()
    self.refresh_window_list()


  def apply_stylesheet(self):
    css_text = None
    try:
      with open(self.stylesheet_path, "r", encoding="utf-8") as f:
        css_text = f.read()

      if not css_text.strip():
        raise ValueError("Stylesheet is empty")
      self.setStyleSheet(css_text)
      print("Stylesheet reloaded.")
    except Exception as e:
      print(f"Failed to load stylesheet: {e}; falling back to emergency css")
      self.setStyleSheet(FALLBACK_CSS)

  def refresh_window_list(self):
    self.windows = get_all_window_titles_and_handles()
    self.window_selector.clear()
    titles = [title if title else "<No Title>" for _, title in self.windows]
    self.window_selector.addItems(titles)
    self.selected_hwnd = None
    self.details_box.setPlainText("No window selected.")

  def on_window_select(self, index):
    if index < 0 or index >= len(self.windows):
      self.details_box.setPlainText("No window selected.")
      self.selected_hwnd = None
      return
    hwnd, title = self.windows[index]
    self.selected_hwnd = hwnd
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    self.details_box.setPlainText(
      f'Selected Window: "{title}"\nHandle: {hwnd}\nProcess ID: {pid}'
    )

  def do_focus(self):
    if self.selected_hwnd:
      focus_window(self.selected_hwnd)
    else:
      QMessageBox.warning(self, "Warning", "No window selected to focus.")

  def refresh_style(self, widget):
    widget.style().unpolish(widget)
    widget.style().polish(widget)
    widget.update()

  def toggle_pressing(self):
    if self.is_pressing:
      self.worker.stop_pressing()
      self.press_button.setText("Start")
      self.press_button.setProperty("active", False)
      self.is_pressing = False
    else:
      if not self.selected_hwnd:
        QMessageBox.warning(self, "Warning", "No window selected.")
        return
      interval = self.interval_entry.text()
      started_pressing = self.worker.start_pressing(self.selected_hwnd, interval)
      if started_pressing:
        self.press_button.setText("Stop")
        self.press_button.setProperty("active", True)
        self.is_pressing = True

    self.refresh_style(self.press_button)

  def on_status_update(self, msg):
    self.details_box.append(f"[Status] {msg}")
    if "Ended pressing thread." in msg or "Stopping" in msg:
      self.press_button.setText("Start")
      self.is_pressing = False

  def on_worker_finished(self):
    self.press_button.setText("Start")
    self.is_pressing = False

if __name__ == "__main__":
  app = QApplication(sys.argv)
  app.setWindowIcon(QIcon("logo.png"))
  window = WindowClicker()
  window.show()
  try:
    sys.exit(app.exec())
  except KeyboardInterrupt:
    pass