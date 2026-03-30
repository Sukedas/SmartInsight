from Controller.transaction_controller import TransactionController
from View.dashboard_view import DashboardView
from View.transaction_view import TransactionView

class MainController:
    """Controlador principal que gestiona el flujo de la aplicación."""
    
    def __init__(self, view, db):
        self.view = view
        self.db = db
        
        self.setup_ui()
        
    def setup_ui(self):
        # Inicializar sub-vistas
        self.dashboard_view = DashboardView()
        self.transaction_view = TransactionView()
        
        # Agregar pestañas a la vista principal
        self.view.tabs.addTab(self.dashboard_view, "Dashboard")
        self.view.tabs.addTab(self.transaction_view, "Transacciones")
        
        # Inicializar sub-controladores
        self.trans_controller = TransactionController(self.transaction_view, self.db)
