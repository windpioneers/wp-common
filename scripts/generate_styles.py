import csv
import json
import logging
import os


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

STYLE_SCHEMA = {
    "type": "object",
    "properties": {
        "style_name": {"type": "string"},
        "icon_name": {"type": "string"},
        "icon_size": {"type": "number"},
        "icon_color": {"type": "hexColor"},
        "icon_transparency": {"type": "number"},
        "label_size": {"type": "number"},
        "line_color": {"type": "hexColor"},
        "line_width": {"type": "number"},
        "line_transparency": {"type": "number"},
        "area_color": {"type": "hexColor"},
        "area_transparency": {"type": "number"},
    },
}


def convert_to_hex_color(value):
    if isinstance(value, str) and len(value) in [3, 4, 6, 8, 9, 12]:
        return ("#" + value).replace("##", "#").upper()

    raise TypeError(f"hexcolor should be a string type with a specific character count: '{value}'")


SCHEMA_TYPE_CAST_MAP = {"number": float, "hexColor": convert_to_hex_color, "string": str, "integer": int}


def generate_style(row, headers):
    style = {}
    for header_item, row_item in zip(headers, row):
        if header_item in STYLE_SCHEMA["properties"]:
            schema = STYLE_SCHEMA["properties"][header_item]
            cast_function = SCHEMA_TYPE_CAST_MAP[schema["type"]]
            value = cast_function(row_item)

            style[header_item] = value

    return style


def generate_styles(style_rows):
    sorted_style_rows = sorted(style_rows, key=lambda d: d["style_name"])

    styles = {}

    for style in sorted_style_rows:
        styles[style["style_name"]] = style

    return styles


def write_styles_json(styles, output_file):
    with open(output_file, "w") as fo:
        json.dump(styles, fo, indent=2)


def clean_row(row):
    return [item.strip() for item in row]


def main():
    styles_csv_path = os.path.join(REPOSITORY_ROOT_FOLDER, "assets", "styles", "styles.csv")

    with open(styles_csv_path, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar="|")

        headers = []
        style_rows = []
        for row in reader:
            row = clean_row(row)

            if not headers:
                headers = row
            else:
                style_rows.append(generate_style(row, headers))

        styles = generate_styles(style_rows)

        output_path = os.path.join(REPOSITORY_ROOT_FOLDER, "public", "styles.json")
        write_styles_json(styles, output_path)


if __name__ == "__main__":
    main()
