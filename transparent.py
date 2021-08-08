from os import getcwd, listdir

from PIL import Image


def make_transparent(file_name):
    img = Image.open(file_name)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((177, 156, 217, 0))
            # newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(file_name, "PNG")


if __name__ == "__main__":
    asset_path = "./assets/assets/"
    for file in listdir(asset_path):
        make_transparent(asset_path+ file)

