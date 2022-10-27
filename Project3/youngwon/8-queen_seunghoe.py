import random
import matplotlib.pyplot as plt
import numpy as np

POPULATION_SIZE = 6		# 개체 집단의 크기
MUTATION_RATE = 0.1			# 돌연 변이 확률
SIZE = 8				# 하나의 염색체에서 유전자 개수		

# 염색체를 클래스로 정의한다. 
class Chromosome:
    def __init__(self, g=[]):
        self.genes = g.copy()       # genes는 queen들의 위치 
        self.fitness = 28		    # 적합도 28 - h
        if self.genes.__len__()==0:	# 염색체가 초기 상태이면 초기화한다. 
            for i in range(SIZE):
                self.genes.append([i, random.randrange(0, 8)])

    def cal_fitness(self):		# 적합도를 계산한다. 
        self.fitness = 28
        value = 0               # h를 의미
        for j in range(SIZE - 1): #0부터 6까지
            for i in range(j + 1, SIZE): #1부터 7까지
                if self.genes[j][0] == self.genes[i][0]: value += 1
                elif self.genes[j][1] == self.genes[i][1]: value += 1
                elif abs(self.genes[j][0] - self.genes[i][0]) == abs(self.genes[j][1] - self.genes[i][1]):
                    value += 1
        self.fitness = self.fitness - value
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
 
# 교차 연산
def crossover(pop):
    father = pop[0] # pop가 적합도가 높은 순서대로 정렬 되어 들어온다. 
    mother = pop[1] # 0, 1의 위치하는 유전자가 적합도가 높다. 
    index = random.randint(1, SIZE - 2)
    child1 = father.genes[:index] + mother.genes[index:] 
    child2 = mother.genes[:index] + father.genes[index:]
    return (child1, child2)
    
# 돌연변이 연산
def mutate(c):
    for i in range(SIZE):
        if random.random() < MUTATION_RATE:
            c.genes[i] = [i, (c.genes[i][1] + 1)%8]         # + 1 하는 방법
            # c.genes[i] = [i, random.randint(0, SIZE-1)]   # 랜덤하게 하는 방법

# 결과를 출력하는 용도
def print_result(gene):
    plist = []
    for j in range(SIZE):
        for i in range(SIZE):
            if [j, i] == gene[j]: plist.append('Q')
            else: plist.append(' ')
    print("┌───┬───┬───┬───┬───┬───┬───┬───┐")
    for i in range(SIZE):
        print("│ " + str(plist[i*SIZE]) + " │ " + str(plist[i*SIZE+1]) + 
             " │ " + str(plist[i*SIZE+2]) + " │ " + str(plist[i*SIZE+3]) +
             " │ " + str(plist[i*SIZE+4]) + " │ " + str(plist[i*SIZE+5]) +
             " │ " + str(plist[i*SIZE+6]) + " │ " + str(plist[i*SIZE+7]) + " │")
        if i < SIZE-1: print("├───┼───┼───┼───┼───┼───┼───┼───┤")
    print("└───┴───┴───┴───┴───┴───┴───┴───┘")
    
# 메인 프로그램
def main():
    population = []
    i = 0

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
    for i in range(6):
        fit_sum.append(population[i].cal_fitness())
    avrg = sum(fit_sum) / 6
    list_avrgfit.append(avrg)
    ###

    count=1

    while population[0].cal_fitness() != 28:
        new_pop = []

        for i in range(POPULATION_SIZE // 2):
            c1, c2 = crossover(population)
            new_pop.append(Chromosome(c1))
            new_pop.append(Chromosome(c2))
            population[1].fitness = 0
            population[0].fitness = 0
            population.sort(key=lambda x: x.fitness, reverse=True) # 사용한 부모 유전자를 사용하지 않도록 하기위해 수행한다.

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
        for i in range(6):
            fit_sum.append(population[i].cal_fitness())
        avrg = sum(fit_sum) / 6
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

if __name__ == '__main__':
    main()
