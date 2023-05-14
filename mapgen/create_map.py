import pickle

from PIL import ImageFont
from tqdm import tqdm
from PIL import Image, ImageDraw

data = pickle.load(open("data.pickle", "rb"))

fnt = ImageFont.truetype('arial.ttf', 65)
# Config
tile_x = 10000
tile_y = 10000
system_size = 300
tiles = 5

print("Mapgen")
print("----------------")
print("Total Systems: " + str(len(data)))
print("Width: " + str(tile_x))
print("Height: " + str(tile_y))
print("System Size: " + str(system_size))
print("Tiles: " + str(tiles**2))
print("Creating blank image")
img = Image.new('RGB', (tile_x, tile_y), color='black')
print("Creating ImageDraw instance")
d = ImageDraw.Draw(img)
for x_tile in range(tiles):
    for y_tile in range(tiles):
        print("Drawing tile " + str(x_tile) + ", " + str(y_tile))
        for system in data:
            image_x = (system.x*system_size) + tile_x//2 - x_tile*tile_x
            image_y = (system.y*system_size) + tile_y//2 - y_tile*tile_y
            d.ellipse((
                (image_x-system_size//2, image_y-system_size//2), (image_x+system_size//2, image_y+system_size//2)),
                fill=(46, 46, 46), outline="white")
            d.text((image_x, image_y), system.symbol, fill="blue", font=fnt, anchor="ms")
        print("Writing ...")
        img.save("tiles/tile_" + str(x_tile) + "_" + str(y_tile) + ".png")
