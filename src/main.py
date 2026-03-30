import sys
from PyQt6.QtWidgets import QApplication
from Controller.main_controller import MainController
from Model.database import Database
from View.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Inicializar Base de Datos
    db = Database()
    
    # Inicializar Vista Principal
    view = MainWindow()
    
    # Inicializar Controlador Principal
    controller = MainController(view, db)
    
    # Mostrar la aplicación
    view.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
