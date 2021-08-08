from __future__ import annotations

import os

from typing import Callable, Optional, Tuple, TYPE_CHECKING, Union

import tcod

import actions
from actions import (
    Action,
    BumpAction,
    PickupAction,
    WaitAction,
)
import color
import exceptions

from kivy.event import EventDispatcher
from kivy.lang import Builder
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget

if TYPE_CHECKING:
    from engine import Engine
    from entity import Item

from keyboard_listener import keyboard_inputs

MOVE_KEYS = {
    # Arrow keys.
    "up": (0, 1),
    "down": (0, -1),
    "left": (-1, 0),
    "right": (1, 0),
    "home": (-1, -1),
    "end": (-1, 1),
    "pageup": (1, 1),
    "pagedown": (1, -1),
    # Vi keys
    "h": (-1, 0),
    "j": (0, -1),
    "k": (0, 1),
    "l": (1, 0),
    "y": (-1, -1),
    "u": (1, -1),
    "b": (-1, 1),
    "n": (1, 1),
    # Num pad
    "numpad1": (-1, -1),
    'numpad2': (0, -1),
    'numpad3': (1, -1),
    'numpad4': (-1, 0),
    'numpad6': (1, 0),
    'numpad7': (-1, 1),
    'numpad8': (0, 1),
    'numpad9': (1, 1),
}

CONFIRM_KEYS = {
    "enter",
    "numpadenter",
}

WAIT_KEYS = {
    ".",
    "numpad5",
    "backspace",
}

# WAIT_KEYS = {
#     tcod.event.K_PERIOD,
#     tcod.event.K_KP_5,
#     tcod.event.K_CLEAR,
# }

ActionOrHandler = Union[Action, "BaseEventHandler"]
"""An event handler return value which can trigger an action or switch active handlers.

If a handler is returned then it will become the active handler for future events.
If an action is returned it will be attempted and if it's valid then
MainGameEventHandler will become the active handler.
"""


Builder.load_string("""
<ItemLabel>:
    text_size: self.size
    halign: "left"
    valign: "middle"
""")


class BaseEventHandler(EventDispatcher):

    def dispatch_event(self, event: str, event_type) -> Optional[BaseEventHandler]:
        # print(f"dispatch_event event:{event} event_type:{event_type}")
        # Key Press
        if event_type in ["keydown", "keyup"]:
            return self.ev_keydown(event)

        # Mouse Button
        elif event_type in ["left", "right"]:
            # print(f" Mouse event at {self.__class__}")
            return self.ev_mousebutton(event)

        return None

    def handle_events(self, event: str, event_type: str) -> BaseEventHandler:
        """Handle an event and return the next active event handler."""
        state = self.dispatch_event(event, event_type)
        if isinstance(state, BaseEventHandler):
            return state
        assert not isinstance(state, Action), f"{self!r} can not handle actions."
        return self

    def __on_enter__(self, root_widget: Widget) -> None:
        raise NotImplementedError()

    def __on_exit__(self, root_widget: Widget) -> None:
        raise NotImplementedError()

    def on_render(self, root_widget: Widget, dt: float) -> None:
        raise NotImplementedError()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: str) -> Optional[BaseEventHandler]:
        raise NotImplementedError()

    def ev_mousebutton(self, event: str) -> Optional[BaseEventHandler]:
        raise NotImplementedError()


class PopupMessage(BaseEventHandler):
    """Display a popup text window."""

    def __init__(self, parent_handler: BaseEventHandler, text: str, **kwargs):
        super(PopupMessage, self).__init__(**kwargs)
        self.parent = parent_handler
        self.text = text

    def __on_enter__(self, root_widget: Widget) -> None:
        pass

    def __on_exit__(self, root_widget: Widget) -> None:
        pass

    def on_render(self, root_widget: Widget, dt: float) -> None:
        """Render the parent and dim the result, then print the message on top."""
        self.parent.on_render(root_widget, dt)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[BaseEventHandler]:
        """Any key returns to the parent handler."""
        return self.parent

    def ev_mousebutton(self, event: str) -> Optional[BaseEventHandler]:
        """Any mouse click returns to the parent handler."""
        return self.parent


