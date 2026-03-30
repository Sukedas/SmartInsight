from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

class TransactionView(QWidget):
    """Vista para el registro y consulta de transacciones (RF1, RF5)."""
    
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        self.label = QLabel("Gestión de Transacciones")
        self.layout.addWidget(self.label)
        
        self.btn_add = QPushButton("Nueva Transacción")
        self.layout.addWidget(self.btn_add)
