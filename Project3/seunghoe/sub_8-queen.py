import random

POPULATION_SIZE = 5		# 개체 집단의 크기
MUTATION_RATE = 0.1			# 돌연 변이 확률
SIZE = 8				# 하나의 염색체에서 유전자 개수		

# 염색체를 클래스로 정의한다. 
class Chromosome:
    def __init__(self, g=[]):
        self.genes = g.copy()       # genes는 queen들간의 상대 위치 
        self.mat = g.copy()         # mat은 queen들의 실제 위치
        self.fitness = 28		    # 적합도 28 - h
        if self.genes.__len__()==0:	# 염색체가 초기 상태이면 초기화한다. 
            for i in range(SIZE):
                row = random.randrange(0, 8)
                col = random.randrange(0, 8)
                while row == 0 and col == 0:
                    row = random.randrange(0, 8)
                    col = random.randrange(0, 8)
                self.genes.append([row, col])
        self.mat_update()
            
    def mat_update(self):
        self.mat.append([self.genes[0][0], self.genes[0][1]])
        for i in range(SIZE):
            if i != 0: self.mat.append([self.genes[i][0] + self.mat[i-1][0], 
                                        self.genes[i][1] + self.mat[i-1][1]])
            self.mat[i][0] = self.mat[i][0] % 8 
            self.mat[i][1] = self.mat[i][1] % 8 
        

    def cal_fitness(self):		# 적합도를 계산한다. 
        self.mat_update()
        self.fitness = 28;
        value = 0               # h를 의미
        for j in range(SIZE - 1): #0부터 6까지
            for i in range(j + 1, SIZE): #1부터 7까지
                if self.mat[j][0] == self.mat[i][0]: value += 1
                elif self.mat[j][1] == self.mat[i][1]: value += 1
                elif abs(self.mat[j][0] - self.mat[i][0]) == abs(self.mat[j][1] - self.mat[i][1]):
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

# 선택 연산
# def select(pop):
#     # max_value  = sum([c.cal_fitness() for c in pop])
#     # pick    = random.randint(max_value//2, max_value)
#     # current = 0
#     # # 룰렛휠에서 어떤 조각에 속하는지를 알아내는 루프
    
#     for c in pop:
#         print(c.cal_fitness())
#     #     current = 0
#     #     current += c.cal_fitness()
#     #     if current > pick:
#         return c
 
# 교차 연산
def crossover(pop):
    father = pop[0]
    mother = pop[1]
    index = random.randint(1, SIZE - 2)
    # print(index)
    # print(father.genes[:index] )
    child1 = father.genes[:index] + mother.genes[index:] 
    child2 = mother.genes[:index] + father.genes[index:]
    # child1.mat_update() 
    # child2.mat_update() 
    return (child1, child2)
    
# 돌연변이 연산
def mutate(c):
    for i in range(SIZE):
        if random.random() < MUTATION_RATE:
            if random.random() < 0.5:
                c.genes[i] = 1
            else:
                c.genes[i] = 0

# 메인 프로그램

def main():
    population = []
    i = 0

    # 초기 염색체를 생성하여 객체 집단에 추가한다. 
    while i<POPULATION_SIZE:
        population.append(Chromosome())
        i += 1

    count=0
    population.sort(key=lambda x: x.cal_fitness(), reverse=True)
    print("세대 번호=", count)
    print_p(population)
    count=1

    while population[0].cal_fitness() != 28:
        new_pop = []

    #     # 선택과 교차 연산
        # for _ in range(POPULATION_SIZE//2):
        c1, c2 = crossover(population);
        new_pop.append(Chromosome(c1));
        new_pop.append(Chromosome(c2));
        new_pop.append(Chromosome())
        new_pop.append(Chromosome())
        # 자식 세대가 부모 세대를 대체한다. 
        # 깊은 복사를 수행한다. 
        population = new_pop.copy();    
        
    # #     # 돌연변이 연산
    #     # for c in population: mutate(c)population
        
        # 출력을 위한 정렬
        population.sort(key=lambda x: x.cal_fitness(), reverse=True)
        print("세대 번호=", count)
        print_p(population)
        count += 1
        if count > 10000 : break;

if __name__ == '__main__':
    main()
