"""
graphics_loader.py
Utility file to load pixel graphics and assemble them as textures when needed
"""

from os import listdir

from kivy.core.image import Image as CoreImage

from array import array
from typing import Dict, Tuple

from kivy.graphics.texture import Texture


def populate_palette() -> Dict[str, Texture]:
    colors = {"floor": [200, 100, 50],
              # "dark_floor": [50, 50, 150],

              # Wall
              "wall": [130, 110, 50],
              "bottom_right": [130, 110, 50],
              "bottom_left": [130, 110, 50],
              "bottom_end": [130, 110, 50],
              "top_left": [130, 110, 50],
              "top_right": [130, 110, 50],
              "middle": [130, 110, 50],
              "horizontal": [130, 110, 50],
              "vertical": [130, 110, 50],
              "T_bottom": [130, 110, 50],
              "T_left": [130, 110, 50],
              "T_right": [130, 110, 50],
              "T_top": [130, 110, 50],
              # "dark_wall": [0, 0, 100],


              "blank": [50, 50, 50],
              "player": [255, 255, 255],
              "orc": [63, 127, 63],
              "troll": [0, 127, 0],
              "confusion_scroll": [207, 63, 255],
              "fireball_scroll": [255, 0, 0],
              "health_potion": [127, 0, 255],
              "lightning_scroll": [255, 255, 0],
              "dagger": [0, 191, 255],
              "sword": [0, 191, 255],
              "leather_armor": [139, 69, 19],
              "chain_mail": [139, 69, 19],
              "corpse": [191, 0, 0],
              "stairs": [100, 100, 100],
              "dark_stairs": [50, 50, 50],
              }
    tile_tex_dict = {name: generate_simple_texture(palette) for name, palette in colors.items()}
    return tile_tex_dict


def assemble_textures(directory: str="./assets/assets") -> Dict[str, Texture]:
    # Place all Textures in accessible-dictionary form
    tile_tex_dict = {}
    for img_name in listdir(directory):
        tile_tex_dict[img_name.split(".")[0]] = CoreImage(f"{directory}/{img_name}").texture
    return tile_tex_dict


def count_textures(directory: str="./assets/assets") -> Dict[str, int]:
    """
    Count all Textures and Keep Track of Animation "Counts"

    For example:

    d = count_textures()
    # player.png
    # player-1.png
    # player-2.png

    Would be d["player"] = 3
    """
    tex_count_dict = {}
    for img_name in listdir(directory):
        name1 = img_name.split(".")[0]
        name2 = name1.split("-")[0]
        # print(f"name2: {name2}")

        if tex_count_dict.get(name2):
            tex_count_dict[name2] += 1
        else:
            tex_count_dict[name2] = 1
    return tex_count_dict


def generate_simple_texture(rgb_palette: Tuple[int, int, int]) -> Texture:
    r, g, b = rgb_palette
    size = 32 * 32
    t = Texture.create(size=(32, 32))
    c =[r, g, b, 255]
    buf = c * size
    arr = array("B", buf)
    t.blit_buffer(arr, colorfmt="rgba", bufferfmt="ubyte")
    return t