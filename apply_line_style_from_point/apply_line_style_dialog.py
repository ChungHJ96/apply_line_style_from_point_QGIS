from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton

class ApplyLineStyleDialog(QDialog):
    def __init__(self, point_layer_names):
        super().__init__()
        self.setWindowTitle("포인트 레이어 선택")
        self.layout = QVBoxLayout()

        self.label = QLabel("포인트 레이어를 선택하세요:")
        self.layout.addWidget(self.label)

        self.combo = QComboBox()
        self.combo.addItems(point_layer_names)
        self.layout.addWidget(self.combo)

        self.ok_button = QPushButton("적용")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)

        self.setLayout(self.layout)

    def selected_layer_name(self):
        return self.combo.currentText()
