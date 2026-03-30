from PyQt6.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    """Ventana principal de la aplicación con navegación por pestañas (RNF2)."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartInsight - Finanzas Personales")
        self.resize(800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)
        
        # Las pestañas se agregarán desde el controlador
