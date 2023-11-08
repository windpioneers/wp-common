import logging
import math
import os
from PIL import Image


ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)

file_handler = logging.FileHandler(os.path.join(os.path.dirname(__file__), os.path.basename(__file__) + ".log"))
file_handler.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)
logger.addHandler(file_handler)


REPOSITORY_ROOT_FOLDER = os.path.dirname(os.path.dirname(__file__))


def get_icon_images(icon_folder, icon_extension="png"):
    files = os.listdir(icon_folder)
    images = []

    for file in files:
        if file.endswith(icon_extension):
            filepath = os.path.join(icon_folder, file)
            img = Image.open(filepath)
            images.append(img)

    return images


def generate_icon_atlas(images, file_path, icons_in_a_row=10, spacing=10, embed_name=False):
    # Assume all icons have the same height and width
    width, height = images[0].size

    # Initialize icon atlas
    icon_atlas_width = (width * icons_in_a_row) + (spacing * (icons_in_a_row + 1))

    number_of_rows = math.ceil(len(images) / icons_in_a_row)
    icon_atlas_height = (height * number_of_rows) + (spacing * (number_of_rows + 1))

    icon_atlas = Image.new(mode="RGBA", size=(icon_atlas_width, icon_atlas_height), color=(0, 0, 0, 0))

    for i, image in enumerate(images):
        row = math.floor(i / icons_in_a_row)
        column = i % icons_in_a_row

        logger.debug("Pasting icon %s to row %s column %s", image.filename, row, column)

        image_x = spacing + (width * column) + (spacing * column)
        image_y = spacing + (height * row) + (spacing * row)
        icon_atlas.paste(image, (image_x, image_y))

    icon_atlas.save(file_path)


def main():
    logger.info("Preparing list of icons to add to icon atlas. Accepts only png files")

    images = get_icon_images(os.path.join(REPOSITORY_ROOT_FOLDER, "assets", "icons"))
    number_of_images = len(images)

    logger.info("Adding %s icons to the icon atlas", number_of_images)
    icon_atlas_file_path = "icon_atlas.png"

    generate_icon_atlas(images, icon_atlas_file_path)
    logger.info("Generated icon atlas at location %s", icon_atlas_file_path)


if __name__ == "__main__":
    main()
