from __future__ import annotations

import lzma
import pickle
from typing import Tuple, TYPE_CHECKING

from tcod.map import compute_fov

import exceptions
from gui.graphics_component import GraphicsFrame
from message_log import MessageLog

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld
    from kivy.uix.widget import Widget


class Engine:
    game_map: GameMap
    game_world: GameWorld
    graphics_component: GraphicsFrame
    mouse_location: Tuple[int, int] = (0, 0)
    map_location: Tuple[int, int] = (0, 0)
    temp_location: Tuple[int, int] = None

    def __init__(self, player: Actor):
        self.message_log = MessageLog()
        self.player = player
        self.graphics_component = GraphicsFrame(self)

    def add_graphics_component(self, root_widget: Widget) -> None:
        if not self.graphics_component:
            self.graphics_component = GraphicsFrame(self)

        if self.graphics_component in root_widget.children:
            return

        root_widget.add_widget(self.graphics_component)

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.

    def normalize_mouse_pos(self, root_widget: Widget) -> None:
        # Changes the mouse location from floats, to tile coordinates on screen
        x, y = root_widget.mouse_location
        y -= 14  # Magic number offset from nearest multiple of 12
        tile_size = 32
        self.update_mouse_location(int(x // tile_size), int(y // tile_size))

    def update_mouse_location(self, x: int, y: int) -> None:
        self.mouse_location = x, y
        # Update mouse location on map
        self.update_map_location(x, y)

    def get_mouse_location(self) -> Tuple[int, int]:
        return self.mouse_location

    def update_temp_location(self, x: int, y: int) -> None:
        self.temp_location = x, y

    def get_temp_location(self) -> Tuple[int, int]:
        return self.temp_location

    def disable_temp_location(self) -> None:
        self.temp_location = None

    def update_map_location(self, x: int, y: int) -> None:
        y_offset = int(self.graphics_component.game_window.y / 32)
        map_x_offset = 10
        map_y_offset = 10

        # Check if Game Window is Centered on Player or on Temporary Location
        if self.temp_location:
            origin_x, origin_y = self.temp_location
        else:
            origin_x, origin_y = self.player.x, self.player.y

        self.map_location = x + origin_x - map_x_offset, y + origin_y - map_y_offset - y_offset

    def get_map_location(self) -> Tuple[int, int]:
        return self.map_location

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, root_widget: Widget, dt: float) -> None:
        self.normalize_mouse_pos(root_widget)
        self.graphics_component.render(root_widget, dt)
        self.message_log.render(root_widget=root_widget, engine=self, height=5)

    def disconnect_graphics_component(self) -> None:
        self.graphics_component = None

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        self.disconnect_graphics_component()
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)
