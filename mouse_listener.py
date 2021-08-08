from kivy.core.window import Window, WindowBase
from kivy.event import EventDispatcher
from kivy.uix.widget import Widget


class MouseListener(Widget):
    mouse_pos: [float, float]

    def __init__(self, **kwargs):
        super(MouseListener, self).__init__(**kwargs)
        Window.bind(on_close=self.close_function,
                    on_hide=self.hide_function,
                    mouse_pos=self.update_mouse_move,
                    )

    def close_function(self, *args):
        print("close_function", args)

    def hide_function(self, *args):
        print("hide_function", args)

    def update_mouse_move(self, window, mouse_pos):
        self.mouse_pos = mouse_pos


if __name__ == "__main__":
    from kivy.app import App
    from kivy.clock import Clock
    from kivy.uix.label import Label


    class MouseLabel(Label):
        mouse_pos: [float, float] = (0, 0)

        def __init__(self, **kwargs):
            super(MouseLabel, self).__init__(**kwargs)
            self.text_size = self.size
            self.halign = "center"
            self.valign = "middle"
            # self.event_listener = MouseListener()
            Window.bind(mouse_pos=self.set_mouse_move)
            Clock.schedule_interval(self.update_text, 60 ** -1)

        def on_touch_down(self, touch):
            print("on_touch_down", touch, touch.button)

        def set_mouse_move(self, window, mouse_pos):
            self.mouse_pos = mouse_pos

        def update_text(self, dt: float):
            self.text = f"Mouse Position: {self.mouse_pos}"

    class MouseLabelApp(App):
        def build(self):
            # return MouseListener()
            return MouseLabel()


    MouseLabelApp().run()