class EventHandler(BaseEventHandler):

    def __init__(self, engine: Engine, **kwargs):
        super(EventHandler, self).__init__(**kwargs)
        self.engine = engine

    def __on_enter__(self, root_widget: Widget) -> None:
        pass

    def __on_exit__(self, root_widget: Widget) -> None:
        pass

    def handle_events(self, event: str, event_type: str) -> BaseEventHandler:
        """Handle events for input handlers with an engine."""
        action_or_state = self.dispatch_event(event, event_type)
        if isinstance(action_or_state, BaseEventHandler):
            return action_or_state
        if self.handle_action(action_or_state):
            # A valid action was performed.
            if not self.engine.player.is_alive:
                # The player was killed sometime during or after the action.
                return GameOverEventHandler(self.engine)
            elif self.engine.player.level.requires_level_up:
                return LevelUpEventHandler(self.engine)
            return MainGameEventHandler(self.engine)  # Return to the main handler.
        return self

    def handle_action(self, action: Optional[Action]) -> bool:
        """Handle actions returned from event methods.

        Returns True if the action will advance a turn.
        """
        if action is None:

            return False

        try:
            action.perform()
        except exceptions.Impossible as exc:
            self.engine.message_log.add_message(exc.args[0], color.impossible)
            return False  # Skip enemy turn on exceptions.

        self.engine.handle_enemy_turns()

        self.engine.update_fov()
        return True

    def on_render(self, root_widget: Widget, dt: float) -> None:
        self.engine.render(root_widget, dt)


class AskUserEventHandler(EventHandler):
    """Handles user input for actions which require special input."""

    menu: BoxLayout = None
    bg: Rectangle = None

    def __init__(self, engine, **kwargs):
        super(AskUserEventHandler, self).__init__(engine)
        # Create Framed Menu with Cursor or Highlight
        self.menu = BoxLayout(pos_hint={"top":0.75, "center_x":0.35}, orientation="vertical", size_hint=(None, None))
        with self.menu.canvas:
            Color(0.5, 0.25, 0.1, 1)
            self.bg = Rectangle(pos=self.menu.pos, size=self.menu.size)

    def __on_exit__(self, root_widget: Widget) -> None:
        root_widget.remove_widget(self.menu)
        self.menu.clear_widgets()
        self.menu.canvas.clear()
        self.rect = None

    # def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
    #     """By default any key exits this input handler."""
    #     if event.sym in {  # Ignore modifier keys.
    #         tcod.event.K_LSHIFT,
    #         tcod.event.K_RSHIFT,
    #         tcod.event.K_LCTRL,
    #         tcod.event.K_RCTRL,
    #         tcod.event.K_LALT,
    #         tcod.event.K_RALT,
    #     }:
    #         return None
    #     return self.on_exit()

    def ev_keydown(self, event: str) -> Optional[ActionOrHandler]:
        """By default any key exits this input handler."""
        if event in {  # Ignore modifier keys.
            "shift",
            "rshift",
            "lctrl",
            "rctrl",
            "alt",
            "alt-gr",
        }:
            return None
        return self.on_exit()

    # def ev_mousebuttondown(
    #     self, event: tcod.event.MouseButtonDown
    # ) -> Optional[ActionOrHandler]:
    #     """By default any mouse click exits this input handler."""
    #     return self.on_exit()

    def ev_mousebutton(self, event: str) -> Optional[ActionOrHandler]:
        """By default any mouse click exits this input handler."""
        return self.on_exit()

    def on_exit(self) -> Optional[ActionOrHandler]:
        """Called when the user is trying to exit or cancel an action.

        By default this returns to the main event handler.
        """
        return MainGameEventHandler(self.engine)


