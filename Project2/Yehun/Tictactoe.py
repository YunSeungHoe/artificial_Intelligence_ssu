import math
import random
import time

class Tictattoe:
    def __init__(self):
        self.board = [0 for i in range(9)]
        self.maxPlayer = 'X'
        self.minPlayer = 'O'

    def main(self):
        print("\n")
        self.show()
        while len(self.empty_idx(self.board)) > 0 and not self.game_over(self.board): 
            # 빈 칸이 있고 게임이 끝나지 않았으면
            self.player_turn(self.board)
            self.com_turn(self.board)
        
        if self.win(self.board, self.maxPlayer):
            print("You win!")
        elif self.win(self.board, self.minPlayer):
            print("You lose...")
        else:
            print("Draw.")

    def evaluate(self, board): # prunning에 사용되는 점수이다.
        # 사람이 이기는 경우는 +1점, 컴퓨터가 이기는 경우는 -1점, 무승부는 0점으로 평가
        if self.win(board, self.maxPlayer): 
            self.score = 1
        elif self.win(board, self.minPlayer):
            self.score = -1
        else:
            self.score = 0
        return self.score
    
    def win(self, board, player): # win 조건에 해당하면 True를 리턴 그렇지 않으면 False를 리턴한다.
        win_cond = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]]

        for c1,c2,c3 in win_cond:
            if board[c1] == board[c2] == board[c3] == player:
                return True
        return False
            
    def player_turn(self, board):
        position = int(input("Your turn : ")) - 1
        while position not in self.empty_idx(board):
            print("It exist already.")
            position = int(input("Your turn : ")) - 1
            print("\n")
        board[position] = self.maxPlayer
        self.show()
        time.sleep(1)
    
    def com_turn(self, board):
        print("Computer played.")
        depth = len(self.empty_idx(board))
        if depth == 0 or self.game_over(board):
            return
        position, _ = self.prunning(board, depth, -math.inf, math.inf, self.minPlayer)
        board[position] = self.minPlayer
        self.show()
        time.sleep(1)

    def game_over(self, board): # 게임이 끝났으면 True를 그렇지 않으면 False를 리턴한다.
        return self.win(board, self.maxPlayer) or self.win(board, self.minPlayer)

    def empty_idx(self, board): # 비어 있는 칸의 인덱스를 리스트로 리턴한다.
        empty_list = []
        for i in range(9):
            if board[i] == 0:
                empty_list.append(i)
        return empty_list

    def prunning(self, board, depth, alpha, beta, player): # 알파-베타 가지치기로 컴퓨터가 어느 칸에 놓는 것이 최적인지 계산하고 해당 인덱스를 리턴한다.
        # alpha: min 노드의 부모(max), beta: max 노드의 부모(min)
        if depth == 0 or self.game_over(board):
            score = self.evaluate(board)
            return [-1, score] # [position, score]
        
        if player == self.maxPlayer: # 베타 가지치기
            prev = -math.inf
            for idx in self.empty_idx(board):
                board[idx] = player # player가 빈 칸에 돌을 놓는다 가정한다.
                now = self.prunning(board, depth-1, alpha, beta, self.minPlayer)[1] # 현재 값
                if prev < now: # 이전 값보다 더 큰 값을 찾으면 해당 값으로 바꾼다.
                    prev = now
                    position = idx
                alpha = max(alpha, prev) # 자식노드 중 최대값을 선택한다.
                board[idx] = 0 # 판을 원래대로 돌려 놓는다.
                if alpha >= beta:  # 부모 노드의 값보다 더 큰 값을 찾으면 나머지는 탐색하지 않는다.
                    break
            return [position, alpha]
        else: # 알파 가지치기
            prev = math.inf # 이전 값
            for idx in self.empty_idx(board):
                board[idx] = player # player가 빈 칸에 돌을 놓는다 가정한다.
                now = self.prunning(board, depth-1, alpha, beta, self.maxPlayer) # 현재 값
                if prev > now[1]: # 이전 값보다 더 작은 값을 찾으면 해당 값으로 바꾼다.
                    prev = now[1]
                    position = idx
                beta = min(beta, prev) # 자식노드 중 최소값을 선택한다.
                board[idx] = 0 # 판을 원래대로 돌려 놓는다.
                if alpha >= beta: # 부모 노드의 값보다 더 작은 값을 찾으면 나머지는 탐색하지 않는다.
                    break
            return [position, beta]
        
    def show(self):
        showlist = []
        for i in range(1, 10):
            if self.board[i-1] is 'X' or self.board[i-1] is 'O':
                showlist.append(self.board[i-1])
            else:
                showlist.append(i)
        print("┌───┬───┬───┐")
        print("│ " + str(showlist[0]) + " │ " + str(showlist[1]) + " │ " + str(showlist[2]) +" │")
        print("├───┼───┼───┤")
        print("│ " + str(showlist[3]) + " │ " + str(showlist[4]) + " │ " + str(showlist[5]) +" │")
        print("├───┼───┼───┤")
        print("│ " + str(showlist[6]) + " │ " + str(showlist[7]) + " │ " + str(showlist[8]) +" │")
        print("└───┴───┴───┘")
        
game = Tictattoe()
game.main() 
