import sys

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton,
                             QLabel, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QStackedWidget, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

import logika
import bot

STR_MENU = 0
STR_VYBOR = 1
STR_IGRA = 2
STR_STAT = 3
STR_PRAVILA = 4

CVET_KRESTIKA = "#0b68eb"
CVET_NOLIKA = "#fa6f10"
CVET_RAMKI = "#dddddd"
CVET_LINIY = "#000000"
CVET_POBEDY = "#a9e8ad"
CVET_OSHIBKI = "#d32f2f"

STIL_KNOPKI = "QPushButton { background-color: #ffffff; color: #111111; font-size: 17px; " \
              "border: 1px solid " + CVET_RAMKI + "; border-radius: 10px; padding: 14px; } " \
              "QPushButton:hover { background-color: #f7f7f7; border-color: #b8b8b8; }"

STIL_KLETKI = "QPushButton { background-color: #ffffff; border: none; " \
              "font-size: 46px; font-weight: bold; }"

STIL_KLETKI_POBEDA = "QPushButton { background-color: " + CVET_POBEDY + "; border: none; " \
                     "font-size: 46px; font-weight: bold; }"

PRAVILA_TEKST = """ПРАВИЛА ИГРЫ «КРЕСТИКИ-НОЛИКИ 5 НА 5»

1. Игра идёт на поле размером 5 на 5 клеток.

2. Играют двое: один ставит крестики (X), другой нолики (O).
   Первыми всегда ходят крестики.

3. За один ход игрок ставит свой символ в любую свободную клетку.
   В занятую клетку поставить символ нельзя.

4. Побеждает тот, кто первым выстроит 4 своих символа подряд:
   по горизонтали, по вертикали или по диагонали.
   Победная линия подсвечивается зелёным цветом.

5. Если все клетки заняты, а победной комбинации нет — объявляется ничья.
   Ничья также объявляется раньше, если ни один игрок уже не может
   собрать линию из 4 символов.

6. В режиме «Игра с компьютером» вторым игроком управляет программа.
   Перед началом партии можно выбрать, за какую сторону играть.

7. Кнопка «Сдаться» завершает партию поражением того, чей сейчас ход.

8. Результаты всех сыгранных партий сохраняются в разделе «Статистика»
   до закрытия программы."""


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Крестики-нолики 5 на 5")
        self.resize(940, 660)
        self.setStyleSheet("background-color: #ffffff; color: #111111;")

        self.pole = logika.sozdat_pole()
        self.tekushchiy = logika.KREST
        self.igra_idet = False
        self.rezhim = "lokalno"
        self.simvol_igroka = logika.KREST
        self.simvol_bota = logika.NOLIK
        self.zhdem_bota = False

        self.pobedy_krestikov = 0
        self.pobedy_nolikov = 0
        self.nichyi = 0

        self.stranicy = QStackedWidget()
        self.setCentralWidget(self.stranicy)

        self.sdelat_menyu()
        self.sdelat_vybor_storony()
        self.sdelat_igrovoe_pole()
        self.sdelat_statistiku()
        self.sdelat_pravila()

        self.stranicy.setCurrentIndex(STR_MENU)

    def sdelat_menyu(self):
        stranica = QWidget()
        obshiy = QHBoxLayout()
        obshiy.setContentsMargins(60, 50, 60, 50)
        obshiy.setSpacing(50)

        levaya_chast = QVBoxLayout()
        levaya_chast.setSpacing(14)

        zagolovok = QLabel("КРЕСТИКИ-НОЛИКИ\n5 НА 5")
        zagolovok.setFont(QFont("Arial", 30, QFont.Weight.Bold))
        zagolovok.setStyleSheet("color: #111111;")
        levaya_chast.addWidget(zagolovok)
        levaya_chast.addSpacing(26)

        knopka1 = QPushButton("Игра с компьютером")
        knopka1.setStyleSheet(STIL_KNOPKI)
        knopka1.clicked.connect(self.nazhali_igra_s_kompyuterom)
        levaya_chast.addWidget(knopka1)

        knopka2 = QPushButton("Локальная игра")
        knopka2.setStyleSheet(STIL_KNOPKI)
        knopka2.clicked.connect(self.nazhali_lokalnaya_igra)
        levaya_chast.addWidget(knopka2)

        knopka3 = QPushButton("Статистика")
        knopka3.setStyleSheet(STIL_KNOPKI)
        knopka3.clicked.connect(self.otkryt_statistiku)
        levaya_chast.addWidget(knopka3)

        knopka4 = QPushButton("Правила")
        knopka4.setStyleSheet(STIL_KNOPKI)
        knopka4.clicked.connect(self.otkryt_pravila)
        levaya_chast.addWidget(knopka4)

        levaya_chast.addStretch()

        primer = [
            ["", "", "X", "", "O"],
            ["", "X", "", "O", ""],
            ["O", "X", "", "", ""],
            ["", "", "X", "X", ""],
            ["O", "", "", "", "X"],
        ]
        ramka = QWidget()
        ramka.setStyleSheet("background-color: " + CVET_LINIY + ";")
        setka = QGridLayout(ramka)
        setka.setSpacing(2)
        setka.setContentsMargins(0, 0, 0, 0)
        for i in range(5):
            for j in range(5):
                kletka = QLabel(primer[i][j])
                kletka.setAlignment(Qt.AlignmentFlag.AlignCenter)
                kletka.setFixedSize(68, 68)
                if primer[i][j] == "X":
                    cvet = CVET_KRESTIKA
                else:
                    cvet = CVET_NOLIKA
                kletka.setStyleSheet("background-color: #ffffff; font-size: 36px; "
                                     "font-weight: bold; color: " + cvet + ";")
                setka.addWidget(kletka, i, j)

        pravaya_chast = QVBoxLayout()
        pravaya_chast.addStretch()
        pravaya_chast.addWidget(ramka, 0, Qt.AlignmentFlag.AlignCenter)
        pravaya_chast.addStretch()

        obshiy.addLayout(levaya_chast, 1)
        obshiy.addLayout(pravaya_chast, 1)
        stranica.setLayout(obshiy)
        self.stranicy.addWidget(stranica)

    def sdelat_vybor_storony(self):
        stranica = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(140, 90, 140, 90)
        layout.setSpacing(16)

        nadpis = QLabel("За кого играем против компьютера?")
        nadpis.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        nadpis.setStyleSheet("color: #111111;")
        nadpis.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(nadpis)

        podskazka = QLabel("Крестики всегда ходят первыми")
        podskazka.setFont(QFont("Arial", 14))
        podskazka.setStyleSheet("color: #666666;")
        podskazka.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(podskazka)
        layout.addSpacing(24)

        knopka_x = QPushButton("Играть за крестики (X)")
        knopka_x.setStyleSheet(STIL_KNOPKI)
        knopka_x.clicked.connect(lambda: self.nachat_igru(logika.KREST))
        layout.addWidget(knopka_x)

        knopka_o = QPushButton("Играть за нолики (O)")
        knopka_o.setStyleSheet(STIL_KNOPKI)
        knopka_o.clicked.connect(lambda: self.nachat_igru(logika.NOLIK))
        layout.addWidget(knopka_o)

        nazad = QPushButton("Назад в меню")
        nazad.setStyleSheet(STIL_KNOPKI)
        nazad.clicked.connect(self.v_menyu)
        layout.addWidget(nazad)

        layout.addStretch()
        stranica.setLayout(layout)
        self.stranicy.addWidget(stranica)

    def otkryt_vybor(self):
        self.stranicy.setCurrentIndex(STR_VYBOR)

    def nazhali_igra_s_kompyuterom(self):
        self.rezhim = "kompyuter"
        self.otkryt_vybor()

    def nazhali_lokalnaya_igra(self):
        self.rezhim = "lokalno"
        self.nachat_igru(logika.KREST)

    def sdelat_igrovoe_pole(self):
        stranica = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(22)

        self.nadpis_hoda = QLabel("Ход игрока: X")
        self.nadpis_hoda.setFont(QFont("Arial", 27, QFont.Weight.Bold))
        self.nadpis_hoda.setStyleSheet("color: #111111;")
        self.nadpis_hoda.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.nadpis_hoda)

        self.taymer_nadpisi = QTimer(self)
        self.taymer_nadpisi.setSingleShot(True)
        self.taymer_nadpisi.timeout.connect(self.obnovit_nadpis_hoda)

        ramka = QWidget()
        ramka.setStyleSheet("background-color: " + CVET_LINIY + ";")
        setka = QGridLayout(ramka)
        setka.setSpacing(2)
        setka.setContentsMargins(2, 2, 2, 2)
        self.knopki = []
        for i in range(logika.RAZMER):
            stroka_knopok = []
            for j in range(logika.RAZMER):
                knopka = QPushButton("")
                knopka.setFixedSize(84, 84)
                knopka.setStyleSheet(STIL_KLETKI)
                knopka.clicked.connect(lambda _, a=i, b=j: self.klik_po_kletke(a, b))
                setka.addWidget(knopka, i, j)
                stroka_knopok.append(knopka)
            self.knopki.append(stroka_knopok)
        layout.addWidget(ramka, 0, Qt.AlignmentFlag.AlignCenter)

        sdatsya = QPushButton("СДАТЬСЯ")
        sdatsya.setStyleSheet(STIL_KNOPKI)
        sdatsya.setFixedWidth(280)
        sdatsya.clicked.connect(self.sdatsya)
        layout.addWidget(sdatsya, 0, Qt.AlignmentFlag.AlignCenter)

        stranica.setLayout(layout)
        self.stranicy.addWidget(stranica)

    def nachat_igru(self, simvol_igroka):
        self.simvol_igroka = simvol_igroka
        self.simvol_bota = logika.drugoy_simvol(simvol_igroka)
        self.novaya_igra()
        self.stranicy.setCurrentIndex(STR_IGRA)

    def novaya_igra(self):
        self.pole = logika.sozdat_pole()
        self.tekushchiy = logika.KREST
        self.igra_idet = True
        self.zhdem_bota = False

        for i in range(logika.RAZMER):
            for j in range(logika.RAZMER):
                self.knopki[i][j].setText("")
                self.knopki[i][j].setStyleSheet(STIL_KLETKI)

        self.obnovit_nadpis_hoda()
        self.stranicy.setCurrentIndex(STR_IGRA)

        if self.rezhim == "kompyuter" and self.simvol_bota == logika.KREST:
            self.zhdem_bota = True
            QTimer.singleShot(400, self.hod_kompyutera)

    def obnovit_nadpis_hoda(self):
        self.pokazat_nadpis("Ход игрока: " + self.tekushchiy)

    def pokazat_nadpis(self, tekst):
        self.taymer_nadpisi.stop()
        self.nadpis_hoda.setStyleSheet("color: #111111;")
        self.nadpis_hoda.setText(tekst)

    def soobshchit_kletka_zanyata(self):
        self.nadpis_hoda.setStyleSheet("color: " + CVET_OSHIBKI + ";")
        self.nadpis_hoda.setText("Клетка занята, выберите свободную")
        self.taymer_nadpisi.start(1500)

    def klik_po_kletke(self, i, j):
        if self.igra_idet == False:
            return
        if self.zhdem_bota == True:
            return
        if self.rezhim == "kompyuter" and self.tekushchiy != self.simvol_igroka:
            return
        if self.pole[i][j] != logika.PUSTO:
            self.soobshchit_kletka_zanyata()
            return

        self.postavit_simvol(i, j, self.tekushchiy)

        if self.proverit_konec_igry() == True:
            return

        self.tekushchiy = logika.drugoy_simvol(self.tekushchiy)
        self.obnovit_nadpis_hoda()

        if self.rezhim == "kompyuter":
            self.zhdem_bota = True
            QTimer.singleShot(400, self.hod_kompyutera)

    def postavit_simvol(self, i, j, simvol):
        self.pole[i][j] = simvol
        self.knopki[i][j].setText(simvol)
        if simvol == logika.KREST:
            cvet = CVET_KRESTIKA
        else:
            cvet = CVET_NOLIKA
        self.knopki[i][j].setStyleSheet(STIL_KLETKI + " QPushButton { color: " + cvet + "; }")

    def hod_kompyutera(self):
        self.zhdem_bota = False
        if self.igra_idet == False:
            return
        if self.stranicy.currentIndex() != STR_IGRA:
            return

        hod = bot.hod_kompyutera(self.pole, self.simvol_bota)
        if hod == None:
            return

        self.postavit_simvol(hod[0], hod[1], self.simvol_bota)

        if self.proverit_konec_igry() == True:
            return

        self.tekushchiy = logika.drugoy_simvol(self.tekushchiy)
        self.obnovit_nadpis_hoda()

    def sdatsya(self):
        if self.igra_idet == False:
            return
        self.igra_idet = False
        proigral = self.tekushchiy
        pobedil = logika.drugoy_simvol(proigral)
        if pobedil == logika.KREST:
            self.pobedy_krestikov = self.pobedy_krestikov + 1
        else:
            self.pobedy_nolikov = self.pobedy_nolikov + 1
        self.pokazat_nadpis("Игрок " + proigral + " сдался")
        self.pokazat_rezultat("Игрок " + proigral + " сдался.\nПобедил игрок " + pobedil + ".")

    def proverit_konec_igry(self):
        rezultat = logika.proverka_pobedy(self.pole)
        if rezultat != None:
            simvol = rezultat[0]
            kletki = rezultat[1]
            if simvol == logika.KREST:
                cvet = CVET_KRESTIKA
            else:
                cvet = CVET_NOLIKA
            for kletka in kletki:
                self.knopki[kletka[0]][kletka[1]].setStyleSheet(STIL_KLETKI_POBEDA + " QPushButton { color: " + cvet + "; }")
            self.igra_idet = False
            if simvol == logika.KREST:
                self.pobedy_krestikov = self.pobedy_krestikov + 1
            else:
                self.pobedy_nolikov = self.pobedy_nolikov + 1
            self.pokazat_nadpis("Победил игрок " + simvol)
            self.pokazat_rezultat("Победил игрок " + simvol + "!")
            return True

        if logika.proverka_nichyi(self.pole) == True:
            self.igra_idet = False
            self.nichyi = self.nichyi + 1
            self.pokazat_nadpis("Ничья")
            self.pokazat_rezultat("Ничья!")
            return True

        return False

    def pokazat_rezultat(self, tekst):
        okno = QMessageBox(self)
        okno.setWindowTitle("Результат партии")
        okno.setText(tekst)
        okno.setStyleSheet("QLabel { font-size: 18px; } " + STIL_KNOPKI)
        zanovo = okno.addButton("Начать партию заново", QMessageBox.ButtonRole.AcceptRole)
        okno.addButton("Выход в меню", QMessageBox.ButtonRole.RejectRole)
        okno.exec()
        self.posle_rezultata(okno.clickedButton() == zanovo)

    def posle_rezultata(self, nachat_zanovo):
        if nachat_zanovo == True:
            if self.rezhim == "kompyuter":
                self.otkryt_vybor()
            else:
                self.novaya_igra()
        else:
            self.v_menyu()

    def sdelat_statistiku(self):
        stranica = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(140, 80, 140, 80)
        layout.setSpacing(16)

        zagolovok = QLabel("Статистика текущей сессии")
        zagolovok.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        zagolovok.setStyleSheet("color: #111111;")
        zagolovok.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(zagolovok)
        layout.addSpacing(18)

        self.nadpis_stat_x = QLabel("")
        self.nadpis_stat_x.setFont(QFont("Arial", 16))
        self.nadpis_stat_x.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.nadpis_stat_x)

        self.nadpis_stat_o = QLabel("")
        self.nadpis_stat_o.setFont(QFont("Arial", 16))
        self.nadpis_stat_o.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.nadpis_stat_o)

        self.nadpis_stat_n = QLabel("")
        self.nadpis_stat_n.setFont(QFont("Arial", 16))
        self.nadpis_stat_n.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.nadpis_stat_n)

        self.nadpis_stat_vsego = QLabel("")
        self.nadpis_stat_vsego.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.nadpis_stat_vsego.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.nadpis_stat_vsego)

        layout.addSpacing(28)

        sbros = QPushButton("Сбросить статистику")
        sbros.setStyleSheet(STIL_KNOPKI)
        sbros.clicked.connect(self.sbrosit_statistiku)
        layout.addWidget(sbros)

        nazad = QPushButton("Выйти в меню")
        nazad.setStyleSheet(STIL_KNOPKI)
        nazad.clicked.connect(self.v_menyu)
        layout.addWidget(nazad)

        layout.addStretch()
        stranica.setLayout(layout)
        self.stranicy.addWidget(stranica)

    def otkryt_statistiku(self):
        self.obnovit_statistiku()
        self.stranicy.setCurrentIndex(STR_STAT)

    def obnovit_statistiku(self):
        vsego = self.pobedy_krestikov + self.pobedy_nolikov + self.nichyi
        self.nadpis_stat_x.setText("Побед крестиков (X): " + str(self.pobedy_krestikov))
        self.nadpis_stat_o.setText("Побед ноликов (O): " + str(self.pobedy_nolikov))
        self.nadpis_stat_n.setText("Ничьих: " + str(self.nichyi))
        self.nadpis_stat_vsego.setText("Всего сыграно партий: " + str(vsego))

    def sbrosit_statistiku(self):
        self.pobedy_krestikov = 0
        self.pobedy_nolikov = 0
        self.nichyi = 0
        self.obnovit_statistiku()

    def sdelat_pravila(self):
        stranica = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(80, 45, 80, 45)
        layout.setSpacing(18)

        tekst = QLabel(PRAVILA_TEKST)
        tekst.setFont(QFont("Arial", 12))
        tekst.setStyleSheet("color: #111111; background-color: #ffffff; "
                            "border: 1px solid " + CVET_RAMKI + "; "
                            "border-radius: 10px; padding: 20px;")
        tekst.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        tekst.setWordWrap(True)
        layout.addWidget(tekst)

        nazad = QPushButton("Выйти в меню")
        nazad.setStyleSheet(STIL_KNOPKI)
        nazad.clicked.connect(self.v_menyu)
        layout.addWidget(nazad)

        stranica.setLayout(layout)
        self.stranicy.addWidget(stranica)

    def otkryt_pravila(self):
        self.stranicy.setCurrentIndex(STR_PRAVILA)

    def v_menyu(self):
        self.igra_idet = False
        self.zhdem_bota = False
        self.stranicy.setCurrentIndex(STR_MENU)


def main():
    prilozhenie = QApplication(sys.argv)
    okno = MainWindow()
    okno.show()
    sys.exit(prilozhenie.exec())


if __name__ == "__main__":
    main()
