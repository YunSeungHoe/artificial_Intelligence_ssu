#!/usr/bin/python3
# -*- coding: utf-8 -*-

import math, time, random, queue

INITSTATE = [2, 8, 3, 
             1, 6, 4, 
             7, 0, 5]
GOALSTATE = [1, 2, 3, 
             8, 0, 4, 
             7, 6, 5]

def SetInit():
    numlist = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    return random.sample(numlist, 9)

# 현재 상태를 출력하는 것
def scrin(board):
    print(board[0:3])
    print(board[3:6])
    print(board[6:9])

class Puzzle:
    PathQue = queue.Queue()
    CloseQue = queue.Queue()
    def __init__(self, board, goal, move=0):
        self.board = board
        self.goal = goal
        self.move = move
        
    # 남은 거리 계산 h(n) : heuristic
    def Remaining(self, current):
        count = 0
        for current_val, goal_val in zip(current, GOALSTATE):
            if current_val is goal_val:
                count += 1
        return count      
          
    # 지니간 거리 계산 g(n)    
    def Passed(self):
        return self.move
    
    # 전체 비용 : f(n) = g(n) + h(n)
    def AllValue(self, current):
        return self.Passed() + self.Remaining(current)

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
        NextList = []
        ZeroIndex = self.FindZero()
        if not ZeroIndex in [0, 1, 2]: # 0을 위로 올릴 수 있다.
            NextList.append(self.ChangeVal(ZeroIndex, ZeroIndex - 3))
        if not ZeroIndex in [6, 7, 8]: # 0을 아래로 내릴 수 있다.
            NextList.append(self.ChangeVal(ZeroIndex, ZeroIndex + 3))
        if not ZeroIndex in [0, 3, 6]: # 0을 왼쪽으로 움직일 수 있다.
            NextList.append(self.ChangeVal(ZeroIndex, ZeroIndex - 1))
        if not ZeroIndex in [2, 5, 8]: # 0을 오른쪽으로 움직일 수 있다.
            NextList.append(self.ChangeVal(ZeroIndex, ZeroIndex + 1))
        return NextList
            
    def __Path__(self):
        a = 1
    

def main():
    print("처음 퍼즐 모양 : ")
    scrin(INITSTATE)
    a = Puzzle(INITSTATE, GOALSTATE)
    
    
if __name__ == '__main__':
    main()
