import random

POPULATION_SIZE = 5		# 개체 집단의 크기
MUTATION_RATE = 0.1			# 돌연 변이 확률
SIZE = 5				# 하나의 염색체에서 유전자 개수		

# 염색체를 클래스로 정의한다. 
class Chromosome:
    def __init__(self, g=[]):
        self.genes = g.copy()		# 유전자는 리스트로 구현된다. 
        self.fitness = 0		# 적합도
        if self.genes.__len__()==0:	# 염색체가 초기 상태이면 초기화한다. 
            i = 0
            while i<SIZE:
                if random.random() >= 0.5: self.genes.append(1)
                else: self.genes.append(0)
                i += 1
    
    def cal_fitness(self):		# 적합도를 계산한다. 
        self.fitness = 0
        value = 0
        for i in range(SIZE):
            value += self.genes[i]*pow(2,SIZE-1-i)
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

# 선택 연산
def select(pop):
    max_value  = sum([c.cal_fitness() for c in population])
    pick    = random.uniform(0, max_value) # 2개의 숫자 사이의 랜덤 실수를 리턴한다.
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
    index = random.randint(1, SIZE - 2) # 2개의 숫자 사이의 랜덤 정수를 리턴한다.
    child1 = father.genes[:index] + mother.genes[index:] 
    child2 = mother.genes[:index] + father.genes[index:] 
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
population = []
i=0

# 초기 염색체를 생성하여 객체 집단에 추가한다. 
while i<POPULATION_SIZE:
    population.append(Chromosome())
    i += 1

count=0
population.sort(key=lambda x: x.cal_fitness(), reverse=True)
print("세대 번호=", count)
print_p(population)
count=1

while population[0].cal_fitness() < 31: # sorting을 하기 때문에 [0]을 비교한다.
    new_pop = []

    # 선택과 교차 연산
    for _ in range(POPULATION_SIZE//2):
        c1, c2 = crossover(population);
        new_pop.append(Chromosome(c1));
        new_pop.append(Chromosome(c2));

    # 자식 세대가 부모 세대를 대체한다. 
    # 깊은 복사를 수행한다. 
    population = new_pop.copy();    
    
    # 돌연변이 연산
    for c in population: mutate(c)

    # 출력을 위한 정렬
    population.sort(key=lambda x: x.cal_fitness(), reverse=True)
    print("세대 번호=", count)
    print_p(population)
    count += 1
    if count > 100 : break;