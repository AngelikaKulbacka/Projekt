import random
import math


def algorytm(antNum, n, weight, value, p, nc):
    for i in range(n):
        print(f"Wpisz wagę {i+1}. przedmiotu: ")
        weight[i] = float(input())
        print(f"Wpisz wartość {i+1}. przedmiotu: ")
        value[i] = float(input())

    print("Wpisz limit miejsca w plecaku: ")
    sackSize = int(input())

    #szlaki feromonowane (w celu konstrukcji rozwiązania, mrówka używa wspólnej informacji, która jest tam kodowana)
    t = [0] * n
    #atrakcyjność ruchu (umożliwia lepszy wybór obiektu ze wszystkich dostępnych obiektów które tworzą sąsiedztwa obecnego stanu, a które mogą być dodawane do rozwiązania które jest konstruowane)
    mi = [None] * n
    #ilość feromonów 'rozpylenia', która zależy od jakości tego rozwiązania
    Dtau = [0] * n
    alpha = 0.7
    beta = 2.3

    for i in range(n):
        t[i] = 1
        mi[i] = value[i] / weight[i]

    tabu = [[0] * antNum for i in range(n)]
    Move = [[0] * antNum for i in range(n)]
    #obliczane prawdopodobieństwo
    probability = [[0] * antNum for i in range(n)]
    currWeight = [None] * antNum
    currValue = [None] * antNum
    bestSolution = 0

    for i in range(antNum):
        Move[i][i] = 1
        tabu[i][i] = 1
        currValue[i] = value[i]
        currWeight[i] = sackSize - weight[i]

    while nc > 0:
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

        for i in range(antNum):
            for j in range(n):
                rann = random.random() / antNum
                if probability[i][j] > rann and currWeight[i] >= weight[j]:
                    Move[i][j] = 1
                    tabu[i][j] = 1
                    currWeight[i] -= weight[j]
                    currValue[i] += value[j]
                    print(f"{i}. {Move[i]}")

        for i in range(antNum):
            if currValue[i] > bestSolution:
                bestSolution = currValue[i]

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

        for i in range(n):
            t[i] = p * t[i] + Dtau[i]
            Dtau[i] = 0

        nc -= 1

    return bestSolution


def main():
    #ilość mrówek
    antNum = 4
    print("Ilość dostępnych przedmiotów: ")
    n = int(input())
    weight = [None] * n
    value = [None] * n
    #współczynnik parowania feromonów
    p = 0.5
    #ilość cykli
    nc = 1

    wynik = algorytm(antNum, n, weight, value, p, nc)
    print(wynik)


if __name__ == '__main__':
    main()