class CharacterScreenEventHandler(AskUserEventHandler):
    TITLE = "Character Information"
    MENU_WIDTH = 300
    MENU_HEIGHT = 175

    def __on_enter__(self, root_widget: Widget) -> None:
        root_widget.add_widget(self.menu)

        # Title
        title_label = Label(text=self.TITLE)
        self.menu.add_widget(title_label)
        self.update_menu()

        # Add Menu to Include Level Up Options
        stats_label = Label(text=f"Level: {self.engine.player.level.current_level}\n"
                                 f"XP: {self.engine.player.level.current_xp}\n"
                                 f"XP for Next Level: {self.engine.player.level.experience_to_next_level}\n"
                                 f"Attack: {self.engine.player.fighter.power}\n"
                                 f"Defense: {self.engine.player.fighter.defense}")
        self.menu.add_widget(stats_label)

    def update_menu(self, dt=0) -> None:
        self.menu.size = self.MENU_WIDTH, self.MENU_HEIGHT
        self.bg.pos = self.menu.pos
        self.bg.size = self.menu.size

    def on_render(self, root_widget: Widget, dt: float) -> None:
        super().on_render(root_widget, dt)
        self.update_menu()


class LevelUpEventHandler(AskUserEventHandler):
    TITLE = "Level Up\nCongradulations! You level up!\nSelect an attribute to increase."
    MENU_WIDTH = 250
    MENU_HEIGHT = 150

    def __on_enter__(self, root_widget: Widget) -> None:
        root_widget.add_widget(self.menu)

        # Title
        title_label = Label(text=self.TITLE)
        self.menu.add_widget(title_label)
        self.update_menu()

        # Add Menu to Include Level Up Options
        selections_label = Label(text=f"a) Constituition (+20 HP, from {self.engine.player.fighter.max_hp})\n"
                                      f"b) Strength (+1 attack, from {self.engine.player.fighter.power})\n"
                                      f"c) Defense (+1 defense, from{self.engine.player.fighter.defense})")
        self.menu.add_widget(selections_label)

    def update_menu(self) -> None:
        self.menu.size = self.MENU_WIDTH, self.MENU_HEIGHT
        self.bg.pos = self.menu.pos
        self.bg.size = self.menu.size

    def on_render(self, root_widget: Widget, dt: float) -> None:
        super().on_render(root_widget, dt)
        self.update_menu()

    def ev_keydown(self, event: str) -> Optional[ActionOrHandler]:
        player = self.engine.player
        key = event
        index = keyboard_inputs[key] - 97

        if 0 <= index <= 2:
            if index == 0:
                player.level.increase_max_hp()
            elif index == 1:
                player.level.increase_power()
            else:
                player.level.increase_defense()
        else:
            self.engine.message_log.add_message("Invalid entry.", color.invalid)

            return None

        return super().ev_keydown(event)

    # def ev_mousebuttondown(
    #     self, event: tcod.event.MouseButtonDown
    # ) -> Optional[ActionOrHandler]:
    #     """
    #     Don't allow the player to click to exit the menu, like normal.
    #     """
    #     return None
    def ev_mousebutton(
        self, event: str
    ) -> Optional[ActionOrHandler]:
        """
        Don't allow the player to click to exit the menu, like normal.
        """
        return None


class ItemLabel(Label):
    pass


class InventoryEventHandler(AskUserEventHandler):
    """This handler lets the user select an item.

    What happens then depends on the subclass.
    """

    TITLE = "<missing title>"
    MENU_WIDTH = 200
    MENU_ITEM_HEIGHT = 50

    def __on_exit__(self, root_widget: Widget) -> None:
        self.engine.graphics_component.exit_inventory_screen(root_widget)

    def __on_enter__(self, root_widget: Widget) -> None:
        # root_widget.add_widget(self.menu)
        self.engine.graphics_component.create_inventory_screen(root_widget,
                                                               entity=self.engine.player
                                                               )

    def on_render(self, root_widget: Widget, dt: float) -> None:
        """Render an inventory menu, which displays the items in the inventory, and the letter to select them.
        Will move to a different position based on where the player is located, so the player can always see where
        they are.
        """
        super().on_render(root_widget, dt)

    def ev_keydown(self, event: str) -> Optional[ActionOrHandler]:
        player = self.engine.player
        index = keyboard_inputs[event] - 97
        if 0 <= index <= 26:
            try:
                selected_item = player.inventory.items[index]
            except IndexError:
                self.engine.message_log.add_message("Invalid entry.", color.invalid)
                return None
            return self.on_item_selected(selected_item)
        return super().ev_keydown(event)

    def ev_mousebutton(self, event: str) -> Optional[ActionOrHandler]:
        pass

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        """Called when the user selects a valid item."""
        raise NotImplementedError()


