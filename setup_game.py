"""Handle the loading and initialization of game sessions."""
from __future__ import annotations

import copy
import lzma
import pickle
import traceback
from typing import Optional

import tcod

from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget

import color
from engine import Engine
import entity_factories
from game_map import GameWorld
import input_handlers
import kivy_input_handlers


def new_game() -> Engine:
    """Return a brand new game session as an Engine instance."""
    # map_width = 40
    # map_height = 25
    #
    # room_max_size = 10
    # room_min_size = 5
    # max_rooms = 30


    map_width = 30
    map_height = 30

    room_max_size = 3
    room_min_size = 2
    max_rooms = 20

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)
    # player.fighter.base_power = 50

    curr_floor = 0

    engine.game_world = GameWorld(
        engine=engine,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        current_floor=curr_floor
    )

    engine.game_world.generate_floor()
    engine.update_fov()

    engine.message_log.add_message(
        "Hello and welcome, adventurer, to yet another dungeon!", color.welcome_text
    )

    dagger = copy.deepcopy(entity_factories.dagger)
    leather_armor = copy.deepcopy(entity_factories.leather_armor)

    dagger.parent = player.inventory
    leather_armor.parent = player.inventory

    player.inventory.items.append(dagger)
    player.equipment.toggle_equip(dagger, add_message=False)

    player.inventory.items.append(leather_armor)
    player.equipment.toggle_equip(leather_armor, add_message=False)

    return engine


def load_game(filename: str) -> Engine:
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine


class MainMenu(kivy_input_handlers.BaseEventHandler):
    """Handle the main menu rendering and input."""

    def __on_enter__(self, root_widget: Widget) -> None:
        # Background Picture
        self.bg_image = Image(source="assets/menu_background.png", allow_stretch=True)
        self.bg_image.size = 300, 300
        self.bg_image.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        root_widget.add_widget(self.bg_image)

        # Menu Options
        menu_title_color = [c/255 for c in color.menu_title] + [1]

        text = "Tombs of the Ancient Kings\n\n\n\n[N] Play a new game\n\n[C] Continue last game\n\n[Q] Quit".upper()
        self.title_label = Label(text=text, color=menu_title_color)
        # self.title_label = Label(text=text, color=menu_title_color, font_name="assets/fonts/whitrabt.ttf")
        root_widget.add_widget(self.title_label)

    def __on_exit__(self, root_widget: Widget) -> None:
        root_widget.clear_widgets()
        self.bg_image = None
        self.title_label = None
        # root_widget.update(0)

    def on_render(self, root_widget: Widget, dt: float) -> None:
        return None

    def ev_keydown(self, event: str) -> Optional[kivy_input_handlers.BaseEventHandler]:
        if event in ("q", "escape"):
            raise SystemExit()
        elif event == "c":
            try:
                return kivy_input_handlers.MainGameEventHandler(load_game("savegame.sav"))
            except FileNotFoundError:
                print("No saved game to load.")
                return kivy_input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()  # Print to stderr.
                print(traceback.print_exc(), exc)
                return kivy_input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event == "n":
            return kivy_input_handlers.MainGameEventHandler(new_game())

        return None

    def ev_mousebutton(self, event: str) -> Optional[kivy_input_handlers.BaseEventHandler]:
        pass
    #     return super(MainMenu, self).ev_mousebutton(event)
