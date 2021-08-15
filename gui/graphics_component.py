"""
graphics_component.py
Main GUI component. Will store all needed graphics components and is central location for updating them.
"""
from typing import Callable, Dict, List, Tuple

from kivy.graphics.texture import Texture
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget

from gui.bottom_pane_gui import BottomPaneGUI
from gui.game_window import GameWindow
from gui import grid_menu
from gui.side_pane_gui import SidePaneGUI
from gui import graphics_loader

from entity import Actor, Item


class GraphicsFrame(FloatLayout):
    view_mode: int = 0  # used to debugging such as extra information or removing FOW
    game_window: GameWindow = None
    bottom_pane_gui: BottomPaneGUI = None
    side_pane_gui: SidePaneGUI = None
    inventory_screen: grid_menu.GridMenuWithTitle = None

    ACTIVATED_HEIGHT: int = 600

    def __init__(self, engine, **kwargs):
        super(GraphicsFrame, self).__init__(**kwargs)

        # Store all files in "./assets/assets" folder
        self.tile_tex_dict: Dict[str, Texture] = graphics_loader.populate_palette()
        self.tile_tex_dict.update(graphics_loader.assemble_textures())
        self.tex_count_dict: Dict[str, int] = graphics_loader.count_textures()
        # for key, value in self.tex_count_dict.items():
        #     print(key, value)

        self.game_window = GameWindow(engine)
        self.add_widget(self.game_window)

        self.bottom_pane_gui = BottomPaneGUI(engine)
        self.add_widget(self.bottom_pane_gui)

        self.side_pane_gui = SidePaneGUI(engine)
        self.add_widget(self.side_pane_gui)

    def enable_history_view(self) -> None:
        self.bottom_pane_gui.height = self.ACTIVATED_HEIGHT

    def disable_history_view(self) -> None:
        self.bottom_pane_gui.height = 100

    def render(self, root_widget: Widget, dt: float) -> None:
        for child in self.children:
            child.render(dt, root_widget, view_mode=self.view_mode)

    def dissolve(self, root_widget) -> None:
        # De-couple graphic component from root_widget
        root_widget.remove(self)

    def exit_inventory_screen(self,
                              root_widget: Widget,
                              ) -> None:
        self.remove_widget(self.inventory_screen)
        self.inventory_screen = None

    def create_inventory_screen(self,
                                root_widget: Widget,
                                entity: Actor = None,
                                item_list: List[Tuple[Item, Callable]] = None,
                                ) -> None:
        min_width = grid_menu.ITEM_BOX_SIZE * (grid_menu.MAX_ROW + 2.5)
        min_height = grid_menu.ITEM_BOX_SIZE * (grid_menu.MAX_ITEMS / (grid_menu.MAX_ROW - 2))

        self.inventory_screen = grid_menu.create_grid_menu(root_widget=self,
                                   size=(min_width, min_height),
                                   center=self.game_window.center,
                                   item_list=item_list,
                                   inventory=entity.inventory,
                                   title_text="<Inventory>",
                                   tile_tex_dict=self.tile_tex_dict,
                                   )

    # def on_touch_down(self, touch):
    #     print(f"{self.__class__}.on_touch_down")
    #     super(GraphicsFrame, self).on_touch_down(touch)