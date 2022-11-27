import pandas as pd
import re, time

WORD_COL = 0
RULE_COL = 1
RESP_COL = 2

RECIPE_START_ROW = 0 
RECIPE_END_ROW = 14
INGREDIENT_START_ROW = 0
INGREDIENT_END_ROW = 10
TYPE_START_ROW = 0
TYPE_END_ROW = 6

# 1. 사용자가 기능을 선택한다.
# 2. 해당 기능에 해당하는 키워드를 입력하면 답변한다.

def keyword_check(df, com, start_len, end_len): ### 동일한 이름이 들어간 음식을 구분하도록 ex)김치찌개, 참치 김치찌개
    matched_len = 0
    response = ""
    for i in range(start_len, end_len):
        compare_word = df.values[i][WORD_COL]
        search = re.search(compare_word, "".join(com))
        if search != None:
            span = search.span()
            if matched_len < span[1] - span[0]:
                matched_len = span[1] - span[0]
                response = df.values[i][RESP_COL]
    if response:
        return True, response
    else:
        return False, None

# pandas 엑셀의 값을 넣으면 df에 저장됨.
df_recipe = pd.read_excel("stew.xlsx")
df_ingredient = ""
df_type = pd.read_excel("type.xlsx")
print(df_recipe.values[13])
print(df_type.values[6])
##################################################
# 룰을 리스트에 저장 
# 지금은 레시피와 관련된 룰만 하지만 
# 추후, 확장의 가능성을 남겨둠
##################################################

rule_1 = ["요리, 조리, 레시피, 만들, 어떻게, 만드는, 순서"] # 기능 1. 레시피 추천
rule_2 = [] # 기능 2. 메인 재료로 음식 추천
rule_3 = ["추천, 알려, 뭐, 어떤"] # 기능 3. 음식 종류로 음식 추천

##################################################
# 입력을 받아 공백을 제거 
# 한글을 처리하기 위해서는 공백을 제거할 필요가 있음
##################################################
# command = list("당근전 요리 하는방법 알려줘".split())
# command = list("세상에서 제일 맛있는 당근전 요리 하는방법 알려줘".split())

print("챗봇: 무엇을 알려드릴까요?")
print("1. 레시피")
print("2. 음식 추천(메인 재료)")
print("3. 음식 추천(요리 종류)")
print("서비스 종료를 원하시면 '종료'를 입력하세요.")
print()
command = input("나: ")
print()

if "종료" in command: ### 종료 조건
    print("이용해 주셔서 감사합니다!")

if command == "1":
    print("챗봇: 어떤 레시피를 알려드릴까요?")
    rule = rule_1
    df = df_recipe
    START_ROW = RECIPE_START_ROW
    END_ROW = RECIPE_END_ROW
elif command == "2":
    print("챗봇: 먹고 싶은 메인 재료를 입력하세요!")
    rule = rule_2
    df = df_ingredient
    START_ROW = INGREDIENT_START_ROW
    END_ROW = INGREDIENT_END_ROW
elif command == "3":
    print("챗봇: 먹고 싶은 요리 종류를 입력하세요!")
    rule = rule_3
    df = df_type
    START_ROW = TYPE_START_ROW
    END_ROW = TYPE_END_ROW
print()
command = list(input("나: ").split())
command_non_space = list("".join(command))
print()

keyword_flag, response = keyword_check(df, command_non_space, START_ROW, END_ROW)
while keyword_flag == False:
    keyword_flag, response = keyword_check(df, command_non_space, START_ROW, END_ROW)
    
print(response)
print()