import queue

# 상태를 나타내는 클래스, f(n) 값을 저장한다. 
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

  # f(n)을 계산하여 반환한다. 
  def f(self):
    return self.h()+self.g()

  # 휴리스틱 함수 값인 h(n)을 계산하여 반환한다. 
  # 각 타일의 목표 위치까지의 예상 비용(거리)의 합  
  def h(self):
    sum = 0
    i = 0
    while i<9 :
      n = self.goal[i] # goal에서 각 인덱스에 들어있어야하는 값들을 n이라고 하자. # 예로 i=4일때 n=5이다. 5라는 값에 대해 생각해보자.
      n_x = i // 3  # goal에서 n이 들어있어야 하는 위치의 x좌표. 
      n_y = i - 3*n_x # goal에서 n이 들어있어야 하는 위치의 y좌표. 
      # 5가 들어있어야하는 목표 좌표를 구하면 = (1,1)
      current_x = self.board.index(n) // 3 # 현재 board에서 n이 들어있는 위치의 x좌표.
      current_y = self.board.index(n) - 3*current_x #현재 board에서 n이 들어있는 위치의 y좌표.
      # 현재 5가 있는 위치의 좌표를 구하면 = (2,1)
      sum += abs(current_x - n_x) + abs(current_y - n_y) #n이 목표위치 좌표로 가기 위해 움직여야하는 비용을 sum에 축적
      # 5가 (2,1)에서 (1,1)로 가기 위해 (2-1)+(1-1) = 1이므로 총 1칸 움직여야한다. 1을 sum에 축적 후 이후 i와 n에 대해 계속 진행
      i += 1   
    return sum



  # 시작 노드로부터의 경로를 반환한다. 
  def g(self):
    return self.moves

  def __eq__(self, other):
    return self.board == other.board
 
  # 상태와 상태를 비교하기 위하여 less than 연산자를 정의한다. 
  def __lt__(self, other):
    return self.f() < other.f()

  def __gt__(self, other):
    return self.f() > other.f()

  # 객체를 출력할 때 사용한다. 
  def __str__(self):
    return "------------------ f(n)=" + str(self.f()) +"\n"+\
    "------------------ h(n)=" + str(self.h()) +"\n"+\
    "------------------ g(n)=" + str(self.g()) +"\n"+\
    str(self.board[:3]) +"\n"+\
    str(self.board[3:6]) +"\n"+\
    str(self.board[6:]) +"\n"+\
    "------------------"

# 초기 상태
puzzle = [1, 2, 3, 
          0, 4, 6, 
          7, 5, 8]

# 목표 상태
goal = [1, 2, 3, 
        4, 5, 6, 
        7, 8, 0]

# open 리스트는 우선순위 큐로 생성한다. 
open_queue = queue.PriorityQueue()
open_queue.put(State(puzzle, goal))

closed_queue = [ ]
moves = 0
while not open_queue.empty():

#  디버깅을 위한 코드
#  print("START OF OPENQ")
#  for elem in open_queue.queue:
#        print(elem)
#  print("END OF OPENQ")
  
  current = open_queue.get()
  if current.board == goal:
      print(current)
      print("탐색 성공")
      print("open queue 길이=", open_queue.qsize())
      print("closed queue 길이=", len(closed_queue))
      break
  moves = current.moves+1
  for state in current.expand(moves):
    if state not in closed_queue and state not in open_queue.queue :
      open_queue.put(state)
  closed_queue.append(current)
else:
  print ('탐색 실패')