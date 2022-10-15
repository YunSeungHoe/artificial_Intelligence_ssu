#!/usr/bin/python3
# -*- coding: utf-8 -*-

from collections import deque
import  random

INITSTATE = [2, 8, 3, 
             1, 6, 4, 
             7, 0, 5]
GOALSTATE = [1, 2, 3, 
             8, 0, 4, 
             7, 6, 5]
CloseQue = []
OpenQue = deque([])
PathQue = []

def SetInit():
    numlist = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    return random.sample(numlist, 9)

# 현재 상태를 출력하는 것
def scrin(board):
    print(board[0:3])
    print(board[3:6])
    print(board[6:9])

def ListMin(list):
    Small = list[0]
    for val in list:
        if val <= Small:
            Small = val
    return Small

class Puzzle:
    global OpenQue
    def __init__(self, board, goal, move=0):
        self.board = board
        self.goal = goal
        self.move = move
        
    # 남은 거리 계산 h(n) : heuristic
    def Remaining(self):
        count = 0
        for current_val, goal_val in zip(self.board, GOALSTATE):
            if current_val is goal_val and current_val != 0:
                count += 1
        return 8 - count      
          
    # 지니간 거리 계산 g(n)    
    def Passed(self):
        return self.move
    
    # 전체 비용 : f(n) = g(n) + h(n)
    def AllValue(self):
        return self.Passed() + self.Remaining()

    # 0의 위치를 찾는 index
    def FindZero(self):
        for index in range(len(self.board)):
            if self.board[index] == 0:
                return index

    # fir와 sec의 값을 바꾼다.
    def ChangeVal(self, fir, sec):
        TempBoard = self.board[:]
        TempBoard[fir], TempBoard[sec] = TempBoard[sec], TempBoard[fir]
        return TempBoard
                
    # 다음 퍼즐의 모양을 리스트에 담는다.    
    def NextState(self):
        NextList = [] # 다음으로 올수 있는 보드의 모양
        NextVal = []  # 다음으로 올수 있는 보드의 f(n) 값
        self.move += 1
        ZeroIndex = self.FindZero()
        CloseQue.append(self.board)
        print("지나간 보드")
        scrin(self.board)
        if not ZeroIndex in [0, 3, 6]: # 0을 왼쪽으로 움직일 수 있다.
            if not self.ChangeVal(ZeroIndex, ZeroIndex - 1) in CloseQue:
                NextList.append(Puzzle(self.ChangeVal(ZeroIndex, ZeroIndex - 1), GOALSTATE, self.move))
        if not ZeroIndex in [2, 5, 8]: # 0을 오른쪽으로 움직일 수 있다.
            if not self.ChangeVal(ZeroIndex, ZeroIndex + 1) in CloseQue:
                NextList.append(Puzzle(self.ChangeVal(ZeroIndex, ZeroIndex + 1), GOALSTATE, self.move))
        if not ZeroIndex in [0, 1, 2]: # 0을 위로 움직일 수 있다.
            if not self.ChangeVal(ZeroIndex, ZeroIndex - 3) in CloseQue:
                NextList.append(Puzzle(self.ChangeVal(ZeroIndex, ZeroIndex - 3), GOALSTATE, self.move))
        if not ZeroIndex in [6, 7, 8]: # 0을 아래로 움직일 수 있다.
            if not self.ChangeVal(ZeroIndex, ZeroIndex + 3) in CloseQue:
                NextList.append(Puzzle(self.ChangeVal(ZeroIndex, ZeroIndex + 3), GOALSTATE, self.move))

        # 다음으로 갈수 있는 보드가 없다.
        if len(NextList) == 0:
            return 
        
        # 다음으로 갈수 있는 보드들의 f(n) 값을 넣는다.
        for i in NextList:
            NextVal.append(i.AllValue())
        
        # 다음으로 갈수 있는 보드들의 f(n) 값 중에서 최소값을 찾는다.
        Small = ListMin(NextVal)        
        
        # 다음으로 갈 수 있는 보드들의 최소값을 가지는 보드들의 인덱스를 리스트에 저장
        NextIndex = list(filter(lambda x: NextVal[x] == Small, range(len(NextVal))))
        
        # 다음으로 갈 수 있는 보드들 중에서 갈수 있는 리스트를 open 큐에 저장
        for i in NextIndex:
            if NextVal[i] != Small:
                if not NextList[i].board in CloseQue:
                    CloseQue.append(NextList[i].board)
            OpenQue.appendleft(Puzzle(NextList[i].board, GOALSTATE, self.move))
        return

    def __Path__(self):
        a = 1
    

def main():
    global OpenQue
    # INITSTATE = SetInit()
    OpenQue.appendleft(Puzzle(INITSTATE, GOALSTATE))
    print("==========")
    print("시작 상태")
    scrin(INITSTATE)
    
    print("\n목표 상태")
    scrin(GOALSTATE)
    print("==========\n")
    
    while len(OpenQue) != 0:
        # time.sleep(1)
        current = OpenQue.popleft()
        if current.board == GOALSTATE:
            print("\n==========")
            print("탐색 성공")
            scrin(current.board)
            print("==========")
            break
        current.NextState()
    if current.board != GOALSTATE:
        print("탐색 실패")
        
if __name__ == '__main__':
    main()
