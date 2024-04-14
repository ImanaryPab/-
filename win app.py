import sys
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import QUrl, Qt

class MediaPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Медиа Плеер")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: black;")

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        hbox = QHBoxLayout(main_widget)

        self.play_audio_button = QPushButton("Аудио", self)
        self.play_audio_button.clicked.connect(self.play_audio)
        self.play_audio_button.setStyleSheet("background-color: white; border-radius: 25px;")
        self.play_audio_button.setFont(QFont("Arial", 12))
        hbox.addWidget(self.play_audio_button)

        self.play_video_button = QPushButton("Видео", self)
        self.play_video_button.clicked.connect(self.play_video)
        self.play_video_button.setStyleSheet("background-color: white; border-radius: 25px;")
        self.play_video_button.setFont(QFont("Arial", 12))
        hbox.addWidget(self.play_video_button)

        self.play_image_button = QPushButton("Изображение", self)
        self.play_image_button.clicked.connect(self.show_image)
        self.play_image_button.setStyleSheet("background-color: white; border-radius: 25px;")
        self.play_image_button.setFont(QFont("Arial", 12))
        hbox.addWidget(self.play_image_button)

        self.seek_slider = QSlider(Qt.Horizontal, self)
        self.seek_slider.sliderMoved.connect(self.set_position)
        self.seek_slider.hide()
        hbox.addWidget(self.seek_slider)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        hbox.addWidget(self.image_label)

        self.player = QMediaPlayer()
        self.player.positionChanged.connect(self.update_position)

    def play_audio(self):
        audio_file, _ = QFileDialog.getOpenFileName(self, "Выберите аудиофайл", "", "Audio Files (*.mp3)")
        if audio_file:
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(audio_file)))
            self.player.play()
            self.seek_slider.setMaximum(self.player.duration())
            self.seek_slider.show()

    def play_video(self):
        video_file, _ = QFileDialog.getOpenFileName(self, "Выберите видеофайл", "", "Video Files (*.mp4 *.avi *.mov)")
        if video_file:
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(video_file)))
            self.player.play()
            self.seek_slider.setMaximum(self.player.duration())
            self.seek_slider.show()

    def set_position(self, position):
        self.player.setPosition(position)
        
    def update_position(self, position):
        self.seek_slider.setValue(position)

    def show_image(self):
        image_file, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Image Files (*.jpg *.png)")
        if image_file:
            pixmap = QPixmap(image_file)
            self.image_label.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MediaPlayer()
    player.show()
    sys.exit(app.exec_())