class InventoryActivateHandler(InventoryEventHandler):
    """Handle using an inventory item."""

    TITLE = "Select an item to use"

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        if item.consumable:
            # Return the action for the selected item.
            return item.consumable.get_action(self.engine.player)
        elif item.equippable:
            return actions.EquipAction(self.engine.player, item)
        else:
            return None


class InventoryDropHandler(InventoryEventHandler):
    """Handle dropping an inventory item."""

    TITLE = "Select an item to drop"

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        """Drop this item."""
        return actions.DropItem(self.engine.player, item)


class InventoryViewerHandler(InventoryEventHandler):
    """Allow viewing of items only"""

    TITLE = "Your items you collected until you perished ..."

    def ev_keydown(self, event: str) -> Optional[ActionOrHandler]:
        """Do nothing to this item"""
        return GameOverEventHandler(self.engine)

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        """Do nothing to this item"""
        return GameOverEventHandler(self.engine)

    def ev_mousebutton(
        self, event: str
    ) -> Optional[ActionOrHandler]:
        """Do nothing to this item"""
        return GameOverEventHandler(self.engine)


class SelectIndexHandler(AskUserEventHandler):
    """Handles asking the user for an index on the map."""
    layout: FloatLayout = None
    LINE_WIDTH: int = 2

    def __on_enter__(self, root_widget: Widget) -> None:
        """Sets the cursor to the player when this handler is constructed"""
        self.layout = FloatLayout(size_hint=(1, 1), pos_hint={"center_x": 0.5, "center_y": 0.5})
        root_widget.add_widget(self.layout)
        with self.layout.canvas:
            Color(1, 0, 0, 1.0)
            self.rect = Line(rectangle=[50, 50, 50, 50], width=self.LINE_WIDTH)

    def __on_exit__(self, root_widget: Widget) -> None:
        root_widget.remove_widget(self.layout)

    # def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
    #     """Check for key movement or confirmation keys."""
    #     key = event.sym
    #     if key in MOVE_KEYS:
    #         modifier = 1  # Holding modifier keys will speed up key movement.
    #         if event.mod & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
    #             modifier *= 5
    #         if event.mod & (tcod.event.KMOD_LCTRL | tcod.event.KMOD_RCTRL):
    #             modifier *= 10
    #         if event.mod & (tcod.event.KMOD_LALT | tcod.event.KMOD_RALT):
    #             modifier *= 20
    #
    #         x, y = self.engine.get_mouse_location()
    #         dx, dy = MOVE_KEYS[key]
    #         x += dx * modifier
    #         y += dy * modifier
    #         # Clamp the cursor index to the map size.
    #         x = max(0, min(x, self.engine.game_map.width - 1))
    #         y = max(0, min(y, self.engine.game_map.height - 1))
    #         self.engine.update_mouse_location(x, y)
    #         return None
    #     elif key in CONFIRM_KEYS:
    #         return self.on_index_selected(*self.engine.mouse_location)
    #     return super().ev_keydown(event)

    def ev_keydown(self, event: str) -> Optional[ActionOrHandler]:
        """Check for key movement or confirmation keys."""
        key = event
        if key in MOVE_KEYS:
            modifier = 1  # Holding modifier keys will speed up key movement.
            # if event.mod & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
            #     modifier *= 5
            # if event.mod & (tcod.event.KMOD_LCTRL | tcod.event.KMOD_RCTRL):
            #     modifier *= 10
            # if event.mod & (tcod.event.KMOD_LALT | tcod.event.KMOD_RALT):
            #     modifier *= 20

            x, y = self.engine.get_mouse_location()
            dx, dy = MOVE_KEYS[key]
            x += dx * modifier
            y += dy * modifier
            # Clamp the cursor index to the map size.
            x = max(0, min(x, self.engine.game_map.width - 1))
            y = max(0, min(y, self.engine.game_map.height - 1))
            self.engine.update_mouse_location(x, y)
            return None
        elif key in CONFIRM_KEYS:
            return self.on_index_selected(*self.engine.mouse_location)
        return super().ev_keydown(event)

    # def ev_mousebuttondown(
    #     self, event: tcod.event.MouseButtonDown
    # ) -> Optional[ActionOrHandler]:
    #     """Left click confirms a selection."""
    #     if self.engine.game_map.in_bounds(*event.tile):
    #         if event.button == 1:
    #             # return self.on_index_selected(*event.tile)
    #             return self.on_index_selected(*self.engine.get_map_location())
    #     return super().ev_mousebuttondown(event)

    def ev_mousebutton(
        self, event: str
    ) -> Optional[ActionOrHandler]:
        # print(f"{self.__class__}.ev_mousebutton event:{event}")
        """Left click confirms a selection."""
        if self.engine.game_map.in_bounds(*self.engine.get_mouse_location()):
        # if self.engine.game_map.in_bounds(*event.tile):
            if event == "left":
                # return self.on_index_selected(*event.tile)
                return self.on_index_selected(*self.engine.get_map_location())
        return super().ev_mousebutton(event)

    def on_index_selected(self, x: int, y: int) -> Optional[ActionOrHandler]:
        """Called when an index is selected."""
        raise NotImplementedError()


