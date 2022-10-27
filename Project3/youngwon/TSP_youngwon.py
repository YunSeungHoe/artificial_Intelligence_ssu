import random
import matplotlib.pyplot as plt

POPULATION_SIZE = 6		# 개체 집단의 크기
MUTATION_RATE = 0.1			# 돌연 변이 확률
SIZE = 9			# 하나의 염색체에서 유전자 개수		
DISTANCE = [[0, 30, 140, 75, 168, 237, 303, 325, 268],
            [30, 0, 140, 105, 198, 247, 315, 334, 257],
            [140, 140, 0, 173, 205, 119, 190, 200, 141],
            [75, 105, 173, 0, 102, 238, 293, 323, 313],
            [168, 198, 205, 102, 0, 213, 247, 287, 340],
            [237, 247, 119, 238, 213, 0, 71, 88, 173],
            [303, 315, 190, 293, 247, 71, 0, 44, 222],
            [325, 334, 200, 323, 287, 88, 44, 0, 202],
            [268, 257, 141, 313, 340, 173, 222, 202, 0]]

# 인덱스 0:서울, 1:인천, 2:대전, 3:춘천, 4:강릉, 5:대구, 6:울산, 7:부산, 8:광주

# 염색체를 클래스로 정의한다. 
class Chromosome:
    def __init__(self, g=[]):
        self.genes = g.copy()		# 유전자는 리스트로 구현된다. 
        self.fitness = 0		# 적합도
        if self.genes.__len__()==0:	# 염색체가 초기 상태이면 초기화한다. 
            self.genes.append(0)
            list = [1, 2, 3, 4, 5, 6, 7, 8]
            new_list = random.sample(list,8)   # 모집단 list에서 샘플 8개를 구하여 새로운 리스트 작성
            self.genes += new_list       # 0 뒤에 갖다붙히기

    
    def cal_fitness(self):		# 적합도를 계산한다. 
        self.fitness = 0
        sum_shortest_distance = 0
        for i in range(SIZE-1):
            # 현재 염색체 리스트가 [068743521]이라면
            city1 = self.genes[i]  # i=0일 때, 맨 앞 0번째 인덱스에 해당하는 도시는 self.genes[0] = 0번, 즉 서울이다.
            city2 = self.genes[i+1]  # 1번째 인덱스에 해당하는 도시는 self.genes[1] = 6번, 울산이다.
            sum_shortest_distance += DISTANCE[city1][city2]  # 0과 6, 즉 서울과 울산 사이의 최단 거리를 알아내기위해 DISTANCE 2차원 배열에서 [0][6]에 해당하는 값을 추출한다.
            # 마찬가지로 i=1,2,3,..,7까지 반복하여 1번째 도시와 2번째 도시, 2번째 도시와 3번째 도시,..., 6번째 도시와 7번째 도시 사이의 최단거리까지 구해 모두 더한다.
        sum_shortest_distance += DISTANCE[self.genes[8]][0]  # 마지막 8번째 도시와 최종 목적지 서울 사이의 최단 거리까지 더한다. 
        self.fitness = sum_shortest_distance
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
# 두 교차점을 기준으로 crossover
def crossover(pop):
    father = pop[0]
    mother = pop[1]

    point = [1, 2, 3, 4, 5, 6, 7, 8]
    slicepoint = random.sample(point,2)  # 랜덤하게 교차점 두개 선택
    slicepoint.sort()  # 오름차순
    index1 = slicepoint[0] # 앞 교차점
    index2 = slicepoint[1] # 뒤 교차점


    fathercopy = father.genes.copy()   # father 잠시 복사
    mother_extract = mother.genes[index1:index2]  # mother로부터 두 교차점 사이에 있는 값들 추출
    fathercopy = [x for x in fathercopy if x not in mother_extract]  # 겹칠 수도 있으므로 father에서 mother추출값 삭제

    i=0
    child1 = []
    while (i<index1):
        child1.append(fathercopy[i]) # index1보다 앞의 위치까지, father에 남은 값들을 child1에 순서대로 입력
        i+=1
    del fathercopy[:i]   #child1에 추가한 값들은 father에서 삭제
    child1 += mother_extract #index1에서 index2 사이의 위치에는 mother로부터 추출한 값들 입력
    child1 += fathercopy #나머지 index2 이후에는 father에 남아있는 값들을 입력



    mothercopy = mother.genes[:]
    father_extract = father.genes[index1:index2]
    mothercopy = [x for x in mothercopy if x not in father_extract]

    i=0
    child2 = []
    while (i<index1):
        child2.append(mothercopy[i])
        i+=1
    del mothercopy[:i]
    child2 += father_extract
    child2 += mothercopy


    return (child1, child2)

    
# 돌연변이 연산
# make random swap 방식 이용
def mutate(c):
    for i in range(SIZE):
        if random.random() < MUTATION_RATE:
            city1 = random.randint(1, SIZE-1) #서울 제외 랜덤하게 도시 두개 선택
            city2 = random.randint(1, SIZE-1)
            while (city1 == city2):
                city2 = random.randint(1, SIZE-1)
            tmp = c.genes[city1]
            c.genes[city1] = c.genes[city2]
            c.genes[city2] = tmp    # 도시 두개 상호 교환
            


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
population.sort(key=lambda x: x.cal_fitness())
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

while population[0].cal_fitness() > 1018: # sorting을 하기 때문에 [0]을 비교한다.
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
    population.sort(key=lambda x: x.cal_fitness())
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


###
plt.plot( range(int(len(list_maxfit))), list_maxfit, label= 'max fitness')
plt.plot( range(int(len(list_maxfit))), list_avrgfit, label = 'average fitness')
plt.xlabel('generation')
plt.ylabel('fitness')
plt.legend( loc='best')
plt.grid(True)
plt.show()
###