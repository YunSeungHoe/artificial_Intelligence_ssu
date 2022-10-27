import random
import copy
import matplotlib.pyplot as plt

POPULATION_SIZE = 6		# 개체 집단의 크기
MUTATION_RATE = 0.1			# 돌연 변이 확률
SIZE = 8				# 하나의 염색체에서 유전자 개수		
CITY = ["서울", "인천", "대전", "춘천", "강릉", "대구", "울산", "부산", "광주"]
DISTANCE = [[0,     30,     140,    75,     168,    237,    303,    325,    268],
            [30,    0,      140,    105,    198,    247,    315,    334,    257],
            [140,   140,    0,      173,    205,    119,    190,    200,    141],
            [75,    105,    173,    0,      102,    238,    293,    323,    313],
            [168,   198,    205,    102,    0,      213,    247,    287,    340],
            [237,   247,    119,    238,    213,    0,      71,     88,     173],
            [303,   315,    190,    293,    247,    71,     0,      44,     222],
            [325,   334,    200,    323,    287,    88,     44,     0,      202],
            [268,   257,    141,    313,    340,    173,    222,    202,    0]]
# 서울 -> 인천 -> 대전 -> 광주 -> 부산 -> 울산 -> 대구 -> 강릉 -> 춘천 -> 서울 : 1018
# 서울 -> 춘천 -> 강릉 -> 대구 -> 울산 -> 부산 -> 광주 -> 대전 -> 인천 -> 서울 : 1018
# 0 - 8 까지 치환      
# 염색체를 클래스로 정의한다. 
class Chromosome:
    def __init__(self, g=[]):
        self.genes = []		    # genes에는 도시들의 위치를 가르키는 인덱스 즉 결합 가능한 유전자가 들어간다.  
        self.city = g.copy()    # city에는 도시들어간다.
        self.genestocity = []
        self.fitness = 0		# 적합도
        if self.city.__len__()==0:	# 염색체가 초기 상태이면 초기화한다. 
            self.city = random.sample(CITY[1:], SIZE)
        self.genes_update()
    
    def genes_update(self):
        temp = copy.copy(CITY[1:])
        for j in range(SIZE):
            for i in range(len(temp)):
                if self.city[j] == temp[i]:
                    self.genes.append(i)
                    del temp[i]
                    break
        self.genes_to_city()
        
    def genes_to_city(self):
        self.genestocity = []
        temp = copy.copy(CITY[1:])
        self.genestocity.append('서울')
        for i in self.genes:
            self.genestocity.append(temp[i])
            del temp[i]
        self.genestocity.append('서울')
    
    def cal_fitness(self):		# 적합도를 계산한다. 
        self.fitness = 0;
        value = 0
        for i in range(1, len(self.genestocity)):
            left = CITY.index(self.genestocity[i-1])
            right = CITY.index(self.genestocity[i])
            value += DISTANCE[left][right]
        self.fitness = value
        return self.fitness

    def __str__(self):
        return self.genes.__str__()

# 염색체와 적합도를 출력한다. 
def print_p(pop):
    i = 0
    for x in pop:
        print("염색체 #", i, "=", x, "적합도=", x.cal_fitness())
        print("염색체 #", i, "=", x.genestocity)
        i += 1
    print("")

def crossover(pop):
    father = pop[0]
    mother = pop[1]
    index = random.randint(1, SIZE - 2)
    # print("father.genes = ", father.genes)
    # print("mother.genes = ", mother.genes)
    # print("index", index)
    father.genes, mother.genes = father.genes[:index] + mother.genes[index:], mother.genes[:index] + father.genes[index:] 
    # print("father.genes = ", father.genes)
    # print("mother.genes = ", mother.genes)
    father.genes_to_city()
    mother.genes_to_city()
    # print("father.genes_to_city = ", father.genestocity)
    # print("mother.genes_to_city = ", mother.genestocity)
    child1 = father.genestocity[1:-1] 
    child2 = mother.genestocity[1:-1] 
    # print("child1", child1)
    # print("child2", child2)
    return (child1, child2)

    
# 돌연변이 연산
def mutate(c):
    for i in range(SIZE-1):
        if random.random() < MUTATION_RATE:
            if c.genes[i] < SIZE-i:
                c.genes[i] = random.randint(0, SIZE-i-1)
    
# 메인 프로그램
def main():
    print(CITY)
    population = []
    i = 0
    ###
    list_maxfit = []
    list_avrgfit = []
    ###

    # 초기 염색체를 생성하여 객체 집단에 추가한다. 
    while i < POPULATION_SIZE:
        population.append(Chromosome())
        i += 1

    count=0
    population.sort(key=lambda x: x.cal_fitness(), reverse=False)
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

    while population[0].cal_fitness() > 1018:
        new_pop = []

    #     # 선택과 교차 연산
        for i in range(POPULATION_SIZE // 2):
            c1, c2 = crossover(population)
            new_pop.append(Chromosome(c1))
            new_pop.append(Chromosome(c2))
            population[1].fitness = 5000
            population[0].fitness = 5000
            population.sort(key=lambda x: x.fitness, reverse=False) 

        population = new_pop.copy();    
        
        for c in population: mutate(c)

        population.sort(key=lambda x: x.cal_fitness(), reverse=False)
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
        # if count > 5 : break;

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