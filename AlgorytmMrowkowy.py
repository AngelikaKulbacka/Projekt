import random
import math



def wypisywanie(n, weight, value, sackSize):
    for i in range(n):
        print(f"{i+1}. waga = {weight[i]} ; wartość = {value[i]}")

    print(f"Miejsce w plecaku: {sackSize}")


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
            if probability[i][j] > rann and currWeight[i] >= weight[j]:
                Move[i][j] = 1
                tabu[i][j] = 1
                currWeight[i] -= weight[j]
                currValue[i] += value[j]
                print(f"{i}. {Move[i]}")


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
    wypisywanie(n, weight, value, sackSize)

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



def algorytm_staly(antNum, n, weight, value, sackSize, p, alpha, beta):
    wypisywanie(n, weight, value, sackSize)

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

    return bestSolution



def algorytm_sredni(antNum, n, weight, value, sackSize, p, alpha, beta):
    wypisywanie(n, weight, value, sackSize)

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

    return bestSolution


def main():
    #ilość mrówek
    antNum = 4
    n = 4
    weight = [2, 1, 3, 2]
    value = [12, 10, 20, 15]
    sackSize = 5
    #współczynnik parowania feromonów
    p = 0.5
    alpha = 0.7
    beta = 2.3
    #ilość cykli
    nc = 1

    #wynik = algorytm_cykliczny(antNum, n, weight, value, sackSize, p, alpha, beta, nc)
    #wynik = algorytm_staly(antNum, n, weight, value, sackSize, p, alpha, beta)
    wynik = algorytm_sredni(antNum, n, weight, value, sackSize, p, alpha, beta)
    print(f"Najlepszy wynik: {wynik}")


if __name__ == '__main__':
    main()