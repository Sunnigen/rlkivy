from typing import Tuple

from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from game_map import GameMap
import globals


Builder.load_string("""
<SidePaneGUI>:
    _dungeon_level_label: dungeon_level_label
    _hp_bar: hp_bar
    _xp_bar: xp_bar
    _stats_label: stats_label
    _target_label: target_label
    pos_hint: {"right": 1, "top": 1}
    size_hint: None, None
    size: 250, 640
    
    canvas:
        Color:
            rgba: 0.196, 0.196, 0.196, 1.0
        Rectangle:
            size: root.size
            pos: root.pos
            
    Label:
        id:  dungeon_level_label
        size_hint: 1, None
        height: 30
        pos: root.x, root.top - self.height
        text: "<Empty>"
        
    HPBar:
        id: hp_bar
        size_hint :1, None
        height: 30
        pos: root.x, root.top - (self.height * 2)
        
    XPBar:
        id: xp_bar
        size_hint :1, None
        height: 30
        pos: root.x, root.top - (self.height * 3)
        
    StatsLabel:
        id: stats_label
        size_hint :1, None
        height: 70
        pos: root.x, root.top - (self.height * 2)
        
    TargetLabel:
        id: target_label
        size_hint: 1, None
        height: 30
        pos: root.x, root.y
""")


class Bar(Label):
    """
    Bar

    General class for horizontal bars for denoting stats
    """
    under_highlight: Rectangle = None
    over_highlight: Rectangle = None

    def __init__(self,
                 under_rgb: Tuple[float, float, float],
                 over_rgb: Tuple[float, float, float],
                 **kwargs):
        super(Bar, self).__init__(**kwargs)

        with self.canvas.before:
            Color(under_rgb[0], under_rgb[1], under_rgb[2], 1)
            self.under_highlight = Rectangle(pos=self.pos, size=self.size)
            Color(over_rgb[0], over_rgb[1], over_rgb[2], 1)
            self.over_highlight = Rectangle(pos=self.pos, size=self.size)

    def update(self,
               root_widget: Widget
               ) -> None:
        raise NotImplementedError

    def update_bar(self, width: float, height: float, percentage: float) -> None:
        self.under_highlight.size = width, height
        self.under_highlight.pos = self.pos
        self.over_highlight.size = width * percentage, height
        self.over_highlight.pos = self.pos


class HPBar(Bar):

    def __init__(self, **kwargs):
        under_rgb = (0.5, 0.0, 0.0)
        over_rgb = (0.0, 0.5, 0.0)
        super(HPBar, self).__init__(under_rgb, over_rgb, **kwargs)

    def update(self, root_widget):
        curr_hp = self.parent.engine.player.fighter.hp
        max_hp = self.parent.engine.player.fighter.max_hp

        self.text = f"HP: {curr_hp} / {max_hp}"

        percentage = curr_hp / max_hp
        width, height = self.size
        self.update_bar(width, height, percentage)


class XPBar(Bar):

    def __init__(self, **kwargs):
        under_rgb = (0.0, 0.0, 0.0)
        over_rgb = (0.5, 0.5, 0.0)
        super(XPBar, self).__init__(under_rgb, over_rgb, **kwargs)

    def update(self, root_widget):
        curr_xp = self.parent.engine.player.level.current_xp
        next_level_xp = self.parent.engine.player.level.experience_to_next_level

        self.text = f"XP: {curr_xp} / {next_level_xp}"

        percentage = curr_xp / next_level_xp
        width, height = self.size
        self.update_bar(width, height, percentage)


class StatsLabel(Label):

    def update(self, root_widget):
        self.text_size = self.size
        self.halign = "left"
        player_fighter = self.parent.engine.player.fighter
        t = f"Attack : {player_fighter.power}\nDefense : {player_fighter.defense}"
        self.text = t


def get_names_at_location(x: int,y: int, game_map: GameMap) -> str:
    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return ""

    names = ", ".join(
        entity.name for entity in game_map.entities if entity.x == x and entity.y == y
    )

    return names.capitalize()


class TargetLabel(Label):

    def update(self, root_widget):
        engine = self.parent.engine
        mouse_x, mouse_y = engine.get_map_location()
        names_at_mouse_location = get_names_at_location(
            x=mouse_x, y=mouse_y, game_map=engine.game_map
        )
        self.text = f"({mouse_x}, {mouse_y})"
        if names_at_mouse_location:
            self.text += " " + names_at_mouse_location


class SidePaneGUI(FloatLayout):
    _dungeon_level_label = ObjectProperty(None)
    _hp_bar = ObjectProperty(None)
    _xp_bar = ObjectProperty(None)
    _stats_label = ObjectProperty(None)
    _target_label = ObjectProperty(None)

    engine = None

    def __init__(self, engine, **kwargs):
        super(SidePaneGUI, self).__init__(**kwargs)
        self.engine = engine

    def render(self, dt: float, root_widget: Widget, view_mode: int):
        # self._dungeon_level_label.text = f"Dungeon Level: {self.engine.game_world.current_floor}"
        self._dungeon_level_label.text = f"Dungeon Level: {self.engine.game_world.current_floor}\nSeed: {globals.SEED_NUMBER}"
        self._hp_bar.update(root_widget)
        self._xp_bar.update(root_widget)
        self._stats_label.update(root_widget)
        self._target_label.update(root_widget)
