import random

POPULATION_SIZE = 10
MUTATION_RATE = 0.1
SIZE = 9 # 하나의 염색체에서 유전자의 개수
# 0: 서울, 1: 인천, 2: 대전, 3: 춘천, 4: 강릉, 5: 대구, 6: 울산, 7: 부산, 8: 광주
DISTANCE = [
    [0, 30, 140, 75, 168, 237, 303, 325, 268],
    [30, 0, 140, 105, 198, 247, 315, 334, 257],
    [140, 140, 0, 173, 205, 119, 190, 200, 141],
    [75, 105, 173, 0, 102, 238, 293, 323, 313],
    [168, 198, 205, 102, 0, 213, 247, 287, 340],
    [237, 247, 119, 238, 213, 0, 71, 88, 173],
    [303, 315, 190, 293, 247, 71, 0, 44, 222],
    [325, 334, 200, 323, 287, 88, 44, 0, 202],
    [268, 257, 141, 313, 340, 173, 222, 202, 0]
]

class Chromosome:
    def __init__(self, g=[]):
        self.genes = g.copy() # 유전자는 리스트로 구현된다. 
        self.fitness = 0 # 적합도
        if self.genes.__len__() == 0: # 염색체가 초기 상태이면 초기화한다. 
            i = 0
            self.genes.append(0)
            while i < SIZE-1: # 서울은 제외
                num = random.randint(1, SIZE-1)
                while num in self.genes: # 겹치는 도시가 있으면 다시 뽑는다.
                    num = random.randint(1, SIZE-1)
                self.genes.append(num)
                i += 1
    
    def cal_fitness(self, ): # 적합도 계산 함수 (적합도는 ㅇㄹ)
        self.fitness = 0
        d = DISTANCE[0][self.genes[1]] # 서울~첫 도시 거리를 더한다.
        for idx in range(1, SIZE-1):
            d += DISTANCE[self.genes[idx]][self.genes[idx+1]] # 서울을 제외한 각 도시 사이의 거리를 더한다.
        d += DISTANCE[self.genes[-1]][0] # 마지막 도시~서울 거리를 더한다.
        self.fitness = d
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

# 중복을 피하는 교차 연산
def crossover(pop):
    father = select(pop)
    mother = select(pop)
    index = random.randint(1, SIZE-2) # 교차 지점 선택
    temp = father.genes.copy() # father 염색체를 복사해 교차로 받아온 유전자를 삭제한다.
    for i in mother.genes[index:]: 
        temp.remove(i)
    child1 = temp + mother.genes[index:] # father 염색체 중 남은 유전자를 교차로 받아온 유전자와 합친다.
    temp = mother.genes.copy() # mother 염색체를 복사해 교차로 받아온 유전자를 삭제한다.
    for i in father.genes[index:]:
        temp.remove(i)
    child2 = temp + father.genes[index:] # mother 염색체 중 남은 유전자를 교차로 받아온 유전자와 합친다.
    return (child1, child2)

# 상호 교환 돌연변이 연산 
def mutate(c):
    for i in range(1, SIZE):
        if random.random() < MUTATION_RATE:
            g = random.randint(1, SIZE-1) # 서울을 제외한 도시 하나를 선택한다.
            while g == i:
                g = random.randint(1, SIZE-1)
            c.genes[i], c.genes[g] = c.genes[g], c.genes[i] # 두 유전자를 상호 교환한다. 
            
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

while population[0].cal_fitness()  : # sorting을 하기 때문에 [0]을 비교한다.
    new_pop = []

    # 선택과 교차 연산
    for _ in range(POPULATION_SIZE//2):
        c1, c2 = crossover(population)
        new_pop.append(Chromosome(c1))
        new_pop.append(Chromosome(c2))

    # 자식 세대가 부모 세대를 대체한다. 
    # 깊은 복사를 수행한다.
    min_fitness = population[0].cal_fitness()
    population = new_pop.copy();    
    
    # 돌연변이 연산
    for c in population: mutate(c)

    # 출력을 위한 정렬
    population.sort(key=lambda x: x.cal_fitness()) 
    print("세대 번호=", count)
    print_p(population)
    count += 1
    if count > 100 : break