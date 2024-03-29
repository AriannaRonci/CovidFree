from datetime import date

from PyQt5 import QtGui
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListView, QVBoxLayout, QPushButton, QLabel, QGridLayout, QMessageBox

from appuntamentotampone.view.VistaAppuntamentoTampone import VistaAppuntamentoTampone
from calendariotamponi.view.VistaModificaAppuntamentoTampone import VistaModificaAppuntamentoTampone


class VistaListaAppuntamentiTamponi(QWidget):
    def __init__(self, controller, data):

        super(VistaListaAppuntamentiTamponi, self).__init__()
        self.controller = controller
        self.data = data

        self.elenco_antigenico = []
        self.elenco_molecolare = []
        self.elenco_sierologico = []

        h_layout = QHBoxLayout()
        self.list_view = QListView()
        h_layout.addWidget(self.list_view)

        self.grid_layout = QGridLayout()

        self.list_view_antigenico = QListView()
        self.list_view_molecolare = QListView()
        self.list_view_sierologico = QListView()

        self.update_ui()

        self.get_list("Appuntamenti Antigenico", 0)
        self.get_list("Appuntamenti Molecolare", 1)
        self.get_list("Appuntamenti Sierologico", 2)

        self.grid_layout.addWidget(self.list_view_antigenico, 1, 0)
        self.grid_layout.addWidget(self.list_view_molecolare, 1, 1)
        self.grid_layout.addWidget(self.list_view_sierologico, 1, 2)

        visualizza_antigenico = QPushButton("Visualizza")
        elimina_antigenico = QPushButton("Elimina")
        modifica_antigenico = QPushButton("Modifica")
        self.grid_layout.addWidget(visualizza_antigenico, 2, 0)
        self.grid_layout.addWidget(elimina_antigenico, 3, 0)
        self.grid_layout.addWidget(modifica_antigenico, 4, 0)
        visualizza_antigenico.clicked.connect(self.show_selected_info_antigenico)
        elimina_antigenico.clicked.connect(self.elimina_appuntamento_antigenico)
        modifica_antigenico.clicked.connect(self.modifica_appuntamento_antigenico)

        visualizza_molecolare = QPushButton("Visualizza")
        elimina_molecolare = QPushButton("Elimina")
        modifica_molecolare = QPushButton("Modifica")
        self.grid_layout.addWidget(visualizza_molecolare, 2, 1)
        self.grid_layout.addWidget(elimina_molecolare, 3, 1)
        self.grid_layout.addWidget(modifica_molecolare, 4, 1)
        visualizza_molecolare.clicked.connect(self.show_selected_info_molecolare)
        elimina_molecolare.clicked.connect(self.elimina_appuntamento_molecolare)
        modifica_molecolare.clicked.connect(self.modifica_appuntamento_molecolare)

        visualizza_sierologico = QPushButton("Visualizza")
        elimina_sierologico = QPushButton("Elimina")
        modifica_sierologico = QPushButton("Modifica")
        self.grid_layout.addWidget(visualizza_sierologico, 2, 2)
        self.grid_layout.addWidget(elimina_sierologico, 3, 2)
        self.grid_layout.addWidget(modifica_sierologico, 4, 2)
        visualizza_sierologico.clicked.connect(self.show_selected_info_sierologico)
        elimina_sierologico.clicked.connect(self.elimina_appuntamento_sierologico)
        modifica_sierologico.clicked.connect(self.modifica_appuntamento_sierologico)

        self.setLayout(self.grid_layout)
        self.setFont(QFont('Arial Nova Light', 14))
        self.setWindowTitle('Lista Appuntamenti Tamponi Giorno: {}'.format(self.data))
        self.setWindowIcon(QIcon('appuntamentovaccino/data/CovidFree_Clinica.png'))

        self.setMaximumSize(910, 400)
        self.resize(910, 400)
        self.move(0, 0)

    # Funzione per la creazione di un layout in cui vengono elencati gli appuntamenti.
    def get_list(self, tipologia, colonna):
        v_layout_tipologia = QVBoxLayout()
        label_tipologia = QLabel(tipologia)
        font_tipologia = label_tipologia.font()
        font_tipologia.setPointSize(15)
        font_tipologia.setItalic(True)
        label_tipologia.setFont(font_tipologia)
        v_layout_tipologia.addWidget(label_tipologia)

        self.grid_layout.addLayout(v_layout_tipologia, 0, colonna)

    # Funzione per la visualizzazione dell'appuntamento selezionato nella lista.
    def show_selected_info_molecolare(self):
        if self.list_view_molecolare.selectedIndexes():
            selected = self.list_view_molecolare.selectedIndexes()[0].row()
            appuntamento_selezionato = self.elenco_molecolare[selected]
            self.vista_tampone = VistaAppuntamentoTampone(appuntamento_selezionato)
            self.vista_tampone.show()
            self.update_ui()

    # Funzione per la visualizzazione dell'appuntamento selezionato nella lista.
    def show_selected_info_antigenico(self):
        if self.list_view_antigenico.selectedIndexes():
            selected = self.list_view_antigenico.selectedIndexes()[0].row()
            appuntamento_selezionato = self.elenco_antigenico[selected]
            self.vista_tampone = VistaAppuntamentoTampone(appuntamento_selezionato)
            self.vista_tampone.show()
            self.update_ui()

    # Funzione per la visualizzazione dell'appuntamento selezionato nella lista.
    def show_selected_info_sierologico(self):
        if self.list_view_sierologico.selectedIndexes():
            selected = self.list_view_sierologico.selectedIndexes()[0].row()
            appuntamento_selezionato = self.elenco_sierologico[selected]
            self.vista_tampone = VistaAppuntamentoTampone(appuntamento_selezionato)
            self.vista_tampone.show()
            self.update_ui()

    # Funzione che inserisce un appuntamento nello specifico elenco.
    def update_ui(self):
        self.list_view_antigenico_model = QStandardItemModel(self.list_view_antigenico)
        self.list_view_molecolare_model = QStandardItemModel(self.list_view_molecolare)
        self.list_view_sierologico_model = QStandardItemModel(self.list_view_sierologico)

        for appuntamento in self.controller.get_elenco_appuntamenti():
            item = QStandardItem()
            if appuntamento.data_appuntamento == self.data:
                item.setText(appuntamento.nome + " " + appuntamento.cognome)
                item.setEditable(False)
                font = item.font()
                font.setPointSize(12)
                item.setFont(font)
                if appuntamento.is_drive_through:
                    item.setBackground(QtGui.QColor(255,255,153))
                if appuntamento.tipo_tampone == "Antigenico Rapido":
                    self.list_view_antigenico_model.appendRow(item)
                    self.elenco_antigenico.append(appuntamento)
                elif appuntamento.tipo_tampone == "Molecolare":
                    self.list_view_molecolare_model.appendRow(item)
                    self.elenco_molecolare.append(appuntamento)
                elif appuntamento.tipo_tampone == "Sierologico":
                    self.list_view_sierologico_model.appendRow(item)
                    self.elenco_sierologico.append(appuntamento)

        self.list_view_antigenico.setModel(self.list_view_antigenico_model)
        self.list_view_molecolare.setModel(self.list_view_molecolare_model)
        self.list_view_sierologico.setModel(self.list_view_sierologico_model)

    # Funzione per l'eliminazione dell'appuntamento selezionato dalla lista dei tamponi "Antigenico Rapido"
    def elimina_appuntamento_antigenico(self):
        if self.list_view_antigenico.selectedIndexes():
            selected = self.list_view_antigenico.selectedIndexes()[0].row()
            appuntamento_selezionato = self.elenco_antigenico[selected]

            if appuntamento_selezionato.data_appuntamento < str(date.today()):
                QMessageBox.critical(self, 'Errore', 'Non è possibile eliminare appuntamenti passati',
                                     QMessageBox.Ok, QMessageBox.Ok)
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)

                msg.setText("Sei sicuro di voler eliminare l'appuntamento?")
                msg.setInformativeText("La decisione è irreversibile!")
                msg.setWindowTitle("Conferma eliminazione")
                msg.setWindowIcon(QIcon('appuntamentovaccino/data/CovidFree_Clinica.png'))
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

                msg.move(250, 100)

                if msg.exec() == QMessageBox.Ok:
                    self.controller.lettura_magazzino()
                    self.controller.aggiorna_magazzino(appuntamento_selezionato.tipo_tampone)
                    self.controller.elimina_appuntamento(appuntamento_selezionato)
                    self.elenco_antigenico.remove(appuntamento_selezionato)
                self.update_ui()

    # Funzione per l'eliminazione dell'appuntamento selezionato dalla lista dei tamponi "Molecolare"
    def elimina_appuntamento_molecolare(self):
        if self.list_view_molecolare.selectedIndexes():
            selected = self.list_view_molecolare.selectedIndexes()[0].row()
            appuntamento_selezionato = self.elenco_molecolare[selected]

            if appuntamento_selezionato.data_appuntamento < str(date.today()):
                QMessageBox.critical(self, 'Errore', 'Non è possibile eliminare appuntamenti passati',
                                     QMessageBox.Ok, QMessageBox.Ok)
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)

                msg.setText("Sei sicuro di voler eliminare l'appuntamento?")
                msg.setInformativeText("La decisione è irreversibile!")
                msg.setWindowTitle("Conferma eliminazione")
                msg.setWindowIcon(QIcon('appuntamentovaccino/data/CovidFree_Clinica.png'))
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

                msg.move(250, 100)

                if msg.exec() == QMessageBox.Ok:
                    self.controller.lettura_magazzino()
                    self.controller.aggiorna_magazzino(appuntamento_selezionato.tipo_tampone)
                    self.controller.elimina_appuntamento(appuntamento_selezionato)
                    self.elenco_molecolare.remove(appuntamento_selezionato)
                self.update_ui()

    # Funzione per l'eliminazione dell'appuntamento selezionato dalla lista dei tamponi "Sierologico"
    def elimina_appuntamento_sierologico(self):
        if self.list_view_sierologico.selectedIndexes():
            selected = self.list_view_sierologico.selectedIndexes()[0].row()
            appuntamento_selezionato = self.elenco_sierologico[selected]

            if appuntamento_selezionato.data_appuntamento < str(date.today()):
                QMessageBox.critical(self, 'Errore', 'Non è possibile eliminare appuntamenti passati',
                                     QMessageBox.Ok, QMessageBox.Ok)
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)

                msg.setText("Sei sicuro di voler eliminare l'appuntamento?")
                msg.setInformativeText("La decisione è irreversibile!")
                msg.setWindowTitle("Conferma eliminazione")
                msg.setWindowIcon(QIcon('appuntamentovaccino/data/CovidFree_Clinica.png'))
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

                msg.move(250, 100)

                if msg.exec() == QMessageBox.Ok:
                    self.controller.lettura_magazzino()
                    self.controller.aggiorna_magazzino(appuntamento_selezionato.tipo_tampone)
                    self.controller.elimina_appuntamento(appuntamento_selezionato)
                    self.elenco_sierologico.remove(appuntamento_selezionato)
                self.update_ui()

    # Funzione per la modifica dell'appuntamento selezionato dalla lista dei tamponi "Antigenico Rapido"
    def modifica_appuntamento_antigenico(self):
        if self.list_view_antigenico.selectedIndexes():
            selected = self.list_view_antigenico.selectedIndexes()[0].row()
            appuntamento_selezionato = self.elenco_antigenico[selected]

            if appuntamento_selezionato.data_appuntamento < str(date.today()):
                QMessageBox.critical(self, 'Errore', 'Non è possibile modificare appuntamenti passati',
                                     QMessageBox.Ok, QMessageBox.Ok)
            else:
                self.vista_modifica = VistaModificaAppuntamentoTampone(self.controller, appuntamento_selezionato)
                self.vista_modifica.show()
                self.close()

    # Funzione per la modifica dell'appuntamento selezionato dalla lista dei tamponi "Molecolare"
    def modifica_appuntamento_molecolare(self):
        if self.list_view_molecolare.selectedIndexes():
            selected = self.list_view_molecolare.selectedIndexes()[0].row()
            appuntamento_selezionato = self.elenco_molecolare[selected]

            if appuntamento_selezionato.data_appuntamento < str(date.today()):
                QMessageBox.critical(self, 'Errore', 'Non è possibile modificare appuntamenti passati',
                                     QMessageBox.Ok, QMessageBox.Ok)
            else:
                self.vista_modifica = VistaModificaAppuntamentoTampone(self.controller, appuntamento_selezionato)
                self.vista_modifica.show()
                self.close()

    # Funzione per la modifica dell'appuntamento selezionato dalla lista dei tamponi "Sierologico"
    def modifica_appuntamento_sierologico(self):
        if self.list_view_sierologico.selectedIndexes():
            selected = self.list_view_sierologico.selectedIndexes()[0].row()
            appuntamento_selezionato = self.elenco_sierologico[selected]
            if appuntamento_selezionato.data_appuntamento < str(date.today()):
                QMessageBox.critical(self, 'Errore', 'Non è possibile modificare appuntamenti passati',
                                     QMessageBox.Ok, QMessageBox.Ok)
            else:
                self.vista_modifica = VistaModificaAppuntamentoTampone(self.controller, appuntamento_selezionato)
                self.vista_modifica.show()
                self.close()