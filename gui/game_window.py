from typing import Dict, List, Tuple

from kivy.graphics import Color, Quad, PushMatrix, PopMatrix, Rectangle, Rotate, Translate
from kivy.graphics.texture import Texture
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget

from entity import Direction


class GameWindow(FloatLayout):
    rect_dict: Dict[Tuple[int, int], Rectangle] = {}  # dictionary of all coordinates mapped to tiles
    quad_dict: Dict[Tuple[int, int], Quad] = {}  # dictionary of all coordinates mapped to tile quads
    hue_dict: Dict[Tuple[int, int], Color] = {}  # dictionary of all coordinates mapped to tile hues

    # tiles: Dict[str, Dict[str, Optional[Color, Quad, Rotate, Translate]]] = {}
    rotate_dict: Dict[Tuple[int, int], Rotate] = {}
    translate_dict: Dict[Tuple[int, int], Translate] = {}

    entity_graphics: List[Quad] = []

    tile_tex_dict: Dict[str, Texture] = {}  # dictionary of all tile names and their palettes
    TILE_SIZE = 32
    VIEWPORT_WINDOW = 10

    def __init__(self, engine, **kwargs):
        super(GameWindow, self).__init__(**kwargs)

        self.engine = engine
        self.size_hint = None, None
        self.size = self.TILE_SIZE * self.VIEWPORT_WINDOW * 2, self.TILE_SIZE * self.VIEWPORT_WINDOW * 2
        self.pos_hint = {"x": 0, "top": 1}
        self.initialize_tiles()

    def reset_tiles(self) -> None:
        self.hue_dict = {}
        self.rect_dict = {}
        self.rotate_dict = {}
        self.translate_dict = {}
        self.quad_dict = {}

    def initialize_tiles(self) -> None:
        self.reset_tiles()
        with self.canvas:
            for i in range(self.VIEWPORT_WINDOW * 2):
                for j in range(self.VIEWPORT_WINDOW * 2):
                    self.hue_dict[(i, j)] = Color(1, 1, 1, 1)
                    self.rect_dict[(i, j)] = \
                        Rectangle(size=(self.TILE_SIZE, self.TILE_SIZE),
                                  pos=(self.x + (i * self.TILE_SIZE), self.y + (j * self.TILE_SIZE))
                                  )

    def obtain_viewport_dimensions(self, origin_x: int, origin_y: int) -> Tuple[int, int, int, int]:
        """
        x, y, width, height coordinates of viewport
        :param origin_x:
        :param origin_y:
        :return: x_lower, x_upper, y_lower, y_upper
        """

        return origin_x - self.VIEWPORT_WINDOW, origin_x + self.VIEWPORT_WINDOW, origin_y - self.VIEWPORT_WINDOW, \
               origin_y + self.VIEWPORT_WINDOW

    def render(self, dt: float, root_widget: Widget, view_mode: int = 0) -> None:
        # Main Game Window
        self.render_viewport(dt, root_widget, view_mode)

        # Any Overlapping Textboxes or Menus
        for child in self.children:
            child.update(dt)

    def render_viewport(self, dt: float, root_widget: Widget, view_mode: int = 0) -> None:
        # view_mode = 0  # visibility mode for debugging
        player = self.engine.player

        # Obtain Viewport Dimension Coordinates
        center = self.engine.get_temp_location()
        if center:  # center NOT ON PLAYER
            x_lower, x_upper, y_lower, y_upper = self.obtain_viewport_dimensions(*center)
        else:  # center ON PLAYER
            x_lower, x_upper, y_lower, y_upper = self.obtain_viewport_dimensions(player.x, player.y)

        with self.canvas:
            # Render BG tiles
            self.render_tiles(view_mode, x_lower, x_upper, y_lower, y_upper, dt)

            # Render Map Object : Down Stairs
            self.render_map_objects(view_mode, x_lower, x_upper, y_lower, y_upper, dt)

        self.canvas.after.clear()
        with self.canvas.after:
            # Render Entities
            self.render_entities(view_mode, x_lower, x_upper, y_lower, y_upper, dt)

    def render_tiles(self, view_mode: int, x_lower: int, x_upper: int, y_lower: int, y_upper: int, dt: float) -> None:
        for x in range(x_lower, x_upper, 1):
            for y in range(y_lower, y_upper, 1):
                tex = self.parent.tile_tex_dict["blank"]
                hue_tuple = 0.25, 0.25, 0.25, 1.0
                try:
                    z = 1 / (x + abs(x))
                    z = 1 / (y + abs(y))

                    if self.engine.game_map.visible[x][y]:
                        hue_tuple = 1.0, 1.0, 1.0, 1.0
                        if self.engine.game_map.tiles[x][y]["walkable"]:
                            tex = self.parent.tile_tex_dict["floor"]
                        else:
                            tex = self.parent.tile_tex_dict["wall"]

                    elif self.engine.game_map.explored[x][y]:
                        # hue = 0.2, 0.2, 0.2, 1.0
                        if self.engine.game_map.tiles[x][y]["walkable"]:
                            tex = self.parent.tile_tex_dict["floor"]
                        else:
                            tex = self.parent.tile_tex_dict["wall"]

                except ZeroDivisionError:
                    """
                    Ensure that accessing the 2D matrix using negative numbers doesn't access the other end of 
                    2D matrix
                    """
                    pass
                except IndexError:
                    pass

                x_norm = x - x_lower
                y_norm = y - y_lower

                tile = self.rect_dict.get((x_norm, y_norm))
                tile.texture = tex
                tile.pos = self.x + (x_norm * self.TILE_SIZE), self.y + (y_norm * self.TILE_SIZE)

                tile_hue = self.hue_dict.get((x_norm, y_norm))
                tile_hue.rgba = hue_tuple

    def render_map_objects(self, view_mode: int, x_lower: int, x_upper: int, y_lower: int, y_upper: int,
                           dt: float) -> None:
        # Render All Map Objects into Viewport
        # All Objects that are to be rendered ON-TOP of the background tiles
        # For example, stairs, furniture, doodads
        Color(1.0, 1.0, 1.0, 1)
        stair_x, stair_y = self.engine.game_map.downstairs_location
        if self.engine.game_map.visible[stair_x][stair_y] or self.engine.game_map.explored[stair_x][stair_y]:
            x_norm = stair_x - x_lower
            y_norm = stair_y - y_lower
            tile = self.rect_dict.get((x_norm, y_norm))
            try:
                tile.texture = self.parent.tile_tex_dict["stairs"]
                tile.pos = self.x + (x_norm * self.TILE_SIZE), self.y + (y_norm * self.TILE_SIZE)
            except AttributeError:
                pass
                # print("cannot find tile stair tile :(", tile, stair_x, stair_y)

    def remove_entity_graphics(self, dt):
        for entity_graphic in self.entity_graphics:
            self.canvas.remove(entity_graphic)

        self.entity_graphics = []

    def render_entities(self,
                        view_mode: int,
                        x_lower: int,
                        x_upper: int,
                        y_lower: int,
                        y_upper: int,
                        dt: float) -> None:

        # Temporary, Should be Converted to self.quad_dict instead of List
        # self.remove_entity_graphics(dt)
        # print("entities : ", len(self.engine.game_map.entities))

        if view_mode == 1:  # render all entities within viewport
            entities_sorted_for_rendering = [e for e in self.engine.game_map.entities if
                                             x_lower <= e.x < x_upper and
                                             y_lower <= e.y < y_upper]
        else:  # render all entities within FOV
            entities_sorted_for_rendering = [e for e in self.engine.game_map.entities
                                             if self.engine.game_map.visible[e.x][e.y]]
        entities_sorted_for_rendering = sorted(
            entities_sorted_for_rendering, key=lambda entity: entity.render_order.value
        )
        # print("entity count: ", len(self.engine.game_map.entities))

        # Update Each Entity Within "View"
        for e in entities_sorted_for_rendering:
            x_norm = e.x - x_lower
            y_norm = e.y - y_lower

            # Update Animation Cycle
            texture_name = e.name2
            try:
                true_anim_index = int(e.animation_index) * e.is_alive
                # Trickery to allow for player.png and player_0.png to exist as the same file
                tex = self.parent.tile_tex_dict[f"{texture_name}" + "%s" % (("_%s" % true_anim_index) * true_anim_index)]
            except KeyError:
                e.animation_index = 0
                tex = self.parent.tile_tex_dict[f"{texture_name}"]
            animation_speed = dt * 2
            e.animation_index += animation_speed
            texture_size = tex.size * 2

            try:
                # Rendering
                PushMatrix()
                entity_translate = Translate()
                entity_color = Color()
                entity_color.rgb = e.color
                entity_color.a = 1

                # Direction of Sprite
                if e.direction == Direction.LEFT:
                    entity_quad = Quad(texture=tex,
                                       points=(-texture_size[0] * 0.5, -texture_size[1] * 0.5,
                                               texture_size[0] * 0.5, -texture_size[1] * 0.5,
                                               texture_size[0] * 0.5, texture_size[1] * 0.5,
                                               -texture_size[0] * 0.5, texture_size[1] * 0.5)
                                       )
                else:  # elif e.direction == Direction.RIGHT:
                    entity_quad = Quad(texture=tex,
                                       points=(texture_size[0] * 0.5, -texture_size[1] * 0.5,
                                               -texture_size[0] * 0.5, -texture_size[1] * 0.5,
                                               -texture_size[0] * 0.5, texture_size[1] * 0.5,
                                               texture_size[0] * 0.5, texture_size[1] * 0.5)
                                       )
                entity_translate.xy = self.x + (texture_size[0] * 0.5) + (x_norm * self.TILE_SIZE), \
                                      self.y + (texture_size[1] * 0.5) + (y_norm * self.TILE_SIZE)
                # self.entity_graphics.append(entity_quad)
                PopMatrix()
            except KeyError:
                print("e.name2 : ", e.name, e.name2)