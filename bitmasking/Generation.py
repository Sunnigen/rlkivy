from random import randint

import numpy as np
import tcod


import Room


def premade(ws: np.mat):
    # room 1
    ws[1:4, 1:4] = True

    # room 2
    ws[1:4, 5:8] = True
    # connector room 1/2
    ws[2, 4] = True

    # room 3
    ws[5:8, 1:4] = True
    # connector 1/3
    ws[4, 2] = True

    # room 4
    ws[5:8, 5:8] = True
    # connector 2/4
    ws[4, 6] = True
    # connector 3/4
    ws[6, 4] = True


def tunnel(ws: np.mat):
    width, height = ws.shape


def CellularAutomata(ws: np.mat):
    height, width = ws.shape


def BSP(ws: np.mat) -> None:
    # print("BSP : ", ws.shape)
    height, width = ws.shape
    bsp = tcod.bsp.BSP(x=2, y=2, width=width - 4, height=height - 4)
    bsp.split_recursive(
        # depth=randint(10, 15)
        depth=6,
        min_width=1,
        min_height=1,
        max_horizontal_ratio=1.5,
        max_vertical_ratio=1.5,
    )

    # In pre-order, leaf nodes are visited before the nodes that connect them
    for node in bsp.pre_order():
        if node.children:
            node1, node2 = node.children
            Room.connect_rooms(ws, node1, node2)
        else:

            # Room Too Big, Split Further
            limit = 6
            if node.width > width//limit and node.height > height//limit and node.width > 3 and node.height > 3:
                BSP(ws[node.y + 1:node.y + node.height - 1, node.x + 1: node.x + node.width - 1])
            else:  # Dig out room
                Room.create_room(ws, node)
