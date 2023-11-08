import os
from PIL import Image


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


def generate_icon_atlas(images, file_path, icons_in_a_row=10, spacing=10):
    # Assume all icons have the same height and width
    width, height = images[0].size

    # Initialize icon atlas, single row
    icon_atlas_width = width * len(images)
    # # Add spacing
    # icon_atlas_width += spacing * len(images) - 1

    icon_atlas_height = height
    # # Add spacing
    # icon_atlas_height += (num_rows + 1) * spacing

    icon_atlas = Image.new(mode='RGBA', size=(icon_atlas_width, icon_atlas_height), color=(0,0,0,0))

    for i, image in enumerate(images):
        image_x = (width * i) # add spacing
        image_y = 0 # add rows
        icon_atlas.paste(image,(image_x,image_y))

    icon_atlas.save(file_path)


def main():
    images = get_icon_images(os.path.join(REPOSITORY_ROOT_FOLDER, "assets", "icons"))
    generate_icon_atlas(images, "icon_atlas.png")


if __name__ == "__main__":
    main()
