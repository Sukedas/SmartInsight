from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class DashboardView(QWidget):
    """Vista para mostrar los gráficos e indicadores principales (RF3, RF9)."""
    
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        # Placeholder para gráficos de matplotlib
        self.title = QLabel("Dashboard - Distribución de Gastos")
        self.layout.addWidget(self.title)
        
        # Aquí se integrarán los canvas de matplotlib para mostrar RF3 y RF4
