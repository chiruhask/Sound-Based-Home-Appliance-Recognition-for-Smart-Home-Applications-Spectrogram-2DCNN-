# Some are Collected From Github Gist and PyQt5 Community
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtGui import QPixmap, QPainter, QBitmap
from PyQt5.QtCore import Qt, pyqtSignal, QSize

class ClickableFrame(QFrame):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)


class RoundImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def setPixmap(self, pixmap):
        if not pixmap.isNull():
            mask = QBitmap(pixmap.size())
            mask.fill(Qt.white)
            painter = QPainter(mask)
            painter.setBrush(Qt.black)
            painter.drawRoundedRect(pixmap.rect(), 10, 10)
            painter.end()
            pixmap.setMask(mask)
        super().setPixmap(pixmap)


class ExpandableImage(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)

        self.title = title
        self.previous_size = None

        self.initUI()

    def set_image(self, image_path):
        self.image_path = image_path
        pixmap = QPixmap(self.image_path)
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setAlignment(Qt.AlignCenter)

    def initUI(self):
        layout = QVBoxLayout()

        self.frame = ClickableFrame(self)
        self.frame.setObjectName("cardFrame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.clicked.connect(self.toggleContent)

        self.label = QLabel(text=self.title)
        self.label.setAlignment(Qt.AlignCenter)

        self.imageLabel = RoundImageLabel(self)
        self.imageLabel.setVisible(False)

        layout.addWidget(self.label)
        layout.addWidget(self.imageLabel)

        self.frame.setLayout(layout)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.frame)
        mainLayout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(mainLayout)

    def toggleContent(self):
        if self.imageLabel.isVisible():
            self.imageLabel.setVisible(False)
            self.label.setVisible(True)
        else:
            self.imageLabel.setVisible(True)
            self.label.setVisible(False)

class ExpandableLabel(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)

        self.title = title

        self.initUI()

    def set_label(self, result):
        self.result.setText(result)

    def initUI(self):
        layout = QVBoxLayout()

        self.frame = ClickableFrame(self)
        self.frame.setObjectName("cardFrame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.label = QLabel(text=self.title)
        self.label.setAlignment(Qt.AlignCenter)

        self.result = QLabel(text='')
        self.result.setAlignment(Qt.AlignCenter)
        self.result.setVisible(False)

        layout.addWidget(self.label)
        layout.addWidget(self.result)

        self.frame.setLayout(layout)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.frame)
        mainLayout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(mainLayout)

    def toggleContent(self):
        if self.result.isVisible():
            self.result.setVisible(False)
            self.label.setVisible(True) 
            return False
        else:
            self.result.setVisible(True)
            self.label.setVisible(False)
            return True

