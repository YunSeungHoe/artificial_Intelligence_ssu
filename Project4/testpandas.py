import pandas as pd

# pandas 엑셀의 값을 넣으면 df에 저장됨.
df = pd.read_excel("artest.xlsx")
# debug 
# print(df)

# 행의 갯수 출력 / 
row_len = df.count()[0]

for i in range(0, row_len):
    or_list = list(map(str, df.values[i][0].split()))
    and_list = list(map(str, df.values[i][1].split()))
    # debug
    # print(or_list, and_list) # [필수 입력 값 리스트] [한개라도 만족하는지 확인하는 리스트]
    # print(df.values[i][2]) # [작성한 레시피 확인]