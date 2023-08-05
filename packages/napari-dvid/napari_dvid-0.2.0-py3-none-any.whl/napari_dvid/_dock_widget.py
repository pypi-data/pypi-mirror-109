from napari_plugin_engine import napari_hook_implementation
from qtpy.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton


class UrlWidget(QWidget):
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer
        self.url = ""

        label = QLabel()
        label.setText("DVID volume url")
        label.adjustSize()

        textbox = QLineEdit()
        textbox.textChanged.connect(self._on_text_changed)

        btn = QPushButton("Load")
        btn.clicked.connect(self._on_click)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(label)
        self.layout().addWidget(textbox)
        self.layout().addWidget(btn)

    def _on_text_changed(self, text):
        self.url = text

    def _on_click(self):
        self.viewer.open(self.url, plugin="napari-dvid")


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return UrlWidget
