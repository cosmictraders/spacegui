import pickle

from PIL import ImageFont
from tqdm import tqdm
from PIL import Image, ImageDraw

data = pickle.load(open("data.pickle", "rb"))

fnt = ImageFont.truetype('arial.ttf', 30)
# Config
width = 80000
height = 80000
system_size = 140

print("Mapgen")
print("----------------")
print("Total Systems: " + str(len(data)))
print("Width: " + str(width))
print("Height: " + str(height))
print("System Size: " + str(system_size))
print("Creating blank image")
img = Image.new('RGB', (width, height), color='black')
print("Creating ImageDraw instance")
d = ImageDraw.Draw(img)
print("Drawing ...")
for system in tqdm(data):
    image_x = (system.x*system_size) + width//2
    image_y = (system.y*system_size) + height//2
    d.ellipse((
        (image_x-system_size//2, image_y-system_size//2), (image_x+system_size//2, image_y+system_size//2)),
              fill=(46, 46, 46), outline="white")
    d.text((image_x, image_y), system.symbol, fill="blue", font=fnt, anchor="ms")
print("Writing ...")
img.save('image.png')
