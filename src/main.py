import sys
from PyQt6.QtWidgets import (
  QApplication, QWidget, QLabel, QComboBox, QLineEdit,
  QPushButton, QVBoxLayout, QMessageBox, QTextEdit,
  QHBoxLayout, QMainWindow, QListWidget, QStackedWidget
)
from PyQt6.QtCore import QFileSystemWatcher
from PyQt6.QtGui import QIcon
from utils.config_utils import ensure_user_stylesheet
from utils.FALLBACK_CSS import FALLBACK_CSS
from settings import APP_BAR_TITLE
from pages.macro_page import MacroPage
from pages.window_clicker_page import WindowClickerPage

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle(APP_BAR_TITLE)
    self.setFixedSize(700, 400)
    
    self.stylesheet_path = ensure_user_stylesheet()
    self.watcher = QFileSystemWatcher([self.stylesheet_path])
    self.watcher.fileChanged.connect(self.apply_stylesheet)

    container = QWidget()
    layout = QVBoxLayout()
    self.setCentralWidget(container)

    self.navbar = QHBoxLayout()
    self.pages = QStackedWidget()

    self.add_page("Macro", MacroPage())
    self.add_page("Window Clicker", WindowClickerPage())
    
    layout.addLayout(self.navbar)
    layout.addWidget(self.pages)
    container.setLayout(layout)

    # Setup
    self.apply_stylesheet()
  
  def add_page(self, name, page):
    if not isinstance(page, QWidget):
      raise TypeError("Page must be a QWidget instance")
    
    next_index = self.pages.count()
    nav_button = QPushButton(name)
    nav_button.clicked.connect(lambda: self.pages.setCurrentIndex(next_index))
    self.navbar.addWidget(nav_button)
    self.pages.addWidget(page)

  def apply_stylesheet(self):
    try:
      css_text = None
      with open(self.stylesheet_path, "r", encoding="utf-8") as f:
        css_text = f.read()

      if not css_text.strip():
        raise ValueError("Stylesheet is empty")
      self.setStyleSheet(css_text)
      print("Stylesheet reloaded.")
    except Exception as e:
      print(f"Failed to load stylesheet: {e}; falling back to emergency css")
      self.setStyleSheet(FALLBACK_CSS)

if __name__ == "__main__":
  app = QApplication(sys.argv)
  app.setWindowIcon(QIcon("assets/logo.png"))
  window = MainWindow()
  window.show()
  try:
    sys.exit(app.exec())
  except KeyboardInterrupt:
    pass