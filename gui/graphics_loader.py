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
              "dark_floor": [50, 50, 150],
              "wall": [130, 110, 50],
              "dark_wall": [0, 0, 100],
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


def generate_simple_texture(rgb_palette: Tuple[int, int, int]) -> Texture:
    r, g, b = rgb_palette
    size = 32 * 32
    t = Texture.create(size=(32, 32))
    c =[r, g, b, 255]
    buf = c * size
    arr = array("B", buf)
    t.blit_buffer(arr, colorfmt="rgba", bufferfmt="ubyte")
    return t