from Model.transaction_model import TransactionModel

class TransactionController:
    """Controlador específico para manejar eventos de transacciones."""
    
    def __init__(self, view, db):
        self.view = view
        self.model = TransactionModel(db)
        
        self.connect_signals()
        
    def connect_signals(self):
        self.view.btn_add.clicked.connect(self.on_add_transaction)
        
    def on_add_transaction(self):
        print("Abriendo diálogo para nueva transacción...")
        # Lógica para mostrar popup y guardar la transacción en el modelo
