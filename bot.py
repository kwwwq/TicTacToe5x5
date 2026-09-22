import random
import logika


def spisok_svobodnyh(pole):
    svobodnye = []
    for i in range(logika.RAZMER):
        for j in range(logika.RAZMER):
            if pole[i][j] == logika.PUSTO:
                svobodnye.append((i, j))
    return svobodnye


def ocenit_kletku(pole, i, j, simvol):
    ocenka = 0
    for liniya in logika.vse_linii():
        nashe = 0
        chuzhoe = 0
        vnutri = False
        for kletka in liniya:
            if kletka[0] == i and kletka[1] == j:
                vnutri = True
            znak = pole[kletka[0]][kletka[1]]
            if znak == simvol:
                nashe = nashe + 1
            elif znak != logika.PUSTO:
                chuzhoe = chuzhoe + 1
        if vnutri == True and chuzhoe == 0:
            ocenka = ocenka + (nashe + 1) * (nashe + 1)
    return ocenka


def hod_kompyutera(pole, simvol_bota):
    simvol_igroka = logika.drugoy_simvol(simvol_bota)
    svobodnye = spisok_svobodnyh(pole)
    if len(svobodnye) == 0:
        return None

    for kletka in svobodnye:
        pole[kletka[0]][kletka[1]] = simvol_bota
        rezultat = logika.proverka_pobedy(pole)
        pole[kletka[0]][kletka[1]] = logika.PUSTO
        if rezultat != None:
            return kletka

    for kletka in svobodnye:
        pole[kletka[0]][kletka[1]] = simvol_igroka
        rezultat = logika.proverka_pobedy(pole)
        pole[kletka[0]][kletka[1]] = logika.PUSTO
        if rezultat != None:
            return kletka

    luchshie = []
    luchshaya_ocenka = -1
    for kletka in svobodnye:
        moya = ocenit_kletku(pole, kletka[0], kletka[1], simvol_bota)
        chuzhaya = ocenit_kletku(pole, kletka[0], kletka[1], simvol_igroka)
        itog = moya + chuzhaya
        if itog > luchshaya_ocenka:
            luchshaya_ocenka = itog
            luchshie = [kletka]
        elif itog == luchshaya_ocenka:
            luchshie.append(kletka)

    return random.choice(luchshie)
