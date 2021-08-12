import numpy as np
from random import choice, randint

import Bitmasking
import Generation
import RenderFunctions


def generate(arr: np.array) -> np.array:
    # False = Not Walkable, True = Walkable
    width, height = arr.shape
    wall_space = np.zeros_like(arr, dtype=np.int16)

    for j in range(width):
        for i in range(height):
            num = Bitmasking.fetch_wall((i, j), arr)
            wall_space[j, i] = num

    return wall_space


def main():
    # Test Function to Generate Random Set
    width, height = 50, 50
    ws = np.zeros((width, height), dtype=bool)
    generation_function = choice([Generation.BSP])
    generation_function(ws)
    # print(ws)
    RenderFunctions.render(ws)


if __name__ == "__main__":
    # main()
    arr = np.array([[False, False, False], [False, True, False], [False, True, False], [False, False, False]])
    print(generate(arr))
