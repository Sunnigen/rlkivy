from typing import Tuple

from kivy.uix.label import Label
from kivy.uix.widget import Widget

from gui.menu import Menu


class MenuWithTitle(Menu):
    title_label: Label = None

    def __init__(self, title_text: str = "<NoTitle>", **kwargs):
        super(MenuWithTitle, self).__init__(**kwargs)
        self.create_title_text(title_text)

    def create_title_text(self, text: str):
        self.title_label = Label(text=text, size_hint=(1, 0.15))
        self.title_label.text_size = self.size
        self.title_label.texture_size = self.size
        self.title_label.valign = "middle"
        self.title_label.halign = "center"  # "center"
        self.add_widget(widget=self.title_label, index=len(self.children))  # add widget to top of list


def create_menu_with_title(root_widget: Widget,
                           size: Tuple[int, int],
                           pos: Tuple[int, int],
                           title_text: str,
                           ) -> None:
    list_menu = MenuWithTitle(
        root_widget=root_widget,
        size=size,
        pos=pos,
        title_text=title_text
    )
    root_widget.add_widget(list_menu)


if __name__ == "__main__":

    from kivy.app import App

    from gui.menu import *

    class MenuWithTitleApp(App):
        # For Testing Only
        def build(self):
            layout = FloatLayout()
            min_width = 300
            min_height = 150

            create_menu_with_title(root_widget=layout,
                                   size=(min_width, min_height),
                                   pos=(uniform(0, Window.width - min_width),
                                        uniform(0, Window.height - min_height)),

                                   title_text="<Title!>",
                                   )
            return layout

    MenuWithTitleApp().run()