import numpy as np
import cv2


def valid_input(
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


def rearrange_tiles(
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
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    img_height, img_width, _ = image.shape
    tile_width, tile_height = tile_size

    is_valid = valid_input((img_height, img_width), (tile_height, tile_width), ordering)
    if not is_valid:
        raise ValueError("The tile size or ordering are not valid for the given image")

    num_tiles_width = img_width // tile_width

    new_image = np.zeros_like(image)

    for new_tile_index, old_tile_index in enumerate(ordering):
        old_row, old_col = divmod(old_tile_index, num_tiles_width)
        new_row, new_col = divmod(new_tile_index, num_tiles_width)

        tile = image[
            old_row * tile_height : (old_row + 1) * tile_height,
            old_col * tile_width : (old_col + 1) * tile_width,
        ]

        new_image[
            new_row * tile_height : (new_row + 1) * tile_height,
            new_col * tile_width : (new_col + 1) * tile_width,
        ] = tile

    cv2.imwrite(out_path, new_image)


# with open("qualifier\images\great_wave_order.txt") as f:
#     lines = f.readlines()
# lines = [int(lines.strip()) for lines in lines]

# rearrange_tiles(
#     image_path="qualifier\images\great_wave_scrambled.png",
#     ordering=lines,
#     out_path="test.png",
#     tile_size=(16, 16),
# )
