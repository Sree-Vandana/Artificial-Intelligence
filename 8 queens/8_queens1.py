"""
Genetic Algorithm to solve 8 Queens problem

tested with:        Initial Population: 10, 100, 500, 1000
                    Iterations: 100, 1000, 10,000

Program Execution:  No Input to the program needed.
                    Values of "Population count" and "Max number of Iterations" are hard coded into program

Modify values:      Can modify the Population in "main" method (line: 226) variable name: 'k = 10'
                    Can modify the max number of Iterations in "geneticAlgorithm" method (line: 176) variable name: "maxIterTime = 1000"
"""
import random
from matplotlib import pyplot as plt

"""
Method to get 2D grid Index Values (Index range [1, 8] both rows and cols)
Input: individual geans
Output: list of tuples
"""
def get2DQueensLocations(individual):
    queens = []
    for i in range(len(individual)):
        queens.append((i+1, int(individual[i])))
    return queens

"""
Attacks calculation functions: 
    1. rowColAttacks:  calculates number of queens attacking horizontally and vertically
    2. diagonalAttack45: number of queens attacking in 45 degree diagonal
    3. diagonalAttack135: number of queens attacking in 135 degree diagonal
Input: 2 queen locations
output: attackSum
"""
def rowColAttacks(q1, q2):
    attackSum = 0
    if q1[0] == q2[0]:                                  # queens in same row
        attackSum = attackSum + 1
    if q1[1] == q2[1]:                                  # queens in same column
        attackSum = attackSum + 1
    if q1[0] == q2[0] and q1[1] == q2[1]:               # queens in same location
        attackSum = attackSum + 1
    return attackSum

def diagonalAttack45(q1, q2):                           # 45 degree diagonal attack
    attackSum = 0
    m = q1[0]
    n = q1[1]
    while((m >= 1 and m <= 8) and (n >= 1 and n <= 8)): # 45 degree diagonal attack UP
        if m != q1[0] and n != q2[0] and m == q2[0] and n == q2[1]:
            attackSum = attackSum + 1
        m = m-1
        n = n+1

    c = q1[0]
    d = q1[1]
    while ((c >= 1 and c <= 8) and (d >= 1 and d <= 8)): # 45 degree diagonal attack DOWN
        if c != q1[0] and d != q2[0] and c == q2[0] and d == q2[1]:
            attackSum = attackSum + 1
        c = c + 1
        d = d - 1

    return attackSum

def diagonalAttack135(q1, q2):                          # 135 degree diagonal attacks
    attackSum = 0
    x = q1[0]
    y = q1[1]
    while ((x >= 1 and x <= 8) and (y >= 1 and y <= 8)): # 128 degree diagonal attacks UP
        if x != q1[0] and y != q1[0] and x == q2[0] and y == q2[1]:
            attackSum = attackSum + 1
        x = x - 1
        y = y - 1

    a = q1[0]
    b = q1[1]
    while ((a >= 1 and a <= 8) and (b >= 1 and b <= 8)): # 128 degree diagonal attacks DOWN
        if a != q1[0] and b != q1[0] and a == q2[0] and b == q2[1]:
            attackSum = attackSum + 1
        a = a + 1
        b = b + 1
    return attackSum

"""
Fitness function === number of non-attacking pairs of queens
Input: population with all states or individuals
Output: list of fitnessValues calculated
"""
def fitnessFunction(population):
    fitnessValues = []
    attackingSum = 0
    for individual in range(len(population)):
        queens = get2DQueensLocations(population[individual])
        for i in range(len(queens)):
            for j in range(i+1, len(queens)):
                attackingSum = attackingSum + rowColAttacks(queens[i], queens[j])
                attackingSum = attackingSum + diagonalAttack45(queens[i], queens[j])
                attackingSum = attackingSum + diagonalAttack135(queens[i], queens[j])
        fitnessValues.append(28-attackingSum)
        attackingSum = 0
    return fitnessValues

"""
Function to randomly select 2 parent index to perform cross over function
"""
def randomSelect(population):
    n = len(population)
    return random.sample(range(0, n), 2)

