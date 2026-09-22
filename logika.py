RAZMER = 5

PUSTO = ""
KREST = "X"
NOLIK = "O"


def sozdat_pole():
    pole = []
    for i in range(RAZMER):
        stroka = []
        for j in range(RAZMER):
            stroka.append(PUSTO)
        pole.append(stroka)
    return pole


def drugoy_simvol(simvol):
    if simvol == KREST:
        return NOLIK
    else:
        return KREST


def proverka_pobedy(pole):
    for i in range(RAZMER):
        for j in range(RAZMER - 3):
            simvol = pole[i][j]
            if simvol == PUSTO:
                continue
            schetchik = 0
            kletki = []
            for k in range(4):
                if pole[i][j + k] == simvol:
                    schetchik = schetchik + 1
                    kletki.append((i, j + k))
            if schetchik == 4:
                return simvol, kletki

    for i in range(RAZMER - 3):
        for j in range(RAZMER):
            simvol = pole[i][j]
            if simvol == PUSTO:
                continue
            schetchik = 0
            kletki = []
            for k in range(4):
                if pole[i + k][j] == simvol:
                    schetchik = schetchik + 1
                    kletki.append((i + k, j))
            if schetchik == 4:
                return simvol, kletki

    for i in range(RAZMER - 3):
        for j in range(RAZMER - 3):
            simvol = pole[i][j]
            if simvol == PUSTO:
                continue
            schetchik = 0
            kletki = []
            for k in range(4):
                if pole[i + k][j + k] == simvol:
                    schetchik = schetchik + 1
                    kletki.append((i + k, j + k))
            if schetchik == 4:
                return simvol, kletki

    for i in range(RAZMER - 3):
        for j in range(3, RAZMER):
            simvol = pole[i][j]
            if simvol == PUSTO:
                continue
            schetchik = 0
            kletki = []
            for k in range(4):
                if pole[i + k][j - k] == simvol:
                    schetchik = schetchik + 1
                    kletki.append((i + k, j - k))
            if schetchik == 4:
                return simvol, kletki

    return None


def vse_linii():
    spisok = []
    for i in range(RAZMER):
        for j in range(RAZMER - 3):
            liniya = []
            for k in range(4):
                liniya.append((i, j + k))
            spisok.append(liniya)
    for i in range(RAZMER - 3):
        for j in range(RAZMER):
            liniya = []
            for k in range(4):
                liniya.append((i + k, j))
            spisok.append(liniya)
    for i in range(RAZMER - 3):
        for j in range(RAZMER - 3):
            liniya = []
            for k in range(4):
                liniya.append((i + k, j + k))
            spisok.append(liniya)
    for i in range(RAZMER - 3):
        for j in range(3, RAZMER):
            liniya = []
            for k in range(4):
                liniya.append((i + k, j - k))
            spisok.append(liniya)
    return spisok


def mozhet_li_vyigrat(pole, simvol):
    linii = vse_linii()
    for liniya in linii:
        isporchena = False
        for kletka in liniya:
            i = kletka[0]
            j = kletka[1]
            if pole[i][j] != PUSTO and pole[i][j] != simvol:
                isporchena = True
        if isporchena == False:
            return True
    return False


def est_svobodnye_kletki(pole):
    for i in range(RAZMER):
        for j in range(RAZMER):
            if pole[i][j] == PUSTO:
                return True
    return False


def proverka_nichyi(pole):
    if est_svobodnye_kletki(pole) == False:
        return True
    if mozhet_li_vyigrat(pole, KREST) == False and mozhet_li_vyigrat(pole, NOLIK) == False:
        return True
    return False
