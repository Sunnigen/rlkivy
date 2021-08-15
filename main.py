#!/usr/bin/env python3

import traceback
from typing import Dict, Tuple

import color
import exceptions
import setup_game
import kivy_input_handlers

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout

import globals  # set seed number from beginning

# Set Global Font
Builder.load_string("""
<Widget>:
    font_name: "assets/fonts/whitrabt.ttf"
""")


def save_game(handler: kivy_input_handlers.BaseEventHandler, filename: str) -> None:
    """If the current event handler has an active Engine then save it."""
    if isinstance(handler, kivy_input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved.")


class RoguelikeKivy(FloatLayout):
    handler: kivy_input_handlers.BaseEventHandler = None
    game_loop: Clock = None
    mouse_location: Tuple[float, float] = (0.0, 0.0)

    def __init__(self, **kwargs):
        super(RoguelikeKivy, self).__init__(**kwargs)

        # Initialize Handler
        self.handler = setup_game.MainMenu()
        self.handler.__on_enter__(root_widget=self)
        self.t = 0

        # Set Game Loop
        GAME_SPEED = 60 ** -1
        self.game_loop = Clock.schedule_interval(self.render, GAME_SPEED)
        # self.game_loop = Clock.schedule_interval(self.check_key_press, GAME_SPEED)
        # self.game_loop = Clock.schedule_interval(self.update_kivy, GAME_SPEED)
        self.size_hint = None, None
        self.size = 900, 750
        Window.size = 900, 750
        Window.top = 30  # position of window at top
        Window.bind(mouse_pos=self.update_mouse_pos)
        # self.keycode_inputs: Dict[str, bool] = {keycode_str: False for keycode_str in keyboard_listener.keyboard_inputs.values()}
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down, on_key_up=self.on_keyboard_up)

    def on_touch_down(self, touch):
        # Check for Mouse Clicks
        if touch.button:
            self.update(event=touch.pos, event_type=touch.button)

        super(RoguelikeKivy, self).on_touch_down(touch.pos)

    def _keyboard_closed(self):
        # print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def on_keyboard_up(self, keyboard, keycode):
        # print('The key', keycode, 'have been released')
        # self.keycode_inputs[keycode[1]] = False
        return True

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # print('The key', keycode, 'have been pressed')
        # print(' - text is %r' % text)
        # print(' - modifiers are %r' % modifiers)
        # self.keycode_inputs[keycode[1]] = True
        self.update(keycode[1], "keydown")
        return True

    def update_mouse_pos(self, window, pos) -> None:
        self.mouse_location = pos

    def render(self, dt):
        # Handles all Graphic Updates
        root_widget = self
        self.handler.on_render(root_widget=root_widget, dt=dt)

    def update(self, event: str, event_type: str) -> None:
        root_widget = self
        try:
            new_handler = self.handler.handle_events(event, event_type)
            if not isinstance(new_handler, type(self.handler)) and new_handler:
                self.handler.__on_exit__(root_widget)
                self.handler = new_handler
                self.handler.__on_enter__(root_widget)
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit:  # Save and quit.
            save_game(self.handler, "savegame.sav")
            raise
        # except BaseException:  # Save on any other unexpected exception.
        #     save_game(self.handler, "savegame.sav")
        #     raise
        except Exception:  # Handle exceptions in game.
            traceback.print_exc()  # Print error to stderr.
            # Then print the error to the message log.
            if isinstance(self.handler, kivy_input_handlers.EventHandler):
                self.handler.engine.message_log.add_message(traceback.format_exc(), color.error)


class RoguelikeKivyApp(App):
    def build(self):
        return RoguelikeKivy()


if __name__ == "__main__":
    RoguelikeKivyApp().run()
