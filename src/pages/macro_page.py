from PyQt6.QtWidgets import (
  QWidget, QLabel, QVBoxLayout, QListWidget, QHBoxLayout
)

class MacroPage(QWidget):
  macro_list = []
  def __init__(self):
    super().__init__()

    self.macro_list_widget = QListWidget()
    self.macro_list_widget.setFixedWidth(200)
    macro_actions = QVBoxLayout()
    macro_actions.addWidget(QLabel("Macro Actions"))
    macro_actions.addWidget(self.macro_list_widget)

    content = QVBoxLayout()
    content.addWidget(QLabel("Add your macro actions here..."))

    layout = QHBoxLayout()
    layout.addLayout(macro_actions)
    layout.addLayout(content)
    self.setLayout(layout)