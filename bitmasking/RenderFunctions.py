import sys
import numpy as np

import Bitmasking
import WallChars


def render(ws: np.mat) -> None:
    # wall_chars = WallChars.WALL_CHARS
    # wall_chars = WallChars.DOUBLE_WALL_CHARS

    width, height = ws.shape

    wall_space = np.zeros((width, height), np.int16)  # need to rotate?
    # char_space = [["" for x in range(height)] for y in range(width)]

    # Create 1 Layer of Blank space around Entire Map
    # Note: This is due to conflicts of how blank indexes are interpreted the same as out of boundary indexes

    for j in range(width):
        for i in range(height):
            num = Bitmasking.fetch_wall((i, j), ws)
            wall_space[j, i] = num
            # try:
            #     char_space[j][i] = wall_chars[num]
            # except KeyError:
            #     char_space[j][i] = " "

    for x in range(width):
        # char_space[x][height - 1] = " "
        # char_space[x][0] = " "
        wall_space[x][height - 1] = 0
        wall_space[x][0] = 0

    for y in range(height):
        # char_space[width - 1][y] = " "
        # char_space[0][y] = " "
        wall_space[width - 1][y] = 0
        wall_space[0][y] = 0

    np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)
    print("\nWall space :")
    print(wall_space)
    # print("\nChar space: ")
    # for row in char_space:
    #     print(' '.join(row))

    # Check for Missing Walls
    # for j in range(width):
    #     for i in range(height):
    #         char = char_space[j][i]
    #         if char == " ":
    #             if not wall_space[j][i] in [0, 255]:
    #                 print(f"{wall_space[j][i]} should have a character!!!")


