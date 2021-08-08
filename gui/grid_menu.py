from functools import partial
from typing import Callable, Dict, List, Tuple

from random import uniform

from kivy.clock import Clock
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget

from components.inventory import Inventory
from entity import Item

from gui.menu_with_title import MenuWithTitle
from gui.menu import Menu

MAX_ROW = 6
ITEM_BOX_SIZE = 48
MAX_ITEMS = 24
TEXTURES = None


def empty_func(*args, **kwargs) -> None:
    print("No action assigned!")


class ItemBox(Menu):
    rect: Rectangle = None
    equip_label: Label = None
    letter_label: Label = None
    item_name: str = ""  # name of item to search in textures
    box_letter: str = ""  # letter of box, meant for keyboard notation
    function: Callable = None  # function to carry out when selected via touch or mouse
    offset: int = 10   # pixel offset from edge of item frame graphic

    def __init__(self,
                 function: Callable,
                 item_name: str,
                 box_letter: str = "",
                 equipped: bool = False,
                 **kwargs
                 ):
        super(ItemBox, self).__init__(**kwargs)
        self.size = (ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        self.function = function
        self.item_name = item_name
        self.box_letter = ""  # designation for box
        if box_letter:
            self.box_letter = box_letter
        if self.item_name:
            self.display_item(equipped)

    def display_item(self, equipped: bool):
        try:
            texture_dict = self.root_widget.tile_tex_dict
        except:
            texture_dict = TEXTURES

        with self.canvas:
            width, height = self.size
            x, y = self.pos
            self.rect = Rectangle(texture=texture_dict.get(self.item_name),
                                  size=(width - self.offset, height - self.offset),
                                  pos=(x+self.offset//2, y+self.offset//2),
                                  )

        self.letter_label = Label(
                               pos_hint={"center_x": 0.70},
                               y=self.y,
                               font_size=12,
                               text=f"{self.box_letter})",
                               size_hint=(None, None),
                               size=(25, 25),
                               color=(1, 1, 1, 1),
                               )
        self.add_widget(self.letter_label)
        if equipped:
            self.equip_label = Label(
                               pos_hint={"center_x": 0.32},
                               font_size=10,
                               text="(E)",
                               size_hint=(None, None),
                               size=(25, 25),
                               color=(1, 1, 1, 1),
                               )
            self.add_widget(self.equip_label)

    def render(self, dt: float, root_widget: Widget):

        if self.item_name:
            x, y = self.pos
            self.rect.pos = x+self.offset//2, y+self.offset//2

        if self.letter_label:
            self.letter_label.y = self.y + ITEM_BOX_SIZE/1.7

        if self.equip_label:
            self.equip_label.y = self.y

        # Update Item Frame
        super(ItemBox, self).render(dt, root_widget)

    def on_touch_down(self, touch):
        # If Selected, activate attached option
        if self.collide_point(*touch):
            if self.function:
                self.function()
            return True
        return super().on_touch_down(touch)


class GridMenuWithTitle(MenuWithTitle):
    grid: GridLayout = None

    def __init__(self,
                 item_list: List[Tuple[Item, Callable]] = None,
                 inventory: Inventory = None,
                 tile_tex_dict: Dict[str, Texture] = None,
                 **kwargs
                 ):
        super(GridMenuWithTitle, self).__init__(**kwargs)
        self.item_list: List[Tuple[Item, Callable]] = item_list
        self.inventory: Inventory = inventory
        self.item_count: int = 24
        self.tile_tex_dict: Dict[str, Texture] = tile_tex_dict

        # Accept an Inventory Object or List of Item Objects
        if self.inventory:
            self.grid = self.create_inventory_layout()
        elif self.item_list:
            self.grid = self.create_item_list_layout()
        else:
            #  No Inventory Or Item List Given
            self.grid = self.create_empty_inventory_layout()
        self.add_widget(self.grid)
        # Clock.schedule_interval(self.update, 60 ** -1)

    def create_inventory_layout(self) -> GridLayout:
        grid = GridLayout(cols=MAX_ROW, size_hint=(1, 1))

        # Display Each Item in Given Inventory
        entity = self.inventory.parent
        self.item_list = self.inventory.items

        for i in range(MAX_ITEMS):
            try:
                item = self.item_list[i]
                item_name = item.name2

                item_function = partial(select_item, item.name, self.root_widget)
                is_equipped = entity.equipment.item_is_equipped(item)
                item_box = self.create_item_box(
                    item_name=item_name,
                    function=item_function,
                    equipped=is_equipped,
                    box_letter=chr(i + 97),
                )
            except IndexError:
                item_box = self.create_item_box()

            grid.add_widget(item_box)
        return grid

    def create_item_list_layout(self) -> GridLayout:
        grid = GridLayout(cols=MAX_ROW, size_hint=(1, 1))

        for i in range(self.item_count):
            try:
                item_entity, item_function = self.item_list[i]
                item_box = self.create_item_box(
                    item_name=item_entity.name,
                    function=item_function,
                    box_letter=chr(i + 97),
                )
            except IndexError:
                item_box = self.create_empty_item_box()
            grid.add_widget(item_box)

        return grid

    def create_empty_inventory_layout(self) -> GridLayout:
        grid = GridLayout(cols=MAX_ROW, size_hint=(1, 1))

        for i in range(MAX_ITEMS):
            grid.add_widget(self.create_empty_item_box())

        return grid

    def create_item_box(self,
                        item_name: str = "",
                        function: Callable = None,
                        box_letter: str = "",
                        equipped: bool = False
                        ):
        return ItemBox(root_widget=self,
                       border_image_tex=self.tile_tex_dict.get("item_box_frame"),
                       # border_image_file="../assets/assets/item_box_frame.png",
                       border_tuple=(6, 6, 6, 6),
                       item_name=item_name,
                       function=function,
                       equipped=equipped,
                       box_letter=box_letter,
                       )

    def render(self, dt: float, root_widget: Widget) -> None:
        if self.grid:
            for item_box in self.grid.children:
                item_box.render(dt, root_widget)
        super(GridMenuWithTitle, self).render(dt, root_widget)


def select_item(item: Item, gui_parent: FloatLayout) -> None:
    print(f"{item} has been selected.")
    print(f"{gui_parent} is the parent.")



def create_grid_menu(root_widget: Widget,
                     size: Tuple[int, int],
                     center: Tuple[int, int],
                     title_text: str,
                     item_list: List[Tuple[Item, Callable]] = None,
                     inventory: Inventory = None,
                     tile_tex_dict: Dict[str, Texture] = None,
                     ) -> GridMenuWithTitle:
    grid_menu = GridMenuWithTitle(
        root_widget=root_widget,
        size=size,
        center=center,
        item_list=item_list,
        inventory=inventory,
        title_text=title_text,
        border_image_tex=tile_tex_dict.get("frame_2"),
        tile_tex_dict=tile_tex_dict,
    )
    root_widget.add_widget(grid_menu)
    return grid_menu


if __name__ == "__main__":
    from copy import deepcopy
    from functools import partial
    from random import choice, randint

    from kivy.app import App

    import entity_factories
    from gui.graphics_loader import assemble_textures

    TEXTURES = assemble_textures(directory="../assets/assets")


    class GridMenuApp(App):
        # For Testing Only
        def build(self):
            layout = FloatLayout(center=(300, 300), size_hint=(None, None) )
            # layout = FloatLayout(pos_hint={"center_x": 0.5,"center_y": 0.5}, size_hint=(None, None) )
            min_width = ITEM_BOX_SIZE * (MAX_ROW + 2.5)
            min_height = ITEM_BOX_SIZE * (MAX_ITEMS/(MAX_ROW - 2))
            item_list = []

            possible_items = [
                entity_factories.chain_mail,
                entity_factories.confusion_scroll,
                entity_factories.dagger,
                entity_factories.fireball_scroll,
                entity_factories.health_potion,
                entity_factories.leather_armor,
                entity_factories.lightning_scroll,
                entity_factories.sword,
            ]

            for _ in range(randint(3, MAX_ITEMS)):
                item = deepcopy(choice(possible_items))
                item_list.append((item, partial(select_item, item.name)))

            # Create Test Inventory
            player = deepcopy(entity_factories.player)

            dagger = deepcopy(entity_factories.dagger)
            player.inventory.items.append(dagger)
            player.equipment.toggle_equip(dagger, add_message=False)

            # Item List
            for i in range(randint(3, MAX_ITEMS-1)):
                item_entity = deepcopy(choice(possible_items))
                item_entity.parent = player.inventory
                player.inventory.items.append(item_entity)

            # Create Grid Menu
            create_grid_menu(root_widget=layout,
                             size=(min_width, min_height),
                             center=layout.center,
                             item_list=item_list,
                             inventory=player.inventory,
                             title_text="<Inventory>",
                             tile_tex_dict=TEXTURES,
                             )
            return layout

    GridMenuApp().run()
