import json
import os

from PIL import Image

SUFFIXS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".JPG",
    ".JPEG",
    ".PNG",
    ".GIF",
    ".BMP",
]


def readConfigFile(config_file: str, encoding="utf-8"):
    with open(config_file, "r", encoding=encoding) as f:
        return json.load(f)


def getConfigData(config_file: str):
    try:
        config_json = readConfigFile(config_file)
    except:
        config_json = readConfigFile(config_file, encoding="utf-8-sig")
    return config_json


def selectPicture(floder_path: str):
    paths = os.listdir(floder_path)
    for path in paths:
        file_name = os.path.join(floder_path, path)
        if os.path.isfile(file_name):
            for suffix in SUFFIXS:
                if path.endswith(suffix):
                    splitPicture(file_name)
                    break
    return None


def splitPicture(file_name: str, width_dt: int = 10):
    config_file = "config.json"
    if os.path.exists(config_file):
        config_json = getConfigData(config_file)
    else:
        config_json = {"图片高度": 2400, "重复高度": 200}
        with open(config_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(config_json, ensure_ascii=False))
    pic_height = config_json["图片高度"]
    idt_height = config_json["重复高度"]

    path, text = os.path.splitext(file_name)
    _, name = os.path.split(path)
    if not os.path.exists(path):
        os.mkdir(path)
    im = Image.open(file_name)
    image_width, image_height = im.size

    i = 1
    upper = 0
    to_image = None
    while upper < image_height:
        if upper > idt_height:
            upper -= idt_height
        bottom = upper + pic_height
        if bottom > image_height:
            bottom = image_height
        region = im.crop((0, upper, image_width, bottom))
        region.save(os.path.join(path, f"{name}_{i:02d}{text}"))

        if to_image is None:
            to_image = Image.new(
                "RGB", (image_width * 2 + width_dt, pic_height), "white"
            )
            to_image.paste(region, (0, 0))
        else:
            to_image.paste(region, (image_width + width_dt, 0))
            to_image.save(os.path.join(path, f"_{name}_{(i-1):02d}{text}"))
            to_image = Image.new(
                "RGB", (image_width * 2 + width_dt, pic_height), "white"
            )
            to_image.paste(region, (0, 0))

        upper = bottom
        i += 1
    return None