class LookHandler(SelectIndexHandler):
    """Lets the player look around using the keyboard."""

    def __on_enter__(self, root_widget: Widget) -> None:
        self.engine.update_temp_location(self.engine.player.x, self.engine.player.y)

    def __on_exit__(self, root_widget: Widget) -> None:
        self.engine.disable_temp_location()

    # def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
    #     """Check for key movement or confirmation keys."""
    #     key = event.sym
    #     if key in MOVE_KEYS:
    #         modifier = 1  # Holding modifier keys will speed up key movement.
    #         if event.mod & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
    #             modifier *= 5
    #         if event.mod & (tcod.event.KMOD_LCTRL | tcod.event.KMOD_RCTRL):
    #             modifier *= 10
    #         if event.mod & (tcod.event.KMOD_LALT | tcod.event.KMOD_RALT):
    #             modifier *= 20
    #
    #         x, y = self.engine.get_temp_location()
    #         dx, dy = MOVE_KEYS[key]
    #         x += dx * modifier
    #         y += dy * modifier
    #         # Clamp the cursor index to the map size.
    #         x = max(0, min(x, self.engine.game_map.width - 1))
    #         y = max(0, min(y, self.engine.game_map.height - 1))
    #         self.engine.update_temp_location(x, y)
    #         return None
    #
    #     return super().ev_keydown(event)

    def ev_keydown(self, event: str) -> Optional[ActionOrHandler]:
        """Check for key movement or confirmation keys."""
        key = event
        if key in MOVE_KEYS:
            modifier = 1  # Holding modifier keys will speed up key movement.
            # if event.mod & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
            #     modifier *= 5
            # if event.mod & (tcod.event.KMOD_LCTRL | tcod.event.KMOD_RCTRL):
            #     modifier *= 10
            # if event.mod & (tcod.event.KMOD_LALT | tcod.event.KMOD_RALT):
            #     modifier *= 20

            x, y = self.engine.get_temp_location()
            dx, dy = MOVE_KEYS[key]
            x += dx * modifier
            y += dy * modifier
            # Clamp the cursor index to the map size.
            x = max(0, min(x, self.engine.game_map.width - 1))
            y = max(0, min(y, self.engine.game_map.height - 1))
            self.engine.update_temp_location(x, y)
            return None

        return super().ev_keydown(event)

    def on_index_selected(self, x: int, y: int) -> MainGameEventHandler:
        """Return to main handler."""
        return MainGameEventHandler(self.engine)


