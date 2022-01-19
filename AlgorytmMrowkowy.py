import random
import math
import pylab



def wypisywanie(antNum, n, weight, value, sackSize, p, alpha, beta, nc):
    print(f"Ilość mrówek: {antNum}")
    for i in range(n):
        print(f"{i+1}. waga = {weight[i]} ; wartość = {value[i]}")
    print(f"Miejsce w plecaku: {sackSize}")
    print(f"Współczynnik parowania feromonów: {p}")
    print(f"Alpha: {alpha}")
    print(f"Beta: {beta}")
    print(f"Ilość cykli: {nc}")



def wypelnianie_tabel(antNum, Move, tabu, currValue, value, currWeight, sackSize, weight):
    for i in range(antNum):
        Move[i][i] = 1
        tabu[i][i] = 1
        currValue[i] = value[i]
        currWeight[i] = sackSize - weight[i]


def liczenie_prawdopodobienstwa(antNum, n, tabu, t, alpha, beta, mi):
    probability = [[0] * antNum for i in range(n)]
    for i in range(antNum):
        sum = 0
        for j in range(n):
            if tabu[i][j] != 1:
                sum += (t[j] ** alpha) * (mi[j] ** beta)
        for j in range(n):
            if tabu[i][j] == 1:
                probability[i][j] = 0
            else:
                if sum == 0:
                    probability[i][j] = math.inf
                else:
                    probability[i][j] = (t[j] ** alpha) * (mi[j] ** beta) / sum
    return probability


def ruch_mrowek(antNum, n, probability, currWeight, weight, Move, tabu, currValue, value):
    for i in range(antNum):
        for j in range(n):
            rann = random.random() / antNum
            if probability[i][j].real > rann and currWeight[i] >= weight[j]:
                Move[i][j] = 1
                tabu[i][j] = 1
                currWeight[i] -= weight[j]
                currValue[i] += value[j]
                #print(f"{i}. {Move[i]}")


def szukanie_rozwiazania(antNum, currValue):
    bestSolution = 0
    for i in range(antNum):
        if currValue[i] > bestSolution:
            bestSolution = currValue[i]
    return bestSolution


def aktualizacja_feromonu(n, t, p, Dtau):
    for i in range(n):
        t[i] = p * t[i] + Dtau[i]
        Dtau[i] = 0



def algorytm_cykliczny(antNum, n, weight, value, sackSize, p, alpha, beta, nc):
    wypisywanie(antNum, n, weight, value, sackSize, p, alpha, beta, nc)

    #szlaki feromonowane (w celu konstrukcji rozwiązania, mrówka używa wspólnej informacji, która jest tam kodowana)
    t = [0] * n
    #atrakcyjność ruchu (umożliwia lepszy wybór obiektu ze wszystkich dostępnych obiektów które tworzą sąsiedztwa obecnego stanu, a które mogą być dodawane do rozwiązania które jest konstruowane)
    mi = [0] * n
    #ilość feromonów 'rozpylenia', która zależy od jakości tego rozwiązania
    Dtau = [0] * n

    tabu = [[0] * antNum for i in range(n)]
    Move = [[0] * antNum for i in range(n)]
    currWeight = [None] * antNum
    currValue = [None] * antNum

    for i in range(n):
        t[i] = 1
        mi[i] = value[i] / weight[i]

    wypelnianie_tabel(antNum, Move, tabu, currValue, value, currWeight, sackSize, weight)

    while nc > 0:
        probability = liczenie_prawdopodobienstwa(antNum, n, tabu, t, alpha, beta, mi)

        ruch_mrowek(antNum, n, probability, currWeight, weight, Move, tabu, currValue, value)

        bestSolution = szukanie_rozwiazania(antNum, currValue)

        #jakość rozwiązania
        Q = 1
        for i in range(antNum):
            for j in range(n):
                if Move[i][j] == 1:
                    if currWeight[i] == 0:
                        Dtau[j] = math.inf
                    else:
                        Dtau[j] = Q / currWeight[i]
                        Move[i][j] = 0
                        break

        aktualizacja_feromonu(n, t, p, Dtau)

        nc -= 1

    return bestSolution



