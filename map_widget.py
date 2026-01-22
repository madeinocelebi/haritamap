import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView

class HaritaWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- Ayarlar ---
        self.genislik = 400
        self.yukseklik = 700
        self.cerceve_kalinligi = 5  # Çerçevenin kalınlığı
        self.cerceve_rengi = "#333333" # Şimdilik belirgin olsun diye 'Kırmızı' yaptım. 
                                       # Siyah/Gri için: #333333 yapabilirsin.
        
        self.harita_url = "https://www.google.com/maps" 
        # ----------------

        self.setWindowTitle("Masaüstü Haritam")

        # 1. Ana Taşıyıcı Kutu (Bu bizim çerçewemiz olacak)
        self.ana_kutu = QFrame()
        
        # Kutunun arka planını boyuyoruz (Çerçeve rengi bu)
        self.ana_kutu.setStyleSheet(f"background-color: {self.cerceve_rengi}; border-radius: 4px;")

        # 2. Düzen (Layout) Ayarları
        self.layout = QVBoxLayout(self.ana_kutu)
        
        # MARJİN: İçeriği kenarlardan itiyoruz. Bu boşlukta alttaki renk görünecek.
        self.layout.setContentsMargins(
            self.cerceve_kalinligi, 
            self.cerceve_kalinligi, 
            self.cerceve_kalinligi, 
            self.cerceve_kalinligi
        )
        self.layout.setSpacing(0)

        # 3. Web Tarayıcı (Harita)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(self.harita_url))
        
        # Haritanın kendisine stil vermiyoruz, layout'a ekliyoruz.
        self.layout.addWidget(self.browser)

        # Ana pencereye bu kutuyu set et
        self.setCentralWidget(self.ana_kutu)

        # 4. Pencere Özellikleri
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 5. Konumlandırma
        self.konumlandir()

    def konumlandir(self):
        screen = QApplication.primaryScreen()
        rect = screen.availableGeometry() 

        # Sağ üst köşe hesabı (Boşlukları biraz artırdım estetik dursun diye)
        x = rect.width() - self.genislik - 25
        y = rect.y() + 25

        self.setGeometry(x, y, self.genislik, self.yukseklik)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HaritaWidget()
    window.show()
    sys.exit(app.exec_())
