import re, time, os, discord, asyncio, random
import pandas as pd
WORD_COL = 0
RULE_COL = 1
RESP_COL = 2
RECIPE_START_ROW = 0
RECIPE_END_ROW = 692
INGREDIENT_START_ROW = 692
INGREDIENT_END_ROW = 723
TYPE_START_ROW = 723
TYPE_END_ROW = 729

def rule_check(com, rule):
    for word in rule:
        for j in range(len(word)):
            for i in range(j, len(com), len(word)):
                command_split = "".join(com[i:i+len(word)])
                if word == command_split:
                    return True
    return False

def keyword_check1(df, com, start_len, end_len):
    matched_len = 0
    for i in range(start_len, end_len):
        compare_word = df.values[i][WORD_COL]
        search = re.search(compare_word, "".join(com))
        if search != None:
            span = search.span()
            search_len = span[1] - span[0]
            if matched_len < search_len:
                matched_len = search_len
                respon = df.values[i][RESP_COL]
                print(df.values[i][RESP_COL])
    if respon:
        return True, respon
    else:
        return False, None


def keyword_check2(df, com, start_len, end_len):
    recommend = []
    for i in range(start_len, end_len):
        compare_word = df.values[i][WORD_COL] 
        if re.search(compare_word, "".join(com)) != None:
            ingredient = df.values[i][WORD_COL]  
            for j in range(RECIPE_START_ROW, RECIPE_END_ROW):
                compare_food = df.values[j][WORD_COL] 
                if re.search(ingredient, compare_food) != None:  
                    recommend.append(compare_food)
                if len(recommend) >= 10:
                    break
            return True, recommend
    return False, None

def keyword_check3(df, com, start_len, end_len):
    recommend = []
    for i in range(start_len, end_len):
        compare_word = df.values[i][WORD_COL]
        if re.search(compare_word, "".join(com)) != None:
            food_type = df.values[i][WORD_COL] 
            if compare_word == "아무":
                num_list = [i for i in range(RECIPE_START_ROW, RECIPE_END_ROW+1)]
                random_list = random.sample(num_list, 10)
                for j in random_list:
                    recommend.append(df.values[j][WORD_COL])
            else:
                for j in range(RECIPE_START_ROW, RECIPE_END_ROW):   
                    compare_food = df.values[j][WORD_COL] 
                    if re.search(food_type, compare_food) != None:  
                        recommend.append(compare_food)
                    if len(recommend) >= 10:
                        break
            return True, recommend
    return False, None

df = pd.read_excel("dataset.xlsx", engine = "openpyxl")

recipe_rule1 = list(df.values[RECIPE_START_ROW][RULE_COL].split())
recipe_rule2 = list(df.values[INGREDIENT_START_ROW][RULE_COL].split())
recipe_rule3 = list(df.values[TYPE_START_ROW][RULE_COL].split())

discord_token ='MTA0MTk4MzQ3NTAyNjIzOTU0OA.GNYi4K.EorOHLefv7Lm73f30fnHAWabdfHJiWQ2ubFKqs'
print("discord bot starting...")
client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print("Hello We logged in as {}".format(client))
    print('I am {}'.format(client.user.name))
    print('My ID is {}'.format(client.user.id))
    
@client.event
async def on_message(message : discord.Message):
    if message.author == client.user:
        return
    command = message.content
    command_non_space = list("".join(command))
    while ' ' in command_non_space:
        command_non_space.remove(' ')
    is_done = False
    if rule_check(command_non_space, recipe_rule3):
        keyword_flag, response = keyword_check3(df, command_non_space, TYPE_START_ROW, TYPE_END_ROW)
        if keyword_flag:
            is_done = True
        
    if not is_done:
        if rule_check(command_non_space, recipe_rule1):
            keyword_flag, response = keyword_check1(df, command_non_space, RECIPE_START_ROW, RECIPE_END_ROW)
            if keyword_flag:
                is_done = True

        elif rule_check(command_non_space, recipe_rule2):
            keyword_flag, response = keyword_check2(df, command_non_space, INGREDIENT_START_ROW, INGREDIENT_END_ROW)
            if keyword_flag:
                is_done = True
            
    if not is_done:
        response = "아직은 해당 기능이 없네요\n"

    await message.channel.send(response)

client.run(discord_token)
