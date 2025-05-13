import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QSpinBox, QMessageBox
)
from PyQt5.QtGui import QIcon

from iqoptionapi.stable_api import IQ_Option
from datetime import datetime

class Prometey(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prometey - Trading Opciones Binarias")
        # self.setWindowIcon(QIcon("prometey.ico"))
        self.api = None

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Correo electrónico")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Iniciar sesión")
        self.login_button.clicked.connect(self.login)

        self.status_label = QLabel("Estado: No conectado")

        # Operaciones
        self.asset_box = QComboBox()
        self.asset_box.addItems(["EURUSD", "USDJPY", "GBPUSD", "EURJPY"])

        self.time_spin = QSpinBox()
        self.time_spin.setRange(1, 5)
        self.time_spin.setValue(1)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Monto ($)")

        self.call_button = QPushButton("CALL (Sube)")
        self.put_button = QPushButton("PUT (Baja)")
        self.call_button.clicked.connect(lambda: self.trade("call"))
        self.put_button.clicked.connect(lambda: self.trade("put"))
        self.call_button.setEnabled(False)
        self.put_button.setEnabled(False)

        # Disposición
        layout.addWidget(QLabel("Correo electrónico:"))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("Contraseña:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.status_label)

        layout.addWidget(QLabel("Activo:"))
        layout.addWidget(self.asset_box)
        layout.addWidget(QLabel("Tiempo (minutos):"))
        layout.addWidget(self.time_spin)
        layout.addWidget(QLabel("Monto ($):"))
        layout.addWidget(self.amount_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.call_button)
        button_layout.addWidget(self.put_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        self.api = IQ_Option(email, password)
        self.api.connect()

        if self.api.check_connect():
            self.status_label.setText("Estado: Conectado")
            QMessageBox.information(self, "Éxito", "Inicio de sesión exitoso.")
            self.call_button.setEnabled(True)
            self.put_button.setEnabled(True)
        else:
            QMessageBox.critical(self, "Error", "Error al iniciar sesión.")
            self.status_label.setText("Estado: No conectado")

    def trade(self, direction):
        asset = self.asset_box.currentText()
        time = self.time_spin.value()
        try:
            amount = float(self.amount_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Monto inválido.")
            return
        
        self.api.change_balance("PRACTICE")  # o "REAL"
        success, trade_id = self.api.buy(amount, asset, direction, time)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if success:
            QMessageBox.information(self, "Éxito", f"Operación realizada ({direction.upper()})")
            self.save_trade(now, asset, direction, amount, time)
        else:
            QMessageBox.critical(self, "Error", "No se pudo ejecutar la operación.")

    def save_trade(self, timestamp, asset, direction, amount, duration):
        history = {
            "Fecha": [timestamp],
            "Activo": [asset],
            "Dirección": [direction.upper()],
            "Monto": [amount],
            "Duración": [duration]
        }
        df = pd.DataFrame(history)

        path = os.path.join(os.path.expanduser("~"), "Documents", "prometey_historial.csv")
        if not os.path.exists(path):
            df.to_csv(path, index=False, mode='w', encoding='utf-8-sig')
        else:
            df.to_csv(path, index=False, mode='a', header=False, encoding='utf-8-sig')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Prometey()
    window.resize(350, 450)
    window.show()
    sys.exit(app.exec_())