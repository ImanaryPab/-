import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QSlider, QHBoxLayout, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QUrl, Qt

class MediaPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TPlayer")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: lightblue;")
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        title_label = QLabel("TPlayer", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-family: Impact; font-size: 50px; color: black;") 

        self.video_widget = QVideoWidget(self)
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.seek_slider = QSlider(Qt.Horizontal, self)
        self.seek_slider.sliderMoved.connect(self.set_position)
        self.seek_slider.hide()

        button_style = """
            QPushButton {
                background-color: white;
                border: 2px solid black;
                border-radius: 5px;
                padding: 5px;
                color: black;
                font-family: Impact;
                font-size: 30px;
            }
            QPushButton#pauseButton {
                background-color: black;
                border: 2px solid black;
                border-radius: 5px;
                padding: 5px;
                min-width: 80px;
                color: white;
                font-family: Arial;
                font-size: 18px;
            }
            QPushButton#speedButton {
                background-color: white;
                border: 2px solid black;
                border-radius: 5px;
                padding: 5px;
                min-width: 80px;
                color: black;
                font-family: Arial;
                font-size: 18px;
            }
        """

        hbox = QHBoxLayout()

        self.play_audio_button = QPushButton("Аудио", self)
        self.play_audio_button.clicked.connect(self.play_audio)
        self.play_audio_button.setStyleSheet(button_style)
        hbox.addWidget(self.play_audio_button)

        self.play_video_button = QPushButton("Видео", self)
        self.play_video_button.clicked.connect(self.play_video)
        self.play_video_button.setStyleSheet(button_style)
        hbox.addWidget(self.play_video_button)

        self.play_image_button = QPushButton("Изображение", self)
        self.play_image_button.clicked.connect(self.show_image)
        self.play_image_button.setStyleSheet(button_style)
        hbox.addWidget(self.play_image_button)

        hbox_pause = QHBoxLayout()
        self.pause_button = QPushButton("Пауза", self)
        self.pause_button.setObjectName("pauseButton")
        self.pause_button.clicked.connect(self.pause)
        self.pause_button.setStyleSheet(button_style)
        hbox_pause.addWidget(self.pause_button)
        self.pause_button.hide()

        hbox_speed = QHBoxLayout()
        self.speed_button = QPushButton("1x", self)
        self.speed_button.setObjectName("speedButton")
        self.speed_button.clicked.connect(self.toggle_speed)
        self.speed_button.setStyleSheet(button_style)
        hbox_speed.addWidget(self.speed_button)
        self.speed_button.hide()

        vbox = QVBoxLayout()
        vbox.addWidget(title_label)
        vbox.addLayout(hbox)
        vbox.addWidget(self.seek_slider)
        vbox.addWidget(self.video_widget)
        vbox.addWidget(self.image_label)
        vbox.addLayout(hbox_pause)
        vbox.addLayout(hbox_speed)

        main_widget.setLayout(vbox)

        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.video_widget)
        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)
        self.player.stateChanged.connect(self.update_pause_button_text)
        self.player.error.connect(self.handle_error)  # Add error handling

    def play_audio(self):
        self.hide_controls()
        audio_file, _ = QFileDialog.getOpenFileName(self, "Выберите аудиофайл", "", "Audio Files (*.mp3 *.wav *.ogg)")
        if audio_file:
            self.image_label.clear()
            self.video_widget.hide()
            self.image_label.hide()
            self.pause_button.setText("Пауза")
            self.pause_button.show()
            self.speed_button.setText("1x")
            self.speed_button.show()
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(audio_file)))
            self.player.play()
            self.seek_slider.setMaximum(self.player.duration())
            self.seek_slider.show()

    def play_video(self):
        self.hide_controls()
        video_file, _ = QFileDialog.getOpenFileName(self, "Выберите видеофайл", "", "Video Files (*.mp4 *.avi *.mov)")
        if video_file:
            self.image_label.clear()
            self.image_label.hide()
            self.video_widget.show()
            self.pause_button.setText("Пауза")
            self.pause_button.show()
            self.speed_button.setText("1x")
            self.speed_button.show()
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(video_file)))
            self.player.play()
            self.seek_slider.setMaximum(self.player.duration())
            self.seek_slider.show()

    def show_image(self):
        self.hide_controls()
        image_file, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Image Files (*.jpg *.png *.jpeg *.bmp)")
        if image_file:
            self.player.stop()
            self.video_widget.hide()
            pixmap = QPixmap(image_file)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))
            self.image_label.show()
            self.seek_slider.hide()

    def hide_controls(self):
        self.pause_button.hide()
        self.speed_button.hide()

    def pause(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def set_position(self, position):
        self.player.setPosition(position)

    def update_position(self, position):
        self.seek_slider.setValue(position)

    def update_duration(self, duration):
        self.seek_slider.setMaximum(duration)

    def update_pause_button_text(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.pause_button.setText("Пауза")
        else:
            self.pause_button.setText("Продолжить")

    def toggle_speed(self):
        current_speed = self.speed_button.text()
        if current_speed == "1x":
            self.speed_button.setText("1.5x")
            self.player.setPlaybackRate(1.5)
        elif current_speed == "1.5x":
            self.speed_button.setText("2x")
            self.player.setPlaybackRate(2)
        else:
            self.speed_button.setText("1x")
            self.player.setPlaybackRate(1)

    def handle_error(self):
        error_message = self.player.errorString()
        QMessageBox.critical(self, "Ошибка", f"Произошла ошибка при воспроизведении: {error_message}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MediaPlayer()
    player.show()
    sys.exit(app.exec_())
