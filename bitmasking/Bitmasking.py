from enum import IntFlag
from typing import Tuple
import numpy as np



"""
Bitmasking.py takes a boolean matrix and a position within the matrix and returns an integer
"""


class Wall(IntFlag):
    EAST = 2**0
    SOUTHEAST = 2**1
    SOUTH = 2**2
    SOUTHWEST = 2**3
    WEST = 2**4
    NORTHWEST = 2**5
    NORTH = 2**6
    NORTHEAST = 2**7


def fetch_wall(pos: Tuple[int, int], walkable_space: np.mat) -> int:
    x, y = pos
    _height, _width = walkable_space.shape
    if walkable_space[y, x]:
        return 0

    wall = 0
    # ORDER
    d = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    for i in range(len(d)):
        dx, dy = d[i]

        # Below causes non-wall coordinates and out-of-grid-coordinates to be same value 0
        if 0 <= y+dy < _height and 0 <= x+dx < _width:
            wall += abs((not walkable_space[y+dy, x+dx]) * 2**i)

    return wall


def generate(arr: np.array) -> np.array:
    # False = Not Walkable, True = Walkable
    width, height = arr.shape
    wall_space = np.zeros_like(arr, dtype=np.int16)

    for j in range(width):
        for i in range(height):
            num = fetch_wall((i, j), arr)
            wall_space[j, i] = num

    return wall_space


if __name__ == "__main__":
    arr = np.array([[False, False, False], [False, True, False], [False, True, False], [False, False, False]])
    print(generate(arr))
    # from WallChars import WALL_CHARS
    #
    # wall_chars = WALL_CHARS
    # ws = np.zeros((10, 10), dtype=bool)
    # height, width = ws.shape
    #
    # # room 1
    # ws[1:4, 1:4] = True
    #
    # # room 2
    # ws[1:4, 5:8] = True
    # # connector room 1/2
    # ws[2, 4] = True
    #
    # # room 3
    # ws[5:8, 1:4] = True
    # # connector 2/4
    # ws[4, 6] = True
    # # connector 3/4
    # ws[6, 4] = True
    #
    # print("Walkable Space :")
    # print(ws)
    # print()
    #
    # wall_space = np.zeros(ws.shape, np.int16)
    # char_space = [["" for x in range(10)] for y in range(10)]
    #
    # for j in range(height):
    #     for i in range(width):
    #         num = fetch_wall((i, j), ws)
    #         wall_space[j, i] = num
    #         try:
    #             char_space[j][i] = wall_chars[num]
    #         except KeyError:
    #             char_space[j][i] = " "
    #
    # print("Wall Space : ")
    # print(wall_space)
    # print("\nChar Space : ")
    # for row in char_space:
    #     print(''.join(row))
