from string import digits
from random import choice, randint

from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import Label as CoreLabel
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget


class FloatingText(CoreLabel):
    lifetime = 100
    parent = None
    opacity = 1
    color = None

    def __init__(self, parent, pos, text, color):
        self.parent = parent
        self.pos = pos
        self.color = color
        self.lifetime = randint(2, 7)
        self.y_speed = randint(50, 150)
        if text[1] == "0":
            text = text.replace("0", "", 1)
        super(FloatingText, self).__init__(text=text, font_name="AppleII.ttf")

        i = randint(25, 75)
        self.text_size = (i, i)

    def update(self, dt):
        x, y = self.pos
        self.lifetime -= dt * 8
        self.pos = x, y + dt * self.y_speed
        self.opacity -= dt * 0.5
        # i = randint(25, 75)
        # self.text_size = (i, i)
        # self.refresh()


class FloatTextFrame(Widget):
    text_list = []
    max_count = 250

    def __init__(self, **kwargs):
        super(FloatTextFrame, self).__init__(**kwargs)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.size_hint = 1, 1

        Clock.schedule_interval(self.update_loop, 60 ** -1)

    def update_loop(self, dt):
        # Update Loop for Render
        self.canvas.clear()
        with self.canvas:
            for label in self.text_list:
                label.update(dt)
                Color(label.color[0], label.color[1], label.color[2], label.opacity)
                Rectangle(texture=label.texture, pos=label.pos)

        # Update List of Active CoreLabels
        self.text_list = [label for label in self.text_list if label.lifetime > 0]

        # Check to Generate More Labels
        generation_count = self.max_count - len(self.text_list)
        for i in range(generation_count):
            start_pos = (randint(0, Window.width), randint(-200, Window.height-50))
            self.text_list.append(self.generate_floating_text(start_pos))

    def generate_floating_text(self, pos):
        my_label = FloatingText(self, pos=pos, text="-{} {}".format("".join([choice(digits) for n in range(randint(3,4))]), choice(["damage\n(poison)", "damage\n(fire)", "damage", "damage", "", "", "", "", "", "", "", ""])), color=[randint(0, 255)/255, randint(0, 255)/255, randint(0, 255)/255])
        my_label.refresh()
        return my_label


class FloatingTextApp(App):
    def build(self):
        return FloatTextFrame()


if __name__ == '__main__':
    FloatingTextApp().run()