def algorytm_staly(antNum, n, weight, value, sackSize, p, alpha, beta, nc):
    wypisywanie(antNum, n, weight, value, sackSize, p, alpha, beta, nc)

    #szlaki feromonowane (w celu konstrukcji rozwiązania, mrówka używa wspólnej informacji, która jest tam kodowana)
    t = [0] * n
    #atrakcyjność ruchu (umożliwia lepszy wybór obiektu ze wszystkich dostępnych obiektów które tworzą sąsiedztwa obecnego stanu, a które mogą być dodawane do rozwiązania które jest konstruowane)
    mi = [None] * n
    #ilość feromonów 'rozpylenia', która zależy od jakości tego rozwiązania
    Dtau = [0] * n

    tabu = [[0] * antNum for i in range(n)]
    Move = [[0] * antNum for i in range(n)]
    currWeight = [None] * antNum
    currValue = [None] * antNum

    for i in range(n):
        t[i] = 1
        mi[i] = value[i] / weight[i]

    wypelnianie_tabel(antNum, Move, tabu, currValue, value, currWeight, sackSize, weight)

    probability = liczenie_prawdopodobienstwa(antNum, n, tabu, t, alpha, beta, mi)

    ruch_mrowek(antNum, n, probability, currWeight, weight, Move, tabu, currValue, value)

    bestSolution = szukanie_rozwiazania(antNum, currValue)

    while nc > 0:
        #jakość rozwiązania
        Q = 1
        for i in range(antNum):
            for j in range(n):
                if Move[i][j] == 1:
                    if currWeight[i] == 0:
                        Dtau[j] = math.inf
                    else:
                        Dtau[j] = Q
                        Move[i][j] = 0
                        break

        aktualizacja_feromonu(n, t, p, Dtau)

        nc -= 1

    return bestSolution



def algorytm_sredni(antNum, n, weight, value, sackSize, p, alpha, beta, nc):
    wypisywanie(antNum, n, weight, value, sackSize, p, alpha, beta, nc)

    #szlaki feromonowane (w celu konstrukcji rozwiązania, mrówka używa wspólnej informacji, która jest tam kodowana)
    t = [0] * n
    #atrakcyjność ruchu (umożliwia lepszy wybór obiektu ze wszystkich dostępnych obiektów które tworzą sąsiedztwa obecnego stanu, a które mogą być dodawane do rozwiązania które jest konstruowane)
    mi = [None] * n
    #ilość feromonów 'rozpylenia', która zależy od jakości tego rozwiązania
    Dtau = [0] * n

    tabu = [[0] * antNum for i in range(n)]
    Move = [[0] * antNum for i in range(n)]
    currWeight = [None] * antNum
    currValue = [None] * antNum

    for i in range(n):
        t[i] = 1
        mi[i] = value[i] / weight[i]

    wypelnianie_tabel(antNum, Move, tabu, currValue, value, currWeight, sackSize, weight)

    probability = liczenie_prawdopodobienstwa(antNum, n, tabu, t, alpha, beta, mi)

    ruch_mrowek(antNum, n, probability, currWeight, weight, Move, tabu, currValue, value)

    bestSolution = szukanie_rozwiazania(antNum, currValue)

    while nc > 0:
        #jakość rozwiązania
        Q = 1
        for i in range(antNum):
            for j in range(n):
                if Move[i][j] == 1:
                    if currWeight[i] == 0:
                        Dtau[j] = math.inf
                    else:
                        Dtau[j] = Q / mi[j]
                        Move[i][j] = 0
                        break

        aktualizacja_feromonu(n, t, p, Dtau)

        nc -= 1

    return bestSolution


def wykres_cykle(antNum, n, weight, value, sackSize, alpha, beta, p):
    nc = [10, 20, 30, 40, 50, 60]
    x = nc
    l = len(x)
    y_cyk = []
    y_st = []
    y_sr = []
    for i in range(l):
        y_cyk.append(algorytm_cykliczny(antNum, n, weight, value, sackSize, p, alpha, beta, nc[i]))
        y_st.append(algorytm_staly(antNum, n, weight, value, sackSize, p, alpha, beta, nc[i]))
        y_sr.append(algorytm_sredni(antNum, n, weight, value, sackSize, p, alpha, beta, nc[i]))
    pylab.plot(x, y_cyk, label='cykliczny')
    pylab.plot(x, y_st, label='staly')
    pylab.plot(x, y_sr, label='sredni')
    pylab.ylabel("Najlepsze wyniki")
    pylab.title('Porównanie względem ilości cykli')
    pylab.grid(True)
    pylab.legend(loc='lower right')


def wykres_parowanie_feromonu(antNum, n, weight, value, sackSize, nc, alpha, beta):
    p = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    x = p
    l = len(x)
    y_cyk = []
    y_st = []
    y_sr = []
    for i in range(l):
        y_cyk.append(algorytm_cykliczny(antNum, n, weight, value, sackSize, p[i], alpha, beta, nc))
        y_st.append(algorytm_staly(antNum, n, weight, value, sackSize, p[i], alpha, beta, nc))
        y_sr.append(algorytm_sredni(antNum, n, weight, value, sackSize, p[i], alpha, beta, nc))
    pylab.plot(x, y_cyk, label='cykliczny')
    pylab.plot(x, y_st, label='staly')
    pylab.plot(x, y_sr, label='sredni')
    pylab.ylabel("Najlepsze wyniki")
    pylab.title('Porównanie względem współczynników parowania feromonów')
    pylab.grid(True)
    pylab.legend(loc='lower right')