class SingleRangedAttackHandler(SelectIndexHandler):
    """Handles targeting a single enemy. Only the enemy selected will be affected."""

    def __init__(
        self, engine: Engine, callback: Callable[[Tuple[int, int]], Optional[Action]]
    ):
        super().__init__(engine)
        self.callback = callback

    def on_render(self, root_widget: Widget, dt: float) -> None:
        super().on_render(root_widget, dt)
        x, y = self.engine.get_mouse_location()

        # Ensure within boundaries
        x_game_window_min = 0
        x_game_window_max = 19
        y_game_window_min = 4
        y_game_window_max = 23
        x = max(x_game_window_min, min(x, x_game_window_max))
        y = max(y_game_window_min, min(y, y_game_window_max))

        tile_size = 32
        self.rect.rectangle = [x * tile_size + (self.LINE_WIDTH//2),
                               y * tile_size - (tile_size//2) + tile_size,
                               tile_size - self.LINE_WIDTH - (self.LINE_WIDTH//2),
                               tile_size - self.LINE_WIDTH - self.LINE_WIDTH]

    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        return self.callback((x, y))


class AreaRangedAttackHandler(SelectIndexHandler):
    """Handles targeting an area within a given radius. Any entity within the area will be affected."""

    def __init__(
        self,
        engine: Engine,
        radius: int,
        callback: Callable[[Tuple[int, int]], Optional[Action]],
    ):
        super().__init__(engine)

        self.radius = radius
        self.callback = callback

    def on_render(self, root_widget: Widget, dt: float) -> None:
        """Highlight the tile under the cursor."""
        # print("AreaRangedAttackerHandler.on_render")
        # print("radius : ", self.radius)
        super().on_render(root_widget, dt)
        x, y = self.engine.get_mouse_location()

        # Ensure within boundaries
        x_game_window_min = 0 + self.radius
        x_game_window_max = 18
        y_game_window_min = 3 + self.radius
        y_game_window_max = 21
        x = max(x_game_window_min, min(x, x_game_window_max))
        y = max(y_game_window_min, min(y, y_game_window_max))

        tile_size = 32
        self.rect.rectangle = [x * tile_size + (self.LINE_WIDTH//2) - (self.radius * tile_size),
                               y * tile_size + (tile_size // 2) - (self.radius * tile_size),
                               (tile_size * (self.radius * 2)) + tile_size - self.LINE_WIDTH - (self.LINE_WIDTH//2),
                               (tile_size * (self.radius * 2)) + tile_size - self.LINE_WIDTH - self.LINE_WIDTH]

    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        return self.callback((x, y))


class MainGameEventHandler(EventHandler):
    def __on_enter__(self, root_widget: Widget) -> None:
        # Check if GUI is Currently Added
        self.engine.add_graphics_component(root_widget)

    def ev_keydown(self, event: str) -> Optional[ActionOrHandler]:
        action: Optional[Action] = None

        key = event
        modifier = event

        player = self.engine.player

        # if key == tcod.event.K_PERIOD and modifier & (
        #     tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT
        # ):
        if key == "spacebar":
            return actions.CheatTakeStairsAction(player)
            # return actions.TakeStairsAction(player)
        if key == "numpad0":
            return actions.KillAllAction(player)

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = BumpAction(player, dx, dy)
        elif key in WAIT_KEYS:
            action = WaitAction(player)

        elif key == "escape":
            raise SystemExit()
        elif key == "v":
            return HistoryViewer(self.engine)

        elif key == "g":
            action = PickupAction(player)

        elif key == "i":
            return InventoryActivateHandler(self.engine)
        elif key == "d":
            return InventoryDropHandler(self.engine)
        elif key == "c":
            return CharacterScreenEventHandler(self.engine)
        elif key == "/":
            return LookHandler(self.engine)

        # No valid key was pressed
        return action

    def ev_mousebutton(self, event: str) -> Optional[BaseEventHandler]:
        # print(f"mouse click at event:{event}")
        return None


class GameOverEventHandler(EventHandler):

    def on_quit(self) -> None:
        """Handle exiting out of a finished game."""
        if os.path.exists("savegame.sav"):
            os.remove("savegame.sav")  # Deletes the active save file.
        raise exceptions.QuitWithoutSaving()  # Avoid saving a finished game.

    def ev_quit(self, event: tcod.event.Quit) -> None:
        self.on_quit()

    def ev_keydown(self, event: str) -> Optional[ActionOrHandler]:
        """Allow to view items, stats, map and log"""
        key = event

        if key == "escape":
            self.on_quit()
        elif key == "v":
            return HistoryViewer(self.engine)
        elif key == "i":
            return InventoryViewerHandler(self.engine)
        elif key == "/":
            return LookHandler(self.engine)

    def ev_mousebutton(self, event: str) -> Optional[BaseEventHandler]:
        # Mouse Clicks do Not Activate Anything on Game Window
        return None


# CURSOR_Y_KEYS = {
#     tcod.event.K_UP: -1,
#     tcod.event.K_DOWN: 1,
#     tcod.event.K_PAGEUP: -10,
#     tcod.event.K_PAGEDOWN: 10,
# }

CURSOR_Y_KEYS = {
    "up": -1,
    "down": 1,
    "pageup": -10,
    "pagedown": 10,
}


class HistoryViewer(EventHandler):
    """Print the history on a larger window which can be navigated."""
    menu = None
    bg = None
    cursor_rect = None
    title = "┤Message history├"
    MENU_WIDTH = 400
    MENU_HEIGHT = 500

    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.log_length = len(engine.message_log.messages)
        self.cursor = self.log_length - 1

    def __on_enter__(self, root_widget: Widget) -> None:
        self.engine.graphics_component.enable_history_view()

    def __on_exit__(self, root_widget: Widget) -> None:
        self.engine.graphics_component.disable_history_view()

    def on_render(self, root_widget: Widget, dt: float) -> None:
        super().on_render(root_widget, dt)  # Draw the main state as the background.

    # def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[GameOverEventHandler, MainGameEventHandler]:
    #     # Fancy conditional movement to make it feel right.
    #     if event.sym in CURSOR_Y_KEYS:
    #         adjust = CURSOR_Y_KEYS[event.sym]
    #         if adjust < 0 and self.cursor == 0:
    #             # Only move from the top to the bottom when you're on the edge.
    #             self.cursor = self.log_length - 1
    #         elif adjust > 0 and self.cursor == self.log_length - 1:
    #             # Same with bottom to top movement.
    #             self.cursor = 0
    #         else:
    #             # Otherwise move while staying clamped to the bounds of the history log.
    #             self.cursor = max(0, min(self.cursor + adjust, self.log_length - 1))
    #     elif event.sym == tcod.event.K_HOME:
    #         self.cursor = 0  # Move directly to the top message.
    #     elif event.sym == tcod.event.K_END:
    #         self.cursor = self.log_length - 1  # Move directly to the last message.
    #     else:  # Any other key moves back to the main game state.
    #         if self.engine.player.is_alive:
    #             return MainGameEventHandler(self.engine)
    #         else:
    #             return GameOverEventHandler(self.engine)
    #     return None

    def ev_keydown(self, event: str) -> Optional[GameOverEventHandler, MainGameEventHandler]:
        # Fancy conditional movement to make it feel right.
        if event in CURSOR_Y_KEYS:
            adjust = CURSOR_Y_KEYS[event]
            if adjust < 0 and self.cursor == 0:
                # Only move from the top to the bottom when you're on the edge.
                self.cursor = self.log_length - 1
            elif adjust > 0 and self.cursor == self.log_length - 1:
                # Same with bottom to top movement.
                self.cursor = 0
            else:
                # Otherwise move while staying clamped to the bounds of the history log.
                self.cursor = max(0, min(self.cursor + adjust, self.log_length - 1))
        elif event == "home":
            self.cursor = 0  # Move directly to the top message.
        elif event == "end":
            self.cursor = self.log_length - 1  # Move directly to the last message.
        else:  # Any other key moves back to the main game state.
            if self.engine.player.is_alive:
                return MainGameEventHandler(self.engine)
            else:
                return GameOverEventHandler(self.engine)
        return None

    def ev_mousebutton(self, event: str) -> Optional[BaseEventHandler]:
        # Might be Able to Click on Messages
        return None
