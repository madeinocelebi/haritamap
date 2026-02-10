import sys
import os
import json
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QUrl, QPoint
from PyQt6.QtGui import QPainter, QColor, QBrush, QRegion, QPainterPath
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage, QWebEngineScript

class MacMusicWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.config_file = os.path.expanduser("~/.macos_music_config.json")
        
        # PENCERE AYARLARI
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                            Qt.WindowType.WindowStaysOnBottomHint | 
                            Qt.WindowType.Tool)
        
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Genişlik biraz arttı, içerik sıkışmasın
        self.resize(460, 750) 

        # Düzen
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # 1. TUTMA ÇUBUĞU (Gizli - Sürüklemek için)
        self.header = QWidget()
        self.header.setFixedHeight(30)
        self.header.setStyleSheet("background-color: transparent;")
        self.layout.addWidget(self.header)

        # 2. TARAYICI
        self.browser = QWebEngineView()
        
        # --- KRİTİK AYAR: ZOOM ---
        # 0.20 yaptık (%30). Artık her şey çok daha minik ve sığmış olacak.
        self.browser.setZoomFactor(0.20) 
        
        # Oturum ve Profil
        storage_path = os.path.join(os.getcwd(), "yt_oturum")
        self.profile = QWebEngineProfile("yt_profile", self.browser)
        self.profile.setPersistentStoragePath(storage_path)
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
        
        # CSS ile Şeffaflık
        script = QWebEngineScript()
        s = """
            /* Arka planları şeffaf yap */
            html, body, ytmusic-app, ytmusic-app-layout, #content, ytmusic-player-bar, ytmusic-browse-response {
                background-color: transparent !important;
                background: transparent !important;
            }
            /* Alt barı belirginleştir */
            ytmusic-player-bar {
                background-color: rgba(0,0,0,0.5) !important;
                backdrop-filter: blur(10px);
            }
            /* Gereksiz scrollbar'ı yok et */
            ::-webkit-scrollbar { width: 0px; background: transparent; }
        """
        script.setName("TransparentBackground")
        script.setSourceCode(s)
        script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentReady)
        script.setWorldId(QWebEngineScript.ScriptWorldId.ApplicationWorld)
        self.profile.scripts().insert(script)

        page = QWebEnginePage(self.profile, self.browser)
        page.setBackgroundColor(Qt.GlobalColor.transparent)
        self.browser.setPage(page)
        
        self.browser.setUrl(QUrl("https://music.youtube.com"))
        self.layout.addWidget(self.browser)

        self.oldPos = None
        self.load_position()

    def load_position(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    data = json.load(f)
                    self.move(data.get("x", 1000), data.get("y", 100))
            except: pass

    def save_position(self):
        data = {"x": self.x(), "y": self.y()}
        try:
            with open(self.config_file, "w") as f:
                json.dump(data, f)
        except: pass

    # --- SÜRÜKLEME ---
    def mousePressEvent(self, event):
        # Sadece üstteki 30px'lik alana tıklanırsa sürükle
        if event.button() == Qt.MouseButton.LeftButton and event.position().y() < 30:
            self.oldPos = event.globalPosition().toPoint()
        else:
            self.oldPos = None

    def mouseMoveEvent(self, event):
        if self.oldPos:
            delta = event.globalPosition().toPoint() - self.oldPos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        if self.oldPos:
            self.oldPos = None
            self.save_position()

    # --- ÇİZİM ---
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        # Arka plan rengi (Yarı şeffaf koyu gri)
        painter.setBrush(QBrush(QColor(20, 20, 20, 180))) 
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 25, 25)

    def resizeEvent(self, event):
        # Köşeleri Yuvarlat
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 25, 25)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)
        super().resizeEvent(event)

if __name__ == "__main__":
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox"
    app = QApplication(sys.argv)
    window = MacMusicWidget()
    window.show()
    sys.exit(app.exec())
