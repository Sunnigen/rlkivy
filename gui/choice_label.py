from typing import Callable
from kivy.uix.label import Label


LABEL_HEIGHT: int = 50


class TextLabel(Label):
    def __init__(self, function: Callable, **kwargs):
        self.function: Callable = function
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.size_hint = None, 1
        self.color = 1, 1, 1, 1
        # self.color = 0, 0, 0, 1
        super(TextLabel, self).__init__(**kwargs)
        self.texture_size = self.size
        self.text_size = self.size
        self.valign = "middle"
        self.halign = "left"  # "center"

    def on_size(self, *args, **kwargs):
        self.texture_size = self.size
        self.text_size = self.size

    def on_touch_down(self, touch):
        # If Label is Selected, activate attached option

        if self.collide_point(*touch.pos):
            self.function()
            return True
        # print("touch at ", touch.pos, " but label at ", self.pos)
        return super().on_touch_down(touch)


if __name__ == "__main__":
    from functools import partial

    from kivy.app import App
    from kivy.uix.floatlayout import FloatLayout

    from gui import menu


    def test_function(s: str):
        print(f"I am pressed : {s}")


    class TestApp(App):
        def build(self):
            root_widget = FloatLayout()
            menu.create_menu(root_widget,
                             size=(300, 150),
                             pos=(100, 100),
                             )

            label = TextLabel(size_hint=(0.8, 0.9),
                              function=partial(test_function, "hello world"),
                              text="hello world!"
                              )
            menu.add_widget_to_menu(root_widget, label)
            return root_widget

    if __name__ == "__main__":
        TestApp().run()
