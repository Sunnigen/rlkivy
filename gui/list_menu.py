from functools import partial
from string import ascii_letters
from typing import Callable, List, Tuple

from random import choice, randint, uniform

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout

from gui.menu import Menu
from gui.choice_label import TextLabel, LABEL_HEIGHT


class ListMenu(Menu):
    def __init__(self,
                 option_list: List[Tuple[str, Callable]],
                 **kwargs
                 ):
        super(ListMenu, self).__init__(**kwargs)
        self.create_list(option_list)

    def create_list(self, option_list: List[Tuple[str, Callable]]) -> None:
        for label_name, label_function in option_list:
            label = TextLabel(size_hint=(0.8, 1/len(option_list)),
                              function=partial(label_function, label_name),
                              text=label_name)
            self.add_widget(label)


def create_list_menu(root_widget: Widget,
                     size: Tuple[int, int],
                     pos: Tuple[int, int],
                     option_list: List[Tuple[str, Callable]]
                     ) -> None:
    # Ensure Minimum Height
    # menu_height = max(menu_height, MIN_WIDTH + MIN_PADDING)
    list_menu = ListMenu(
        root_widget=root_widget,
        size=size,
        pos=pos,
        option_list=option_list)
    root_widget.add_widget(list_menu)


def no_function(text: str):
    print(f"No function was attached to the menu option: {text}")


def test_function(s: str, *args, **kwargs):
    print(f"Option #{s} selected", args, kwargs)


def generate_random_letters() -> str:
    return "".join([choice(ascii_letters) for i in range(randint(4, 10))])


class ListMenuApp(App):
    # For Testing Only
    def build(self):
        layout = FloatLayout()
        option_count = randint(1, 7)
        option_list = [(generate_random_letters(), partial(test_function, f"{i}")) for i in range(option_count)]
        min_height = max(LABEL_HEIGHT * (len(option_list) + 1), 150)
        create_list_menu(layout,
                         size=(300, min_height),
                         pos=(uniform(0, Window.width-300), uniform(0, Window.height - min_height)),
                         option_list=option_list,
                         )
        return layout


if __name__ == "__main__":
    ListMenuApp().run()
