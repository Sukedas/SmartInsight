class TransactionModel:
    """Modelo para manejar la lógica de las transacciones (RF1, RF2, RF5, RF7)."""
    
    def __init__(self, database):
        self.db = database

    def add_transaction(self, date, amount, category, trans_type, is_recurring):
        query = '''
            INSERT INTO transactions (date, amount, category, type, is_recurring)
            VALUES (?, ?, ?, ?, ?)
        '''
        self.db.execute_query(query, (date, amount, category, trans_type, is_recurring))

    def get_transactions_by_period(self, start_date, end_date):
        query = 'SELECT * FROM transactions WHERE date BETWEEN ? AND ?'
        return self.db.fetch_all(query, (start_date, end_date))
        
    def get_max_expense_day_in_month(self, month, year):
        # Lógica para identificar el día de mayor gasto (RF7)
        pass
