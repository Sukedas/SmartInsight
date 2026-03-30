from Model.budget_model import BudgetModel

class BudgetController:
    """Controlador para la gestión de presupuestos."""
    
    def __init__(self, view, db):
        self.view = view
        self.model = BudgetModel(db)
