import random
from deap import creator, base, tools, algorithms
import os
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():
    m = 0.5
    b = 0.25
    # m = random.random()
    # b = random.random()
    # generate parts of y = mx + b
    print("y=" + str(m) + "x+" + str(b))
    testCase = []
    UI = input("Enter own settings (Y/N): ")
    if UI == "Y":
        SampleSize = int(input("Enter sample size: "))
        MutE = float(input("Enter mutation effect greater than 0, less than 1: "))
        MutC = float(input("Enter mutation change greater than 0, less than 1: "))
        GenS = int(input("Enter number of generations to run: "))
        PopS = int(
            input("Enter population size for each of the aforemention generations: ")
        )
    else:
        SampleSize = 100
        MutE = 0.1
        MutC = 0.5
        GenS = 1000
        PopS = 100
    for x in range(SampleSize):
        testCase.append(x * m + b)
    os.system("pause")
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()

    def genRan():
        return random.random()

    toolbox.register("Alpha", genRan)
    toolbox.register(
        "individual", tools.initRepeat, creator.Individual, toolbox.Alpha, n=2
    )
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def eval2(individual):
        predCase = []
        for x in range(SampleSize):
            predCase.append(x * individual[0] + individual[1])
        evalCase = []
        for x in range(SampleSize):
            evalCase.append(abs((testCase[x] - predCase[x]) / testCase[x]))
        return (0 - sum(evalCase),)

    def evalOneMax(individual):
        return sum(individual)

    toolbox.register("evaluate", eval2)
    toolbox.register("mate", tools.cxBlend, alpha=0.05)
    toolbox.register(
        "mutate", tools.mutPolynomialBounded, eta=MutE, low=[0, 0], up=[1, 1], indpb=0.5
    )
    toolbox.register("select", tools.selTournament, tournsize=math.floor(PopS / 2))

    population = toolbox.population(n=PopS)

    bestof = []
    NGEN = GenS
    for gen in range(NGEN):
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=MutC)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        population = toolbox.select(offspring, k=len(population))
        top = tools.selBest(population, k=1)
        bestof.append(top[0] + [gen + 1])
        print(str(gen + 1) + ": " + str(top))

    print("M off by " + str(m - top[0][0]) + " and B off by " + str(b - top[0][1]))
    UbestOf = []
    for i in bestof:
        if len(UbestOf) == 0:
            UbestOf.append(i)
        else:
            isU = True
            for x in UbestOf:
                isU = (x[0] != i[0]) & (x[1] != i[1])
                if isU == False:
                    break
            if isU:
                UbestOf.append(i)
    UbestOf.append(bestof[len(bestof) - 1])

    plotX = list(range(SampleSize))

    def calcY(xList, M, B):
        Y = []
        for i in xList:
            Y.append(i * M + B)
        return Y

    plotY = calcY(plotX, m, b)
    plt.plot(plotX, plotY, label="Actual Line")
    count = 0

    for i in UbestOf:
        count += 1
        if (
            count == 1
            or count == math.floor(0.25 * len(UbestOf))
            or count == math.floor(0.50 * len(UbestOf))
            or count == math.floor(0.75 * len(UbestOf))
            or count == len(UbestOf)
        ):
            plt.plot(
                plotX,
                calcY(plotX, i[0], i[1]),
                label="Best from gen " + str(i[2]),
                linestyle="--",
            )

    plt.title(
        "ML genetic algo attempts at reproducing line y=" + str(m) + "x+" + str(b)
    )
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
