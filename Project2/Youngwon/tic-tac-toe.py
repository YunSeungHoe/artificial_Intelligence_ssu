import copy

board = [" "] * 10

def print_board(board):
    print("┌───┬───┬───┐")
    print("│ " + board[1] + " │ " + board[2] + " │ " + board[3] +" │")
    print("├───┼───┼───┤")
    print("│ " + board[4] + " │ " + board[5] + " │ " + board[6] +" │")
    print("├───┼───┼───┤")
    print("│ " + board[7] + " │ " + board[8] + " │ " + board[9] +" │")
    print("└───┴───┴───┘")


def judge(board,letter):
    return ((board[1] == board[2] == board[3] == letter) or
 
            (board[4] == board[5] == board[6] == letter) or
            
            (board[7] == board[8] == board[9] == letter) or
            
            (board[1] == board[4] == board[7] == letter) or
            
            (board[2] == board[5] == board[8] == letter) or
            
            (board[3] == board[6] == board[9] == letter) or
            
            (board[1] == board[5] == board[9] == letter) or
            
            (board[3] == board[5] == board[7] == letter))


def Computer_best(board):
    for i in range(1, 10):
        copy_board = []
        for n in board:
            copy_board.append(n)

        if copy_board[i] == " ":
            copy_board[i] = "O"
            if judge(copy_board, 'O'):
                return i

    for i in range(1, 10):
        copy_board = []
        for n in board:
            copy_board.append(n)

        if copy_board[i] == " ":
            copy_board[i] = "X"
            if judge(copy_board, 'X'):
                return i

    for i in range(1,10):
            if board[i] == " ":
                return i



i=0
while True:
  x = int(input("당신의 수를 놓을 위치를 입력하세요: "))

  if board[x] != " ":
    print("잘못된 위치입니다.")
    continue
  else:
    board[x] = "X"
    print_board(board)


  if judge(board, "X"):
    print("Player 우승")
    break
  i += 1

  if i == 9:
    print("무승부")
    break
  
  print("컴퓨터가 수를 놓습니다.")
  Computer_input = Computer_best(board)
  board[Computer_input] = "O"
  print_board(board)

  if judge(board, "O"):
    print("Computer 우승")
    break
  i += 1
  
