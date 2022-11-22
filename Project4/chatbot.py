import pandas as pd
import re, time

WORD_COL = 0
RULE_COL = 1
RESP_COL = 2
RECIPE_START_ROW = 1 
RECIPE_END_ROW = 12


def rule_check(com, rule):
    for word in rule:
        for j in range(len(word)):
            for i in range(j, len(com), len(word)):
                command_split = "".join(com[i:i+len(word)])
                if word == command_split:
                    # print("command = {}, rule = {}".format(command_split, word))
                    return True
    return False

def keyword_check(df, com, start_len, end_len):
    for i in range(start_len, end_len):
        compare_word = df.values[i][WORD_COL]
        if re.search(compare_word, "".join(com)) != None:
            return True, df.values[i][RESP_COL]
    return False, None

# pandas 엑셀의 값을 넣으면 df에 저장됨.
df = pd.read_excel("stew.xlsx")

##################################################
# 룰을 리스트에 저장 
# 지금은 레시피와 관련된 룰만 하지만 
# 추후, 확장의 가능성을 남겨둠
##################################################
recipe_rule = list(df.values[RECIPE_START_ROW][RULE_COL].split())
recipe_rule1 = list(df.values[13][RULE_COL].split())
print(recipe_rule1)
##################################################
# 입력을 받아 공백을 제거 
# 한글을 처리하기 위해서는 공백을 제거할 필요가 있음
##################################################
# command = list("당근전 요리 하는방법 알려줘".split())
# command = list("세상에서 제일 맛있는 당근전 요리 하는방법 알려줘".split())
command = list(input().split())
command_non_space = list("".join(command))
print(command_non_space)
row_len = df.count()[0] # 행의 갯수 출력
if rule_check(command_non_space, recipe_rule):
    # 처음부터 음식단어가 들어가는 경우
    # 중간에 움식단어가 들어가는 경우
    keyword_flag, response = keyword_check(df, command_non_space, RECIPE_START_ROW, RECIPE_END_ROW)
    if keyword_flag: 
        print(response)
elif rule_check(command_non_space, recipe_rule1):
    keyword_flag, response = keyword_check(df, command_non_space, RECIPE_START_ROW, RECIPE_END_ROW)
    if keyword_flag: 
        print(response)
else: 
    # 일치하는 규칙이 없을 때!
    print("아직은 레시피 기능밖에 없네요 ㅠㅠ")