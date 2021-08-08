from typing import Dict

from kivy.app import App

from kivy.core.window import Window
from kivy.event import EventDispatcher


keyboard_inputs = {
    # specials keys from kivy.core.window.__init__.py
    'backspace': 8, 'tab': 9, 'enter': 13, 'rshift': 303, 'shift': 304,
    'alt': 308, 'rctrl': 306, 'lctrl': 305,
    'super': 309, 'alt-gr': 307, 'compose': 311, 'pipe': 310,
    'capslock': 301, 'escape': 27, 'spacebar': 32, 'pageup': 280,
    'pagedown': 281, 'end': 279, 'home': 278, 'left': 276, 'up':
        273, 'right': 275, 'down': 274, 'insert': 277, 'delete': 127,
    'numlock': 300, 'print': 144, 'screenlock': 145, 'pause': 19,

    # a-z keys
    'a': 97, 'b': 98, 'c': 99, 'd': 100, 'e': 101, 'f': 102, 'g': 103,
    'h': 104, 'i': 105, 'j': 106, 'k': 107, 'l': 108, 'm': 109, 'n': 110,
    'o': 111, 'p': 112, 'q': 113, 'r': 114, 's': 115, 't': 116, 'u': 117,
    'v': 118, 'w': 119, 'x': 120, 'y': 121, 'z': 122,

    # 0-9 keys
    '0': 48, '1': 49, '2': 50, '3': 51, '4': 52,
    '5': 53, '6': 54, '7': 55, '8': 56, '9': 57,

    # numpad
    'numpad0': 256, 'numpad1': 257, 'numpad2': 258, 'numpad3': 259,
    'numpad4': 260, 'numpad5': 261, 'numpad6': 262, 'numpad7': 263,
    'numpad8': 264, 'numpad9': 265, 'numpaddecimal': 266,
    'numpaddivide': 267, 'numpadmul': 268, 'numpadsubstract': 269,
    'numpadadd': 270, 'numpadenter': 271,

    # F1-15
    'f1': 282, 'f2': 283, 'f3': 284, 'f4': 285, 'f5': 286, 'f6': 287,
    'f7': 288, 'f8': 289, 'f9': 290, 'f10': 291, 'f11': 292, 'f12': 293,
    'f13': 294, 'f14': 295, 'f15': 296,

    # other keys
    '(': 40, ')': 41,
    '[': 91, ']': 93,
    '{': 123, '}': 125,
    ':': 58, ';': 59,
    '=': 61, '+': 43,
    '-': 45, '_': 95,
    '/': 47, '*': 42,
    '?': 47,
    '`': 96, '~': 126,
    '´': 180, '¦': 166,
    '\\': 92, '|': 124,
    '"': 34, "'": 39,
    ',': 44, '.': 46,
    '<': 60, '>': 62,
    '@': 64, '!': 33,
    '#': 35, '$': 36,
    '%': 37, '^': 94,
    '&': 38, '¬': 172,
    '¨': 168, '…': 8230,
    'ù': 249, 'à': 224,
    'é': 233, 'è': 232,
}


class KeyboardListener(EventDispatcher):
    def __init__(self, **kwargs):
        super(KeyboardListener, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text'
        )

        self.keycode_inputs: Dict[str, bool] = {keycode_str: False for keycode_str in keyboard_inputs.values()}
        # self.keycode_inputs: Dict[int, bool] = {keycode_int: False for keycode_int in keyboard_inputs.keys()}
        self._keyboard.bind(on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up)

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down,
                              on_key_up=self._on_keyboard_up
                              )
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # print('The key', keycode, 'have been pressed')
        # print(' - text is %r' % text)
        # print(' - modifiers are %r' % modifiers)

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        # if keycode[1] == 'escape':
        #     keyboard.release()
        self.keycode_inputs[keycode[1]] = True

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        self.keycode_inputs[keycode[1]] = False
        return True


class TestHandler(KeyboardListener):
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print(f"{self.__class__} key down", keycode)
        return super(TestHandler, self)._on_keyboard_down(keyboard, keycode, text, modifiers)

    def _on_keyboard_up(self, keyboard, keycode):
        print(f"{self.__class__} key up", keycode)
        return super(TestHandler, self)._on_keyboard_up(keyboard, keycode)


if __name__ == "__main__":
    from kivy.clock import Clock
    from kivy.uix.label import Label


    class KeyboardLabel(Label):
        def __init__(self, **kwargs):
            super(KeyboardLabel, self).__init__(**kwargs)
            self.text_size = self.size
            self.halign = "center"
            self.valign = "middle"
            self.event_listener = TestHandler()
            Clock.schedule_interval(self.update_text, 60 ** -1)

        def update_text(self, dt: float):
            self.text = "\n".join([f"{key}" for key, val in self.event_listener.keycode_inputs.items() if val])


    class KeyboardApp(App):
        def build(self):
            return KeyboardLabel()

    KeyboardApp().run()
