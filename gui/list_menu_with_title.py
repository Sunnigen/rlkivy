from typing import Callable, List, Tuple

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

from gui.list_menu import ListMenu


class ListMenuWithTitle(ListMenu):
    title_label: Label = None

    def __init__(self, title_text: str = "<NoTitle>", **kwargs):
        super(ListMenuWithTitle, self).__init__(**kwargs)
        self.create_title_text(title_text)

    def create_title_text(self, text: str):
        self.title_label = Label(text=text, size_hint=(1, 0.15))
        self.title_label.text_size = self.size
        self.title_label.texture_size = self.size
        self.title_label.valign = "middle"
        self.title_label.halign = "center"  # "center"
        self.add_widget(widget=self.title_label, index=len(self.children))  # add widget to top of list


def create_list_menu_with_title(root_widget: Widget,
                                size: Tuple[int, int],
                                pos: Tuple[int, int],
                                option_list: List[Tuple[str, Callable]],
                                title_text: str,
                                ) -> None:
    list_menu = ListMenuWithTitle(
        root_widget=root_widget,
        size=size,
        pos=pos,
        option_list=option_list,
        title_text=title_text
    )
    root_widget.add_widget(list_menu)


if __name__ == "__main__":
    from functools import partial
    from random import randint

    from kivy.app import App

    from gui.list_menu import *

    class ListMenuApp(App):
        # For Testing Only
        def build(self):
            layout = FloatLayout()
            min_width = 300
            option_count = randint(1, 7)
            option_list = [(generate_random_letters(), partial(test_function, f"{i}")) for i in range(option_count)]
            min_height = max(LABEL_HEIGHT * (len(option_list) + 1), 150)

            create_list_menu_with_title(root_widget=layout,
                                        size=(min_width, min_height),
                                        pos=(uniform(0, Window.width - min_width),
                                             uniform(0, Window.height - min_height)),
                                        option_list=option_list,
                                        title_text="Select An Option Below:",
                                        )
            return layout

    ListMenuApp().run()