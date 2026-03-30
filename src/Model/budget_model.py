class BudgetModel:
    """Modelo para gestionar los presupuestos por categoría o generales (RF6)."""
    
    def __init__(self, database):
        self.db = database

    def set_budget(self, category, amount, period):
        query = '''
            INSERT INTO budgets (category, amount, period)
            VALUES (?, ?, ?)
        '''
        self.db.execute_query(query, (category, amount, period))

    def get_budget_vs_actual(self, category, period):
        # Comparación presupuesto vs gasto real (RF4)
        pass
