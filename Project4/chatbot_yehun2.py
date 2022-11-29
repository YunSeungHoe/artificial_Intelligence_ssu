import pandas as pd
import re, time

WORD_COL = 0
RULE_COL = 1
RESP_COL = 2
RECIPE_START_ROW = 0
RECIPE_END_ROW = 13

INGREDIENT_START_ROW = 13
INGREDIENT_END_ROW = 44

TYPE_START_ROW = 44
TYPE_END_ROW = 45

def rule_check(com, rule):
    for word in rule:
        for j in range(len(word)):
            for i in range(j, len(com), len(word)):
                command_split = "".join(com[i:i+len(word)])
                if word == command_split:
                    # print("command = {}, rule = {}".format(command_split, word))
                    return True
    return False

def keyword_check1(df, com, start_len, end_len): ### 동일한 이름이 들어간 음식을 구분하도록 ex)김치찌개, 참치 김치찌개
    matched_len = 0
    for i in range(start_len, end_len):
        compare_word = df.values[i][WORD_COL]
        search = re.search(compare_word, "".join(com))
        if search != None:
            span = search.span()
            if matched_len < span[1] - span[0]:
                matched_len = span[1] - span[0]
                respon = df.values[i][RESP_COL]
    if respon:
        return True, respon
    else:
        return False, None


def keyword_check2(df, com, start_len, end_len):
    recommend = []
    for i in range(start_len, end_len):
        compare_word = df.values[i][WORD_COL]    #김치, 닭, 달걀 ...
        print("".join(com))
        print(compare_word)
        if "".join(com) in compare_word != None:
            ingredient = df.values[i][WORD_COL]  ##사용자가 원하는 재료 ex)김치
            for j in range(RECIPE_START_ROW, RECIPE_END_ROW):   #다시 맨위부터 모든 음식이 비교대상이 되어 김치가 들어가는 음식 찾기
                compare_food = df.values[j][WORD_COL] 
                if re.search(ingredient, compare_food) != None:   ##김치 글자가 들어가는 음식 있으면 리스트에 추가
                    recommend.append(compare_food)
                if len(recommend) >= 10:
                    break
            return True, recommend
    return False, None

def keyword_check3(df, com, start_len, end_len):
    recommend = []
    for i in range(start_len, end_len):
        compare_word = df.values[i][WORD_COL]
        print("".join(com))
        if re.search(compare_word, "".join(com)) != None:
            food_type = df.values[i][WORD_COL]  ##사용자가 원하는 종류 ex) 탕, 찌개
            for j in range(RECIPE_START_ROW, RECIPE_END_ROW):   #다시 맨위부터 모든 음식이 비교대상이 되어 '탕'이 들어가는 음식
                compare_food = df.values[j][WORD_COL] 
                if re.search(food_type, compare_food) != None:   ##'탕' 글자가 들어가는 음식 있으면 리스트에 추가
                    recommend.append(compare_food)
                if len(recommend) >= 10:
                    break
            return True, recommend
    return False, None

# pandas 엑셀의 값을 넣으면 df에 저장됨.
df = pd.read_excel("stew.xlsx")
##################################################
# 룰을 리스트에 저장 
# 지금은 레시피와 관련된 룰만 하지만 
# 추후, 확장의 가능성을 남겨둠
##################################################
recipe_rule1 = list(df.values[RECIPE_START_ROW][RULE_COL].split())
recipe_rule2 = list(df.values[INGREDIENT_START_ROW][RULE_COL].split())
recipe_rule3 = list(df.values[TYPE_START_ROW][RULE_COL].split())
##################################################
# 입력을 받아 공백을 제거 
# 한글을 처리하기 위해서는 공백을 제거할 필요가 있음
##################################################
# command = list("당근전 요리 하는방법 알려줘".split())
# command = list("세상에서 제일 맛있는 당근전 요리 하는방법 알려줘".split())
while(True): ### 종료 전까지 무한 반복
    print("챗봇: 무엇을 알려드릴까요?")
    command = list(input("나: ").split())
    if "종료" in command: ### 종료 조건
        print("이용해 주셔서 감사합니다!")
        break 
    command_non_space = list("".join(command))
    #print(command_non_space)
    row_len = df.count()[0] # 행의 갯수 출력
    print("챗봇: ", end="")
    if rule_check(command_non_space, recipe_rule1):
        # 처음부터 음식단어가 들어가는 경우
        # 중간에 움식단어가 들어가는 경우
        keyword_flag, response = keyword_check1(df, command_non_space, RECIPE_START_ROW, RECIPE_END_ROW)
        if keyword_flag:
            print(response+"\n")
        else: ### 일치하는 요리가 없을 때
            print("아직 해당 요리의 레시피는 없네요\n")

    elif rule_check(command_non_space, recipe_rule2):
        keyword_flag, response = keyword_check2(df, command_non_space, INGREDIENT_START_ROW, INGREDIENT_END_ROW)
        if keyword_flag:
            print(", ".join(response), "어떤가요? \n")
        else: ### 일치하는 요리가 없을 때
            print("해당 재료로 만들 수 있는 음식이 없네요\n")
            
    
    elif rule_check(command_non_space, recipe_rule3):
        keyword_flag, response = keyword_check3(df, command_non_space, TYPE_START_ROW, TYPE_END_ROW)
        if keyword_flag:
            print(", ".join(response), "어떤가요? \n")
        else: ### 일치하는 요리가 없을 때
            print("해당 종류의 음식은 아직 없네요\n")
        
    else: 
        # 일치하는 규칙이 없을 때!
        print("아직은 해당 기능이 없네요\n")