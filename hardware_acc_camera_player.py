# hardware_acc_camera_player_fixed.py

import sys
from PyQt5.QtCore              import Qt
from PyQt5.QtGui               import QSurfaceFormat
from PyQt5.QtWidgets           import (
    QApplication, QWidget, QVBoxLayout
)
from PyQt5.QtMultimedia        import QCamera, QCameraInfo, QVideoProbe
from PyQt5.QtMultimediaWidgets import QVideoWidget

class CameraApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("camera_qt (GPU accel via QVideoWidget)")
        self.resize(640, 480)

        # 1) (Optional) Request an OpenGL context for all windows
        fmt = QSurfaceFormat()
        fmt.setRenderableType(QSurfaceFormat.OpenGL)
        fmt.setProfile(QSurfaceFormat.CoreProfile)
        fmt.setVersion(2, 0)              # GL2.0+ is almost guaranteed on Win10
        QSurfaceFormat.setDefaultFormat(fmt)

        # 2) Pick default camera
        cam_info = QCameraInfo.defaultCamera()
        if cam_info.isNull():
            raise RuntimeError("No camera found")
        self.camera = QCamera(cam_info)

        # 3) Use QVideoWidget for native, accelerated video output
        self.viewfinder = QVideoWidget(self)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.viewfinder)
        self.camera.setViewfinder(self.viewfinder)

        # 4) Optional: hook raw frames for ML
        self.probe = QVideoProbe()
        self.probe.setSource(self.camera)
        self.probe.videoFrameProbed.connect(self.on_frame)

        # 5) Start camera
        self.camera.start()

    def on_frame(self, qframe):
        # Called for each QVideoFrame
        # Convert to QImage / numpy here for ML:
        # img = qframe.image()
        pass

    def closeEvent(self, event):
        self.camera.stop()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CameraApp()
    win.show()
    sys.exit(app.exec_())
