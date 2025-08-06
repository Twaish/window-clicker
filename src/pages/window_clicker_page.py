from PyQt6.QtWidgets import (
  QWidget, QLabel, QComboBox, QLineEdit,
  QPushButton, QVBoxLayout, QMessageBox, QTextEdit,
  QHBoxLayout
)
from core.click_worker import ClickWorker
from utils.window_utils import window_exists, focus_window, get_all_window_titles_and_handles
from utils.FALLBACK_CSS import FALLBACK_CSS
from settings import DEFAULT_CLICK_INTERVAL

class WindowClickerPage(QWidget):
  def __init__(self):
    super().__init__()
    
    self.windows = []
    self.selected_hwnd = None
    self.is_pressing = False
    
    # Window Selector
    self.window_selector = QComboBox()
    self.window_selector.currentIndexChanged.connect(self.on_window_select)

    self.focus_button = QPushButton("Focus")
    self.focus_button.clicked.connect(lambda: focus_window(self.selected_hwnd))

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
    self.interval_entry = QLineEdit(str(DEFAULT_CLICK_INTERVAL))

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

    # Main Layout
    layout = QVBoxLayout()
    layout.addLayout(sel_row)
    layout.addLayout(int_row)
    layout.addWidget(self.details_box)
    main_layout = QHBoxLayout()
    main_layout.addLayout(layout)
    main_layout.setContentsMargins(0, 0, 0, 0)
    self.setLayout(main_layout)

    # Worker
    self.worker = ClickWorker()
    self.worker.pressing_update.connect(self.on_pressing_update)
    self.worker.status_update.connect(self.on_status_update)
    
    self.refresh_window_list()

  def refresh_window_list(self):
    self.windows = get_all_window_titles_and_handles()
    self.window_selector.clear()
    titles = [title if title else "<No Title>" for _, title, _ in self.windows]
    self.window_selector.addItems(titles)
    self.selected_hwnd = None
    self.details_box.setPlainText("No window selected.")
    self.on_window_select(0)

  def on_window_select(self, index):
    if index < 0 or index >= len(self.windows):
      self.details_box.setPlainText("No window selected.")
      self.selected_hwnd = None
      return
    hwnd, title, pid = self.windows[index]
    self.selected_hwnd = hwnd
    self.details_box.setPlainText(f'title: "{title}"\nhwnd: {hwnd}\npid: {pid}')

  def toggle_pressing(self):
    if self.is_pressing:
      self.worker.stop_pressing()
      return
    
    if not window_exists(self.selected_hwnd):
      QMessageBox.warning(self, "Warning", "Selected window is not valid or no longer exists.")
      return
    
    interval = self.interval_entry.text()
    self.worker.start_pressing(self.selected_hwnd, interval)

  def on_pressing_update(self, is_pressing):
    self.press_button.setText("Stop" if is_pressing else "Start")
    self.press_button.setProperty("active", is_pressing)
    self.is_pressing = is_pressing
    self.refresh_style(self.press_button)
  
  def on_status_update(self, msg):
    self.details_box.append(f"[Status] {msg}")

  def refresh_style(self, widget):
    widget.style().unpolish(widget)
    widget.style().polish(widget)
    widget.update()