from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import BorderImage, Rectangle
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget


class TextLabel(Label):
    def __init__(self, text, **kwargs):
        super(TextLabel, self).__init__(**kwargs)
        self.text = text
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.size_hint = (1, 1)
        self.texture_size = self.size
        self.valign = "middle"
        self.halign = "center"


class Menu(Rectangle):
    def __init__(self, **kwargs):
        pass


class MainScreen(FloatLayout):
    border = None
    label = None

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.label = TextLabel(text="Hello World!")
        self.add_widget(self.label)

        with self.label.canvas.before:
            self.border = BorderImage(
                size=(self.label.width, self.label.height),
                pos=(self.label.x, self.label.y),
                border=(60, 60, 60, 60,),
                # border=(30, 30, 30, 30,),
                # source='assets/assets/frame.png')
                source='assets/assets/frame_2_2.png')
                # source='assets/assets/frame.png')
        Clock.schedule_interval(self.update, 60 ** -1)

    def update(self, dt):
        self.border.size = Window.size
        self.border.pos = (self.label.x, self.label.y)


class MultiMenuApp(App):
    def build(self):
        return MainScreen()


if __name__ == "__main__":
    MultiMenuApp().run()
