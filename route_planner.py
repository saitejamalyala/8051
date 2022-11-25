
from typing import Deque, List
def route_exists(from_row, from_column, to_row, to_column, map_matrix):

    pos = (from_row, from_column)
    visited = set()
    queue = Deque([pos])
    visited.add(pos)

    while len(queue)>0:
        pos = queue.popleft()
        if pos == (to_row, to_column):
            return True
        else:
            row,col = pos[0], pos[1]

            if row-1>=0 and map_matrix[row-1][col] == True and (row-1,col) not in visited:
                queue.append((row-1,col))
                visited.add((row-1,col))

            if row+1<len(map_matrix) and map_matrix[row+1][col] == True and (row+1,col) not in visited:
                queue.append((row+1,col))
                visited.add((row+1,col))

            if col-1>=0 and map_matrix[row][col-1] == True and (row,col-1) not in visited:
                queue.append((row,col-1))
                visited.add((row,col-1))

            if col+1<len(map_matrix[0]) and map_matrix[row][col+1] == True and (row,col+1) not in visited:
                queue.append((row,col+1))
                visited.add((row,col+1))

    return False
  


if __name__ == '__main__':
    map_matrix = [
        [True, False, False],
        [True, True, False],
        [False, True, True]
    ];

    print(route_exists(0, 0, 2, 2, map_matrix))