"""
A function to produce a cross over child to create next generation
"""
def reproduce(population, x, y):
    n = len(population[0])
    c = random.randint(0, n)
    s_1 = population[x][0: c]
    s_2 = population[y][c: n+1]
    return s_1 + s_2

"""
A function to calculate if or not to do mutation to a child generated
{0, 1} within the set of 2 numbers 0 and 1. the probability of selecting any one number randomly is 0.5
if we get 0 --> no mutation
if we get 1 --> do mutation
"""
def smallRandomProbability():
    prob = random.sample(range(0, 2), 1)
    return prob

"""
A function for mutation: change one randomly selected child index value with another randomly selected value
"""
def mutate(child):
    n = len(child)
    randomIndex, randomValue = randomSelect(child)
    digitMap = map(int, child)
    digitList = list(digitMap)
    digitList[randomIndex] = randomValue
    stringInts = [str(int) for int in digitList]
    child = "".join(stringInts)
    return child

"""
If solution is found, print the board of the solution individual
"""
def printBoardValues(board):
    for i in range(8):
        for j in range(8):
            print(board[i][j], end="\t")
        print("\n")

def printBoard(queenLocations):
    board = [['.'] * 8 for i in range(8)]
    # printBoardValues(board)
    point = get2DQueensLocations(queenLocations)
    for i in range(8):
        board[point[i][0]-1][point[i][1]-1] = 'Q'
    printBoardValues(board)


"""
Plot the graph between "Generations" and "Avg fitness values"
"""
def plotGraph(x_values, y_values):
    plt.plot(y_values, x_values)
    plt.xlabel("Generations")
    plt.ylabel("Avg Fitness")
    plt.legend("Genetic Algorithm For 8 Queens")
    plt.show()

"""
Genetic algorithm with all the steps
"""
def genticAlgorithm(population):
    fitnessValues = []                              # [min, max] = [0, 28]
    maxIterTime = 1000
    time = 0
    generationCountList = []
    avgFitnessValues = []
    solutionFound = 0

    while time < maxIterTime:
        fitnessValues = fitnessFunction(population);
        generationCountList.append(time)
        avgFitnessValues.append(sum(fitnessValues)/len(fitnessValues))

        if 28 in fitnessValues:
            print("\n********  Yes Solution found **********\n")
            print("Solution found at Generation = ", time)
            print("Maximum Fitness value in the end = ", max(fitnessValues))
            print("row Locations of Queens = ", population[fitnessValues.index(max(fitnessValues))])
            printBoard(population[fitnessValues.index(max(fitnessValues))])
            solutionFound = 1
            break

        new_population = []
        for i in range(len(population)):
            x, y = randomSelect(population)                         # Selection
            child = reproduce(population, x, y)                     # crossOver
            if(smallRandomProbability()):                           # Mutation
                child = mutate(child)
            new_population.append(child)

        population = new_population
        print("*** Generation: ", time, " ***")
        print("generation population:\n",population)
        print("Maximum fitness: ",max(fitnessValues))
        print("Average fitness: ",avgFitnessValues[time])
        print("Individual with maximum Fitness value: ", population[fitnessValues.index(max(fitnessValues))])
        print("\n")
        time = time + 1


    if solutionFound == 0:
        print("\n******** Solution not found **********\n")
        print("Final Generation = ", time)
        print("Final fitness values during Termination\n", fitnessValues)
        print("Maximum Fitness value in the end = ", max(fitnessValues))
        print("Average fitness in the end = ", avgFitnessValues[time-1])
        print("Individual with maximum Fitness value: ", population[fitnessValues.index(max(fitnessValues))])
        printBoard(population[fitnessValues.index(max(fitnessValues))])

    print("Final Generation:\n", population)
    plotGraph(avgFitnessValues, generationCountList)


if __name__ == '__main__':
    k = 10                                                          # 10, 100, 500, 1000 ( k randomly generated states)
    population = []                                                 # list of entire population
    for i in range(k):                                              # Initialization phase
        pop = ""
        for i in range(8):
            pop = pop + str(random.randint(1, 8))                   # k random states represented using 8 digit string
        population.append(pop)

    print("** Initial Population **\n",population)
    genticAlgorithm(population)

