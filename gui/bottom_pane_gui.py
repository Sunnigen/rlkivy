from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget


Builder.load_string("""
<BottomPaneGUI>:
    orientation: "vertical"
    pos_hint: {"x": 0, "y": 0}
    size_hint: 1, None
    height: 100
    padding: 10
    
    canvas:
        Color:
            rgba: 0.196, 0.196, 0.196, 1.0
        Rectangle:
            pos: root.pos
            size: root.size
""")


class MessageLabel(Label):
    def __init__(self, text: str, **kwargs):
        super(MessageLabel, self).__init__(
            pos_hint={"x": 0, "y": 0},
            size_hint=(1, 1),
            text=text,
            halign="left",
            valign="bottom",
            markup=True,
            **kwargs)

    def update(self) -> None:
        self.text_size = self.size
        self.size = self.texture_size

    def set_text(self, text: str) -> None:
        self.text = text


class MessageLogGUI(BoxLayout):
    message_label = None
    engine = None

    def __init__(self, engine, **kwargs):
        super(MessageLogGUI, self).__init__(**kwargs)
        self.engine = engine
        self.message_label = MessageLabel(text="<empty>")
        self.add_widget(self.message_label)
        self.size_hint = 1, 1

    def render(self, dt: float, root_widget: Widget):
        self.message_label.update()


class BottomPaneGUI(BoxLayout):

    def __init__(self, engine, **kwargs):
        super(BottomPaneGUI, self).__init__(**kwargs)
        self.message_log_gui = MessageLogGUI(engine)
        self.add_widget(self.message_log_gui)

    def render(self, dt: float, root_widget: Widget):
        self.message_log_gui.render(dt, root_widget)
