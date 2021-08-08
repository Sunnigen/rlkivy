from typing import Iterable, List, Reversible, Tuple
import textwrap

from kivy.uix.widget import Widget

import color


class Message:
    def __init__(self, text: str, fg: Tuple[int, int, int]):
        self.plain_text = text
        self.fg = fg
        if self.fg:
            self.markup_color = "%02x%02x%02x" % (fg[0], fg[1], fg[2])
        else:
            self.markup_color = "%02x%02x%02x" % (0, 0, 0)
        self.markup_text = "[color={}]{}[/color]".format(self.markup_color, self.plain_text)
        self.count = 1

    @property
    def full_text(self) -> str:
        """The full text of this message, including the count if necessary."""
        if self.count > 1:
            return f"{self.markup_text} (x{self.count})"
        return self.markup_text

    def __repr__(self):
        return "Message text:{}, markup_color:{}, count:{}, markup_text:{}".format(
            self.plain_text,
            self.fg,
            self.markup_color,
            self.count,
            self.markup_text
        )


class MessageLog:
    def __init__(self) -> None:
        self.messages: List[Message] = []

    def add_message(
        self, text: str, fg: Tuple[int, int, int] = color.white, *, stack: bool = True,
    ) -> None:
        """Add a message to this log.

        `text` is the message text, `fg` is the text color.

        If `stack` is True then the message can stack with a previous message
        of the same text.
        """
        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text, fg))

    def render(
        self, root_widget: Widget, engine, height: int,
    ) -> None:
        """Render this log over the given area.

        `x`, `y`, `width`, `height` is the rectangular region to render onto
        the `console`.
        """
        self.render_messages(root_widget, engine, height, self.messages)

    @staticmethod
    def wrap(string: str, width: int) -> Iterable[str]:
        """Return a wrapped text message."""
        for line in string.splitlines():  # Handle newlines in messages.
            yield from textwrap.wrap(
                line, width, expand_tabs=True,
            )

    @classmethod
    def render_messages(
        cls,
        root_widget: Widget,
        engine,
        height: int,
        messages: Reversible[Message],
    ) -> None:
        """Render the messages provided.

        The `messages` are rendered starting at the last message and working
        backwards.
        """
        max_amount_of_messages = engine.graphics_component.bottom_pane_gui.height // 10
        y_offset = height + 2
        text_to_display = ""

        if len(messages) > max_amount_of_messages:
            _messages = messages[-max_amount_of_messages:]
        else:
            _messages = messages

        for message in _messages:
            for line in list(cls.wrap(message.full_text, 500)):
                text_to_display += "\n" + line
                y_offset -= 1
                if y_offset < 0:
                    break  # No more space to print messages.

        engine.graphics_component.bottom_pane_gui.message_log_gui.message_label.set_text(text=text_to_display)
