import random
import matplotlib.pyplot as plt
import numpy as np

POPULATION_SIZE = 100	# 개체 집단의 크기
MUTATION_RATE = 0.1			# 돌연 변이 확률
SIZE = 8			# 하나의 염색체에서 유전자 개수		

# 염색체를 클래스로 정의한다. 
class Chromosome:
    def __init__(self, g=[]):
        self.genes = g.copy()		# 유전자는 리스트로 구현된다. 
        self.fitness = 0		# 적합도
        if self.genes.__len__()==0:	# 염색체가 초기 상태이면 초기화한다. 
            i = 0
            while i<SIZE:
                self.genes.append(random.randint(0, 7)) 
                i += 1
    
    def cal_fitness(self):		# 적합도를 계산한다. 
        self.fitness = 28
        value = 0
        # 일단 서로 충돌하는 퀸 쌍의 개수를 구한다.
        # chromosome을 설계할 때 같은 열의 collision은 막았으므로 행 충돌, 대각선 충돌만 존재한다.
        
        # 행 충돌 횟수
        horizon_collision = sum([self.genes.count(pos) - 1 for pos in self.genes]) / 2
        # 염색체가 [2 2 3 2 3 2 2 3] 일 때, 첫 pos인 2에 대해서 염색체 리스트에서 2의 개수를 세면 5개, 첫 2의 충돌횟수는 5-1번
        # 두번쩨 pos인 2에 대해서 2의 개수를 세면 역시나 5개, 두번째 2의 충돌 횟수는 5-1번
        # 세번째 pos인 3에 대해서 3의 개수를 세면 3개, 세번째 3의 충돌 횟수는 3-1번
        # 계속해서 충돌 횟수를 구하여 다 더하고, a가 b와 충돌한 것과 b가 a와 충돌한 것을 모두 셌으므로 겹치는 것들을 없애기위해 2로 나눈다.
        
        # 대각선 충돌 횟수
        diagonal_collision = 0
        index = 0
        for pos in range(0,7): # 0~6번 인덱스에 존재하는 각 원소들에 대하여 오른쪽으로 떨어진 원소들과의 대각선 충돌 확인하기 위해
            for j in range(1, 8-pos):  # 각각으로부터 인덱스가 1칸, 2칸, ... , 가장 끝 칸에 떨어져 있는 원소들과 각각 대각선 충돌 일어나는지 확인
                if abs(self.genes[pos] - self.genes[pos + j]) == j: 
                    diagonal_collision += 1
                    # 염색체가 [2 3 2 2 3 2 2 3] 일 때, pos가 0인 경우에 j는 1~7로,
                    # 가로로 1칸 떨어져있는 값들이 세로로도 1만큼 차이나는가? => ([0]에 들어있는 값 - [1]에 들어있는 값) == 1 인지 확인 => abs(2 - 3) == 1 이 맞으므로 대각선 충돌 발생 , 이 때 diagonal_collision 1 증가
                    # 가로로 2칸 떨어져있는 값들이 세로로도 2만큼 차이나는가? => ([0]에 들어있는 값 - [2]에 들어있는 값) == 2 인지 확인 => abs(2 - 2) != 1 이므로 대각선 충돌 발생하지않음
                    # 이와 같은 방식으로 모든 인덱스에 대해 대각선 충돌이 발생하는지 확인하여 총 횟수를 구한다
    
        value = int(horizon_collision + diagonal_collision)
        # 총 충돌 횟수 = 행 충돌 + 대각선 충돌

        self.fitness = self.fitness - value
        # 적합도 => 서로 공격하지 않는 퀸 쌍의 개수 => 28 - 충돌하는 퀸 쌍의 개수
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
    max_value = sum([c.cal_fitness() for c in pop])
    pick = random.uniform(0, max_value) # 2개의 숫자 사이의 랜덤 실수를 리턴한다.
    current = 0
    
    # 룰렛휠에서 어떤 조각에 속하는지를 알아내는 루프
    for c in pop:
        current += c.cal_fitness()
        if current > pick:
            return c

# 교차 연산
# 복수점 교차 crossover 방식 이용
def crossover(pop):
    father = select(pop)
    mother = select(pop)
    index1 = random.randint(1, SIZE - 2) # 첫 번째 교차점 랜덤 선택
    index2 = random.randint(1, SIZE - 2) # 두 번째 교차점 랜덤 선택
    while (index1 == index2): # 두 교차점이 일치하는 경우 다시 선택
        index2 = random.randint(1, SIZE - 2)
        if index1 != index2:
            break

    # 두 교차점을 기준으로 crossover
    if index1 < index2:
        child1 = father.genes[:index1] + mother.genes[index1:index2] + father.genes[index2:]
        child2 = mother.genes[:index1] + father.genes[index1:index2] + mother.genes[index2:]

    elif index1 > index2:
        child1 = father.genes[:index2] + mother.genes[index2:index1] + father.genes[index1:]
        child2 = mother.genes[:index2] + father.genes[index2:index1] + mother.genes[index1:]

    return (child1, child2)
    
# 돌연변이 연산
# make random swap 방식 이용
def mutate(c):
    for i in range(SIZE):
        if random.random() < MUTATION_RATE:
                head = random.randint(0, 7)
                end = random.randint(0, 7)
                tmp = c.genes[head]
                c.genes[head] = c.genes[end]
                c.genes[end] = tmp

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
    count += 1
    if count > 100 : break