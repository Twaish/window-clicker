FALLBACK_CSS = """
* {
  font-size: 14px;
  font-weight: 600;
  font-family: "Consolas", "JetBrainsMono NFP";
  margin: 0;
  padding: 0;
  color: #f0f0f0;
}

QWidget {
  background-color: #222;
  padding: 6px;
}

QPushButton {
  border: 1px solid #555;
  border-radius: 4px;
}
QPushButton:hover {
  background: #343434;
}

QComboBox {
  border: 1px solid #555;
  border-radius: 4px;
}

QLineEdit {
  background: #202020;
  border: 1px solid #555;
  border-radius: 4px;
}

QTextEdit {
  background: #202020;
  border: 1px solid #555;
  border-radius: 4px;
}

.press_button {
  background-color: #16a34a;
}
.press_button:hover {
  background-color: #1ac057;
}
.press_button[active="true"] {
  background-color: #ef4444;
}
.press_button[active="true"]:hover {
  background-color: #f15757;
}

QScrollBar:vertical, QScrollBar:horizontal {
  background: transparent;
  padding: 0;
  width: 5px;
  height: 5px;
}

QScrollBar::handle {
  background: #404040;
}
QScrollBar::handle:hover {
  background-color: #909090;
}
"""