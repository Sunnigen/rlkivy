from random import randint

import numpy as np

import tcod


def connect_rooms(ws: np.mat, room1: tcod.bsp.BSP, room2: tcod.bsp.BSP) -> None:
    if randint(0, 1) == 1:
        create_vertical_tunnel(ws, room1, room2)
        create_horizontal_tunnel(ws, room1, room2)
    else:
        create_horizontal_tunnel(ws, room1, room2)
        create_vertical_tunnel(ws, room1, room2)


def create_room(ws: np.mat, room: tcod.bsp.BSP) -> None:
    for x in range(room.x, room.x + room.width - 2):
        for y in range(room.y, room.y + room.height - 2):
            create_floor(ws, x, y)


def create_vertical_tunnel(ws: np.mat, room1: tcod.bsp.BSP, room2: tcod.bsp.BSP) -> None:
    step_count = 1
    if room2.y + room2.height // 2 < room1.y + room1.height//2:
        step_count = -1

    for i in range(room1.y + room1.height//2, room2.y + room2.height//2, step_count):
        try:
            create_floor(ws, room1.x + room1.width//2, i)
        except IndexError:
            print("\ncreate_vertical_tunnel")
            print_error(ws, room1, room2, i)


def create_horizontal_tunnel(ws: np.mat, room1: tcod.bsp.BSP, room2: tcod.bsp.BSP) -> None:
    step_count = 1
    if room2.x + room2.width // 2 < room1.x + room1.width//2:
        step_count = -1

    for i in range(room1.x + room1.width//2, room2.x + room2.width//2, step_count):
        try:
            create_floor(ws, i, room1.y + room1.height//2)
        except IndexError:
            print("\ncreate_horizontal_tunnel")
            print_error(ws, room1, room2, i)


def create_floor(ws: np.mat, x: int, y: int) -> None:
    ws[y][x] = True


def print_error(ws, room1, room2, i):
    print(f"ws shape : {ws.shape}")
    print(f"Error Index : {i}")
    print(room1, room2)
