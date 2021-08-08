from typing import Optional, Tuple

from random import uniform

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import BorderImage
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget


MIN_WIDTH: int = 150
MIN_PADDING: int = 30


class Menu(BoxLayout):
    # Generic menu class with a background with extra widgets.
    border: BorderImage = None
    padding = [60, 30, 60, 30]

    def __init__(self,
                 root_widget: Widget,
                 border_image_tex: Texture = None,
                 # border_image_file: str = "../assets/assets/frame_2.png",
                 border_tuple: Tuple[int, int, int, int] = (30, 30, 30, 30),
                 orientation: str = "vertical",
                 **kwargs):
        super(Menu, self).__init__(**kwargs)
        self.root_widget: Optional[Widget] = root_widget
        self.orientation = orientation
        self.size_hint = None, None

        # Menu Background
        with self.canvas:
            self.border = BorderImage(
                size=self.size,
                pos=self.pos,
                border=border_tuple,
                texture=border_image_tex)

    @property
    def root_widget(self) -> Widget:
        # print("getter method root_widget")
        return self.__root_widget

    @root_widget.setter
    def root_widget(self, root_widget: Widget):
        self.__root_widget = root_widget

    def on_size(self, *args, **kwargs):
        self.render(0.0, None)

    def on_pos(self, *args, **kwargs):
        self.render(0.0, None)

    def render(self, dt: float, root_widget: Widget):
        # Update Location of Graphics
        if self.border:
            self.border.size = self.size
            self.border.pos = self.x, self.y

    # def update(self, dt):
        # print(f"{self.__class__}.update, {self.border}")
        # self.render()


def create_menu(root_widget: Widget,
                size: Tuple[int, int],
                pos: Tuple[int, int],
                ) -> None:

    menu = Menu(
        root_widget=root_widget,
        size=size,
        pos=pos,
    )
    root_widget.add_widget(menu)


def add_widget_to_menu(root_widget: Widget,
                       widget: Widget,
                       ) -> None:
    # Searches for Menu Object
    for child in root_widget.children:
        if isinstance(child, Menu):
            widget.width = child.width
            child.add_widget(widget)
            return None


if __name__ == "__main__":
    class MenuApp(App):
        # For Testing Only
        def build(self):
            layout = FloatLayout()
            min_width = 300
            min_height = 150
            create_menu(root_widget=layout,
                        size=(min_width, min_height),
                        pos=(uniform(0, Window.width - min_width), uniform(0, Window.height - min_height)),
                        )
            return layout

    MenuApp().run()
