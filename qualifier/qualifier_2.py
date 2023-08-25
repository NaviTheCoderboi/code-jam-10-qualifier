from PIL import Image


def Valid_input(
    image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]
) -> bool:
    valid = []
    num_tiles_width = image_size[0] // tile_size[0]
    num_tiles_height = image_size[1] // tile_size[1]
    num_of_tiles = num_tiles_width * num_tiles_height
    if num_of_tiles != len(ordering):
        valid.append(False)
    if image_size[0] % tile_size[0] != 0 or image_size[1] % tile_size[1] != 0:
        valid.append(False)
    for order in ordering:
        count = ordering.count(order)
        if count > 1:
            valid.append(False)
            break
    if valid:
        return False
    else:
        return True


def Rearrange_tiles(
    image_path: str, tile_size: tuple[int, int], ordering: list[int], out_path: str
) -> None:
    """
    Rearrange the image.

    The image is given in `image_path`. Split it into tiles of size `tile_size`, and rearrange them by `ordering`.
    The new image needs to be saved under `out_path`.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once. If these conditions do not hold, raise a ValueError with the message:
    "The tile size or ordering are not valid for the given image".
    """
    opened_image = Image.open(image_path)
    img_width, img_height = opened_image.size
    tile_width, tile_height = tile_size
    num_tiles_width = img_width // tile_width

    is_valid = Valid_input(
        [img_width, img_height], tile_size=tile_size, ordering=ordering
    )
    if not is_valid:
        raise ValueError("The tile size or ordering are not valid for the given image")

    new_image = Image.new("RGBA", (img_width, img_height))

    for new_tile_index, old_tile_index in enumerate(ordering):
        old_col = old_tile_index % num_tiles_width
        old_row = old_tile_index // num_tiles_width

        left = old_col * tile_width
        upper = old_row * tile_height
        right = left + tile_width
        lower = upper + tile_height

        new_col = new_tile_index % num_tiles_width
        new_row = new_tile_index // num_tiles_width

        new_left = new_col * tile_width
        new_upper = new_row * tile_height

        tile = opened_image.crop((left, upper, right, lower))
        new_image.paste(tile, (new_left, new_upper))
    new_image.save(out_path)


# with open("qualifier\images\pydis_logo_order.txt") as f:
#     lines = f.readlines()
# lines = [int(lines.strip()) for lines in lines]

# rearrange_tiles(
#     image_path="qualifier\images\pydis_logo_scrambled.png",
#     ordering=lines,
#     out_path="test.png",
#     tile_size=[256, 256],
# )
