# 8x8 체스판에 8개의 퀸을 서로 잡아먹지 못하는 위치에 놓는다.
# 하나의 퀸을 기준으로 가로, 세로, 대각선에 다른 퀸이 존재하면 안된다.
import random
import matplotlib.pyplot as plt
import numpy as np

POPULATION_SIZE = 10
MUTATION_RATE = 0.1
SIZE = 8 # 하나의 염색체에서 유전자의 개수

class Chromosome:
    # 각 퀸은 각 열에 하나만 존재한다는 가정하에 각 열에서의 행 인덱스를 유전자로 가진다.
    def __init__(self, g=[]):
        self.genes = g.copy() # 유전자는 리스트로 구현된다. 
        self.fitness = 0 # 적합도
        if self.genes.__len__() == 0: # 염색체가 초기 상태이면 초기화한다. 
            i = 0
            while i < SIZE:
                self.genes.append(random.randint(0, SIZE-1)) # 퀸이 존재할 행 인덱스(0 ~ SIZE-1)중 하나를 리턴한다. 
                i += 1
    
    def cal_fitness(self): # 적합도 계산 함수 (서로 공격하지 않는 쌍이 많을수록 적합도가 높다.)
        # 첫 번째 퀸(첫 번째 열)부터 시작해 모든 오른쪽에 있는 퀸과 공격이 가능한지 판단한다.
        # 현재 퀸의 행 인덱스가 k일 때 오른쪽으로 n번째에 있는 열에서 퀸이 k, k+n, k-n 행 인덱스에 존재하면 공격 가능하다.
        self.fitness = 0
        value = 28 # 모든 퀸들이 서로 공격하지 않을 때 쌍의 개수
        h = 0 # 서로 공격 가능한 퀸 쌍의 개수 
        for i in range(SIZE-1): # i는 현재 기준이 되는 퀸의 열
            for j in range(i+1, SIZE):
                n = j - i # 기준 퀸으로부터 몇 열 떨어져 있는가
                if (self.genes[j] == self.genes[i]) or (self.genes[j] == self.genes[i]+n) or (self.genes[j] == self.genes[i]-n):
                    h += 1
        value -= h
        self.fitness = value 
        return self.fitness
    
    def __str__(self):
        return self.genes.__str__()
    
# 염색체와 적합도를 출력한다. 
def print_p(pop):
    i = 0
    for x in pop:
        print("염색체 #", i, "=", x, "적합도=", x.cal_fitness())
        i += 1
    print("")
    
def select(pop):
    max_value = sum([c.cal_fitness() for c in pop]) # 전체 개체의 적합도의 합
    pick = random.uniform(0, max_value) # 0~max_value 사이의 랜덤 실수를 리턴한다.
    current = 0
    
    # 룰렛휠에서 어떤 조각에 속하는지를 알아내는 루프
    for c in pop:
        current += c.cal_fitness()
        if current > pick:
            return c

# 교차 연산
def crossover(pop):
    father = select(pop)
    mother = select(pop)
    index = random.randint(1, SIZE-2) # 교차 지점 선택
    child1 = father.genes[:index] + mother.genes[index:]
    child2 = mother.genes[:index] + father.genes[index:]
    return (child1, child2)

# 돌연변이 연산
def mutate(c):
    for i in range(SIZE):
        if random.random() < MUTATION_RATE:
            c.genes[i] = random.randint(0, SIZE-1)
            
# 결과를 출력하는 용도
def print_result(gene):
    plist = [[' ' for i in range(SIZE)] for j in range(SIZE)]
    for j in range(SIZE):
        for i in range(SIZE):
            if i == gene[j]: plist[i][j] = 'Q'
            else: plist[i][j] = ' '
    print("┌───┬───┬───┬───┬───┬───┬───┬───┐")
    for i in range(SIZE):
        print("│ " + str(plist[i][0]) + " │ " + str(plist[i][1]) + 
             " │ " + str(plist[i][2]) + " │ " + str(plist[i][3]) +
             " │ " + str(plist[i][4]) + " │ " + str(plist[i][5]) +
             " │ " + str(plist[i][6]) + " │ " + str(plist[i][7]) + " │")
        if i < SIZE-1: print("├───┼───┼───┼───┼───┼───┼───┼───┤")
    print("└───┴───┴───┴───┴───┴───┴───┴───┘")       
    
# 메인 프로그램
population = []
i=0

###
list_maxfit = []
list_avrgfit = []
###


# 초기 염색체를 생성하여 객체 집단에 추가한다. 
while i<POPULATION_SIZE:
    population.append(Chromosome())
    i += 1

count=0
population.sort(key=lambda x: x.cal_fitness(), reverse=True)
print("세대 번호=", count)
print_p(population)

###
list_maxfit.append(population[0].cal_fitness())
fit_sum = []
for i in range(10):
    fit_sum.append(population[i].cal_fitness())
avrg = sum(fit_sum) / 10
list_avrgfit.append(avrg)
###

count=1

while population[0].cal_fitness() != 28: # sorting을 하기 때문에 [0]을 비교한다.
    new_pop = []

    # 선택과 교차 연산
    for _ in range(POPULATION_SIZE//2):
        c1, c2 = crossover(population)
        new_pop.append(Chromosome(c1))
        new_pop.append(Chromosome(c2))

    # 자식 세대가 부모 세대를 대체한다. 
    # 깊은 복사를 수행한다. 
    population = new_pop.copy();    
    
    # 돌연변이 연산
    for c in population: mutate(c)

    # 출력을 위한 정렬
    population.sort(key=lambda x: x.cal_fitness(), reverse=True)
    print("세대 번호=", count)
    print_p(population)


    ###
    list_maxfit.append(population[0].cal_fitness())
    fit_sum = []
    for i in range(10):
        fit_sum.append(population[i].cal_fitness())
    avrg = sum(fit_sum) / 10
    list_avrgfit.append(avrg)
    ###

    count += 1
    
print_result(population[0].genes)

###
plt.plot( range(int(len(list_maxfit))), list_maxfit, label= 'max fitness')
plt.plot( range(int(len(list_maxfit))), list_avrgfit, label = 'average fitness')
plt.xlabel('generation')
plt.ylabel('fitness')
plt.legend( loc='best')
plt.grid(True)
plt.show()
###