def wykres_alpha(antNum, n, weight, value, sackSize, nc, beta, p):
    alpha = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    x = alpha
    l = len(x)
    y_cyk = []
    y_st = []
    y_sr = []
    for i in range(l):
        y_cyk.append(algorytm_cykliczny(antNum, n, weight, value, sackSize, p, alpha[i], beta, nc))
        y_st.append(algorytm_staly(antNum, n, weight, value, sackSize, p, alpha[i], beta, nc))
        y_sr.append(algorytm_sredni(antNum, n, weight, value, sackSize, p, alpha[i], beta, nc))
    pylab.plot(x, y_cyk, label='cykliczny')
    pylab.plot(x, y_st, label='staly')
    pylab.plot(x, y_sr, label='sredni')
    pylab.ylabel("Najlepsze wyniki")
    pylab.title('Porównanie względem alphy')
    pylab.grid(True)
    pylab.legend(loc='lower right')


def wykres_beta(antNum, n, weight, value, sackSize, nc, alpha, p):
    beta = [1.2, 2.3, 3.4, 4.5, 5.6, 6.7, 7.8, 8.9, 9.1]
    x = beta
    l = len(x)
    y_cyk = []
    y_st = []
    y_sr = []
    for i in range(l):
        y_cyk.append(algorytm_cykliczny(antNum, n, weight, value, sackSize, p, alpha, beta[i], nc))
        y_st.append(algorytm_staly(antNum, n, weight, value, sackSize, p, alpha, beta[i], nc))
        y_sr.append(algorytm_sredni(antNum, n, weight, value, sackSize, p, alpha, beta[i], nc))
    pylab.plot(x, y_cyk, label='cykliczny')
    pylab.plot(x, y_st, label='staly')
    pylab.plot(x, y_sr, label='sredni')
    pylab.ylabel("Najlepsze wyniki")
    pylab.title('Porównanie względem bety')
    pylab.grid(True)
    pylab.legend(loc='lower right')


def wyswietlenie_wykresow(antNum, n, weight, value, sackSize, p, alpha, beta, nc):
    textstr = f'Ilość mrówek: {antNum}\n' \
              f'Ilość kradzionych rzeczy: {n}\n' \
              f'Wagi: rand(1 - 100)\n' \
              f'Zysk: rand(1 - 100)\n' \
              f'Ilość rzeczy mieszczących\n' \
              f'się w plecaku: {sackSize}\n' \
              f'\n' \
              f'DANE, KTÓRE SIĘ ZMIENIAJĄ\n' \
              f'W ZALEŻNOŚCI OD WYKRESU:\n' \
              f'Współczynnik parowania: {p}\n' \
              f'Alpha: {alpha}\n' \
              f'Beta: {beta}\n' \
              f'Ilość cykli: {nc}'
    pylab.figtext(0.02, 0.5, textstr, fontsize=10)
    pylab.subplot(4, 1, 1)
    wykres_cykle(antNum, n, weight, value, sackSize, alpha, beta, p)
    pylab.subplot(4, 1, 2)
    wykres_parowanie_feromonu(antNum, n, weight, value, sackSize, nc, alpha, beta)
    pylab.subplot(4, 1, 3)
    wykres_alpha(antNum, n, weight, value, sackSize, nc, beta, p)
    pylab.subplot(4, 1, 4)
    wykres_beta(antNum, n, weight, value, sackSize, nc, alpha, p)
    pylab.subplots_adjust(left=0.25,
                          bottom=0.03,
                          right=0.995,
                          top=0.965,
                          wspace=0.4,
                          hspace=0.35)
    pylab.show()









def main():
    # #ilość mrówek
    # antNum = 4
    # n = 4
    # weight = [2, 1, 3, 2]
    # value = [12, 10, 20, 15]
    # sackSize = 5
    # #współczynnik parowania feromonów
    # p = 0.5
    # alpha = 0.7
    # beta = 2.3
    # #ilość cykli
    # nc = 1
    #
    # print("1. algorytm cykliczny\n"
    #       "2. algorytm stały\n"
    #       "3. algorytm średni")
    # alg = int(input("Wybierz rodzaj algorytmu: "))
    # if alg == 1:
    #     wynik = algorytm_cykliczny(antNum, n, weight, value, sackSize, p, alpha, beta, nc)
    # if alg == 2:
    #     wynik = algorytm_staly(antNum, n, weight, value, sackSize, p, alpha, beta, nc)
    # if alg == 3:
    #     wynik = algorytm_sredni(antNum, n, weight, value, sackSize, p, alpha, beta, nc)
    # else:
    #     print("Proszę wybrać liczbę 1, 2, lub 3")
    #
    # print(f"Najlepszy wynik: {wynik}")


    antNum = 100
    n = 100
    weight = []
    for i in range(100):
        weight.append(random.randrange(1, 100))
    value = []
    for i in range(100):
        value.append(random.randrange(1, 10))
    sackSize = 80
    nc = 50
    alpha = 0.7
    beta = 2.3
    p = 0.5

    wyswietlenie_wykresow(antNum, n, weight, value, sackSize, p, alpha, beta, nc)



if __name__ == '__main__':
    main()