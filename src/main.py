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

    # Navbar
    navbar = QHBoxLayout()
    pages = QStackedWidget()

    macro_page = QPushButton("Macro")
    macro_page.clicked.connect(lambda: pages.setCurrentIndex(0))
    navbar.addWidget(macro_page)
    pages.addWidget(MacroPage())

    window_clicker_page = QPushButton("Window Clicker")
    window_clicker_page.clicked.connect(lambda: pages.setCurrentIndex(1))
    navbar.addWidget(window_clicker_page)
    pages.addWidget(WindowClickerPage())
    
    main_layout = QVBoxLayout()
    main_layout.addLayout(navbar)
    main_layout.addWidget(pages)
    container = QWidget()
    container.setLayout(main_layout)
    self.setCentralWidget(container)

    # Setup
    self.apply_stylesheet()

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