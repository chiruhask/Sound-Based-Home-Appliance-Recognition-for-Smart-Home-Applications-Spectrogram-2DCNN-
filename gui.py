import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QSlider, QGridLayout, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QTimer
from widgets import *
from model import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Home Appliances Sound Analyzer")

        self.setStyleSheet("""
            #cardFrame {
                background-color: #FFFFFF;
                border-radius: 10px;
                margin-bottom: 10px;
            }
        """)

        self.toog = False
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        open_audio_button = QPushButton('Open Audio')
        open_audio_button.clicked.connect(self.open_audio)
        self.grid.addWidget(open_audio_button, 0, 0, 1, 2)

        self.music_slider = QSlider()
        self.music_slider.setOrientation(1)
        self.grid.addWidget(self.music_slider, 1, 0, 1, 2)

        self.play_button = QPushButton('Play')
        self.play_button.clicked.connect(self.play_audio)
        self.pause_button = QPushButton('Pause')
        self.pause_button.clicked.connect(self.pause_audio)
        self.grid.addWidget(self.play_button, 2, 0)
        self.grid.addWidget(self.pause_button, 2, 1)

        self.show_spec = ExpandableImage("Show Spectogram", parent=self)
        self.grid.addWidget(self.show_spec, 3, 0, 1, 2)

        self.predicted_label = ExpandableLabel("Predict Sound")
        self.predicted_label.set_label('Hello World')
        self.grid.addWidget(self.predicted_label, 4, 0, 1, 2)

        self.media_player = QMediaPlayer()
        self.media_player.setVolume(50)
        self.media_player.positionChanged.connect(self.update_slider)
        self.media_player.durationChanged.connect(self.update_duration)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_slider)

        self.setWindowTitle('Audio Player')
        self.setGeometry(100, 100, 750, 300)
        self.show()

    def open_audio(self):
        file_dialog = QFileDialog()
        audio_file, _ = file_dialog.getOpenFileName(self, "Open Audio File", "", "Audio Files (*.wav)")
        if audio_file:
            self.audio_file = audio_file
            create_spectrogram(audio_file, 'ui/data/result.png')
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(audio_file)))
            self.play_button.setEnabled(True)
            self.pause_button.setEnabled(True)
            self.show_spec.set_image('ui/data/result.png')
            self.show_spec.frame.clicked.connect(self.show_specto)
            self.predicted_label.frame.clicked.connect(self.show_result)

    def play_audio(self):
        self.media_player.play()
        self.timer.start(100)

    def pause_audio(self):
        self.media_player.pause()
        self.timer.stop()

    def update_slider(self):
        position = self.media_player.position()
        self.music_slider.setValue(position)

    def update_duration(self, duration):
        self.music_slider.setRange(0, duration)

    def show_specto(self):
        if self.toog:
            self.toog = False
            self.resize(750, 300)
        else:
            self.toog = True

    def show_result(self):
        val = self.predicted_label.toggleContent()
        if val:
            label, value = get_sound_class('ui/data/result.png')
            self.predicted_label.set_label(f'{label}: {value}')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())