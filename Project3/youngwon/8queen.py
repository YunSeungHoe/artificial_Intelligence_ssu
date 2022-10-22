import matplotlib.pyplot as plt
import numpy as np
import random



#처음 100개 chromosome
def make_unit_chromosome():
    return [random.randint(1, 8) for _ in range(8)]


def initialization():
    print("1.INITIALIZATION\n")
    first_100 = [make_unit_chromosome() for _ in range(100)]
    print("top 10 in first 100:\n")
    for u in range(0, 10):
        print("       {}".format(first_100[u]))
    print()
    return first_100


# 적합도함수 구현
def notcollision_check(unit):
    horizon_collision = sum([unit.count(pos) - 1 for pos in unit]) / 2
    diagonal_collision = 0

    index = 0
    for pos in range(0, 7):
        for j in range(1, 8-pos):
            if abs(unit[pos] - unit[pos + j]) == j: 
                diagonal_collision += 1
    collision = int(horizon_collision + diagonal_collision)
    return 28-collision


def fitness_evaluation(chromosome_list):
    print("Fitness evaluation\n")

    for unit in chromosome_list:  # 결과값 print
        print("unit : {},  collision : {}"
              .format(str(unit), str(notcollision_check(unit))))

    selected = []
    chromosome_list.sort(key=lambda x: notcollision_check(x), reverse=True)

    print()
    print("selection\n")
    print("top 10:")
    for i in range(0, 10):  # 상위 10개값 저장
        selected.append(chromosome_list[i])
        print("unit : {},  collision : {}"
              .format(str(selected[i]), str(notcollision_check(selected[i]))))
    print()
    return selected


# Cross-over
def cross_over(ranked_list):  # 원래 입력받은 10개 + cross over 한 10개를 반환한다.

    cross_over_list = []
    for i in range(0, 5):
        cross_up = []
        cross_down = []
        key_list_up = ranked_list[i*2]
        key_list_down = ranked_list[i*2+1]

        for j in range(0, 4):
            cross_up.append(key_list_up[j])
            cross_down.append(key_list_down[j])

        for k in range(4, 8):
            cross_down.append(key_list_up[k])
            cross_up.append(key_list_down[k])

        cross_over_list.append(cross_up)
        cross_over_list.append(cross_down)

    print("cross-over\n")
    print("cross-over:")
    for i in range(0, 10):  # 상위 10개값 저장
        print("unit : {},  collision : {}"
              .format(str(cross_over_list[i]), str(notcollision_check(cross_over_list[i]))))
    print()

    print("original:")
    for i in range(0, 10):  # 상위 10개값 저장
        print("unit : {},  collision : {}"
              .format(str(ranked_list[i]), str(notcollision_check(ranked_list[i]))))
        cross_over_list.append(ranked_list[i])
    print()

    print("total:")
    for i in range(0, 20):  
        print("unit : {},  collision : {}"
              .format(str(cross_over_list[i]), str(notcollision_check(cross_over_list[i]))))
    print()

    return cross_over_list


# Mutation
def make_random_swap(input_list):
    key_head = random.randint(0, 7)
    key_end = random.randint(0, 7)
    tmp = input_list[key_head]
    input_list[key_head] = input_list[key_end]
    input_list[key_end] = tmp

    return input_list


def mutation(un_mutated_list):
    key_value = random.randint(1, 100)
    which_chromosome = random.randint(0, 19)

    if (key_value % 2) == 0:  # 50%의 확률로
        make_random_swap(un_mutated_list[which_chromosome])
        print("mutation!")

    print()
    return un_mutated_list


# Update Generation
def update_generation(to_be_mutation_list):

    print("cross-over + update generation\n")
    total_list = []
    for i in range(0, 8):
        tmp_list = mutation(to_be_mutation_list)
        for j in range(0, 20):
            total_list.append(tmp_list[j])

    print("total list:")
    for i in range(0, 100):  
            print("unit : {},  collision : {}"
                  .format(str(total_list[i]), str(notcollision_check(total_list[i]))))

    print()
    return total_list



def change_into_array(list_form):

    array_form = []
    pos_1 = [1, 0, 0, 0, 0, 0, 0, 0]
    pos_2 = [0, 1, 0, 0, 0, 0, 0, 0]
    pos_3 = [0, 0, 1, 0, 0, 0, 0, 0]
    pos_4 = [0, 0, 0, 1, 0, 0, 0, 0]
    pos_5 = [0, 0, 0, 0, 1, 0, 0, 0]
    pos_6 = [0, 0, 0, 0, 0, 1, 0, 0]
    pos_7 = [0, 0, 0, 0, 0, 0, 1, 0]
    pos_8 = [0, 0, 0, 0, 0, 0, 0, 1]

    for i in range(0, 8):
        if list_form[i] == 1:
            array_form.append(pos_1)
        elif list_form[i] == 2:
            array_form.append(pos_2)
        elif list_form[i] == 3:
            array_form.append(pos_3)
        elif list_form[i] == 4:
            array_form.append(pos_4)
        elif list_form[i] == 5:
            array_form.append(pos_5)
        elif list_form[i] == 6:
            array_form.append(pos_6)
        elif list_form[i] == 7:
            array_form.append(pos_7)
        elif list_form[i] == 8:
            array_form.append(pos_8)

    return np.array(array_form)


if __name__ == "__main__":

    population = initialization()

    total_answer_list = []
    answer_list = []
    check_collision = 1

    # while len(total_answer_list) < 10: # 10개의 답안을 전부 찾고자 하는 경우

    generation_no = 1
    while len(total_answer_list) < 1:  # 1개만 찾는 경우
        print(" generation {} \n".format(generation_no))
        selected_list = fitness_evaluation(population)
        crossed_list = cross_over(selected_list)
        new_population = update_generation(crossed_list)
        new_population.sort(key=lambda x: notcollision_check(x), reverse=True)
        generation_no += 1
        answer_list = new_population[0]

        check_collision = notcollision_check(new_population[0])
        if answer_list not in total_answer_list:
            if check_collision == 28:
                total_answer_list.append(answer_list)

        print("best chromosome : {}".format(answer_list))
        print("present generation no : {}".format(generation_no))
        print()

    print("total answer list ")
    for answer in total_answer_list:
        print(answer) 

    answer_array = change_into_array(total_answer_list[0])

    print(answer_array)
   