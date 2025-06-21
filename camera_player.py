# camera_qt.py
import sys
from PyQt5.QtWidgets           import QApplication, QWidget, QVBoxLayout
from PyQt5.QtMultimedia        import QCamera, QCameraInfo, QVideoProbe
from PyQt5.QtMultimediaWidgets import QCameraViewfinder

class CameraApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("camera_qt (PyQt5 QCamera)")
        self.resize(640, 480)

        # 1) select default camera
        cam_info = QCameraInfo.defaultCamera()
        if cam_info.isNull():
            raise RuntimeError("No camera found")
        self.camera = QCamera(cam_info)

        # 2) viewfinder widget for live preview
        self.viewfinder = QCameraViewfinder(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.viewfinder)
        self.camera.setViewfinder(self.viewfinder)

        # 3) optional: grab raw frames for ML
        self.probe = QVideoProbe()
        self.probe.setSource(self.camera)
        self.probe.videoFrameProbed.connect(self.on_frame)

        # 4) start camera
        self.camera.start()

    def on_frame(self, frame):
        # frame is a QVideoFrame
        # Convert to QImage, then to bytes/NumPy for ML:
        img = frame.image()  
        # e.g.:
        # ptr = img.bits()
        # ptr.setsize(img.byteCount())
        # arr = np.frombuffer(ptr, dtype=np.uint8).reshape(img.height(), img.width(), 4)
        # ...feed arr into your model...
        # (or skip this entirely if you just wanted preview)
        pass

    def closeEvent(self, event):
        self.camera.stop()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CameraApp()
    win.show()
    sys.exit(app.exec_())
