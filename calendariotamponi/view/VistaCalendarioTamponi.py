from datetime import datetime
import calendar
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWidget, QCalendarWidget, QSizePolicy, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, \
    QGridLayout, QDesktopWidget
from PyQt5.QtCore import QDate, Qt

from calendariotamponi.controller.ControlloreCalendarioTamponi import ControlloreCalendarioTamponi
from calendariotamponi.view.VistaInserisciAppuntamentoTampone import VistaInserisciAppuntamentoTampone
from calendariotamponi.view.VistaListaAppuntamentiTamponi import VistaListaAppuntamentiTamponi
from calendariotamponi.view.VistaRicercaAppuntamentoTampone import VistaRicercaAppuntamentoTampone


class VistaCalendarioTamponi(QWidget):

    def __init__(self, parent=None):

        super(VistaCalendarioTamponi, self).__init__(parent)
        self.controller = ControlloreCalendarioTamponi()
        self.calendario_tamponi = self.init_calendario()

        grid_layout = QGridLayout()
        calendar_layout = QVBoxLayout()
        calendar_layout.addWidget(self.calendario_tamponi)

        self.calendario_tamponi.selectionChanged.connect(self.calendar_date)
        self.label = QLabel('')
        calendar_layout.addWidget(self.label)


        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.get_generic_button("Visualizza", self.show_selected_data))
        buttons_layout.addWidget(self.get_generic_button("Aggiungi Appuntamento", self.show_add_appuntamento))
        buttons_layout.addWidget(self.get_generic_button("Ricerca Appuntamento", self.show_ricerca_appuntamento))

        grid_layout.addLayout(calendar_layout, 0, 0)
        grid_layout.addLayout(buttons_layout, 0, 1, alignment=Qt.AlignBottom)

        self.setLayout(grid_layout)
        self.setWindowTitle("Calendario Appuntamenti Tamponi")
        self.setWindowIcon(QIcon('appuntamentovaccino/data/CovidFree_Clinica.png'))

        self.setMaximumSize(1000, 650)
        self.resize(915, 650)
        self.move(0, 0)

    def init_calendario(self):
        calendario = QCalendarWidget(self)
        currentMonth = datetime.now().month
        currentYear = datetime.now().year


        calendario.setMinimumDate(QDate(currentYear, currentMonth, 1))
        calendario.setMaximumDate(
            QDate(currentYear + 1, currentMonth, calendar.monthrange(currentYear, currentMonth)[1]))
        calendario.setSelectedDate(QDate(currentYear, currentMonth, 1))

        calendario.setFont(QFont('Georgia', 10))
        calendario.setStyleSheet('background-color: lightblue')

        calendario.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        calendario.setGeometry(200, 200, 300, 200)
        calendario.setGridVisible(True)
        return calendario

    def get_generic_button(self, titolo, on_click):
        button = QPushButton(titolo)
        button.setFont(QFont('Georgia', 13))
        button.clicked.connect(on_click)
        return button

    def show_selected_data(self):
        self.vista_visualizza_appuntamenti = VistaListaAppuntamentiTamponi(self.controller, self.calendar_date(), self.update_ui)
        self.vista_visualizza_appuntamenti.show()

    def show_add_appuntamento(self):
        self.vista_inserisci_appuntamento = VistaInserisciAppuntamentoTampone(self.controller, self.update_ui)
        self.vista_inserisci_appuntamento.show()

    def show_ricerca_appuntamento(self):
        self.vista_ricerca_appuntamento = VistaRicercaAppuntamentoTampone()
        self.vista_ricerca_appuntamento.show()

    def update_ui(self):
        pass

    def calendar_date(self):
        dateselected = self.calendario_tamponi.selectedDate()
        data_selezionata = str(dateselected.toPyDate())

        self.label.setText("Data selezionata : " + data_selezionata)
        return data_selezionata