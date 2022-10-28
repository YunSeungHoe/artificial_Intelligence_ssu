# 상태를 나타내는 클래스
class State:
  def __init__(self, board, goal, moves=0):
    self.board = board
    self.moves = moves
    self.goal = goal

  # i1과 i2를 교환하여서 새로운 상태를 반환한다. 
  def get_new_board(self, i1, i2, moves):
    new_board = self.board[:]
    new_board[i1], new_board[i2] = new_board[i2], new_board[i1]
    return State(new_board, self.goal, moves)

  # 자식 노드를 확장하여서 리스트에 저장하여서 반환한다. 
  def expand(self, moves):
    result = []
    i = self.board.index(0)		# 숫자 0(빈칸)의 위치를 찾는다. 
    if not i in [0, 1, 2] :		# UP 연산자 
      result.append(self.get_new_board(i, i-3, moves))
    if not i in [0, 3, 6] :		# LEFT 연산자 
      result.append(self.get_new_board(i, i-1, moves))
    if not i in [2, 5, 8]:		# DOWN 연산자 
      result.append(self.get_new_board(i, i+1, moves))
    if not i in [6, 7, 8]:		# RIGHT 연산자 
      result.append(self.get_new_board(i, i+3, moves))
    return result

  # 객체를 출력할 때 사용한다. 
  def __str__(self):
    return str(self.board[:3]) +"\n"+\
    str(self.board[3:6]) +"\n"+\
    str(self.board[6:]) +"\n"+\
    "------------------"

  def __eq__(self, other):
    return self.board == other.board

# 초기 상태
puzzle = [1, 2, 3, 
          0, 4, 6, 
          7, 5, 8]

# 목표 상태
goal = [1, 2, 3, 
        4, 5, 6, 
        7, 8, 0]

# open 리스트
open_queue = [ ]
open_queue.append(State(puzzle, goal))

closed_queue = [ ]
moves = 0

#  디버깅을 위한 코드
#print("START OF OPENQ")
#for elem in open_queue:
#        print(elem)
#print("END OF OPENQ")
  
while len(open_queue) != 0: 
  current = open_queue.pop(0)			# OPEN 리스트의 앞에서 삭제
  print(current)
  if current.board == goal:
      print("탐색 성공")
      break
  moves = current.moves+1
  closed_queue.append(current)		
  for state in current.expand(moves):
      if (state in closed_queue) or (state in open_queue):	# 이미 거쳐간 노드이면
          continue				# 노드를 버린다.      
      else: 
          open_queue.append(state)		# OPEN 리스트의 끝에 추가