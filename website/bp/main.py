import os
from io import BytesIO
from pathlib import Path

from PIL import Image
from autotraders.agent import Agent
from flask import *

from website.session import get_session

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    s = get_session()
    agent = Agent(s)
    return render_template("index.html", agent=agent)


@main_bp.route("/map/")
def map():
    return render_template("map.html")


@main_bp.route("/map_tile/<z>/<x>/<y>.png")
async def map_api(z, x, y):
    x = int(x)
    y = int(y)
    z = int(z)
    tiles_path = Path(os.getcwd()) / "website" / "static" / "tiles"
    if z == 2:
        img = Image.new('RGBA', (10000, 10000), color='black')
        image1 = Image.open(tiles_path / ("tile_" + str(x) + "_" + str(y) + ".png")).reduce(2)
        image2 = Image.open(tiles_path / ("tile_" + str(x + 1) + "_" + str(y) + ".png")).reduce(2)
        image3 = Image.open(tiles_path / ("tile_" + str(x) + "_" + str(y + 1) + ".png")).reduce(2)
        image4 = Image.open(tiles_path / ("tile_" + str(x + 1) + "_" + str(y + 1) + ".png")).reduce(2)
        img.paste(image1, (0, 0, 5000, 5000))
        img.paste(image2, (5000, 0, 10000, 5000))
        img.paste(image3, (0, 5000, 5000, 10000))
        img.paste(image4, (5000, 5000, 10000, 10000))
        new_img = img.reduce(8)
        img_io = BytesIO()
        new_img.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    elif z == 3:
        img = Image.open(
            tiles_path / ("tile_" + str(int(x)) + "_" + str(int(y)) + ".png"))
        new_img = img.reduce(8)
        img_io = BytesIO()
        new_img.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    else:

        img = Image.open(
            tiles_path / ("tile_" + str(int(8 * x / (2 ** z))) + "_" + str(int(8 * y / (2 ** z))) + ".png"))
        x_part = 8 * x / (2 ** z) % 1
        y_part = 8 * y / (2 ** z) % 1
        assert img.height == img.width
        dimension = img.height
        scale = int(8 * (1 / z ** 2) * dimension)
        x_coord = int(x_part * dimension)
        y_coord = int(y_part * dimension)
        new_img = img.crop((x_coord, y_coord, x_coord + scale, y_coord + scale))
        img_io = BytesIO()
        new_img.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')


@main_bp.route("/map-v2/")
def map_v2():
    return render_template("map_v2.html")


@main_bp.route("/map-v3/")
def map_v3():
    return render_template("map_v3.html")
