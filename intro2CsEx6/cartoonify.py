##############################################################################
# FILE: cartoonify.py
# EXERCISE: Intro2cs2 ex6 2021-2022
# DESCRIPTION: 
##############################################################################

##############################################################################
#                                   Imports                                  #
##############################################################################
import math, sys
from ex6_helper import *
from typing import Optional

##############################################################################
#                                   Typing                                   #
##############################################################################
SingleChannelImage = List[List[int]]
ColoredImage = List[List[List[int]]]
Image = Union[ColoredImage, SingleChannelImage]
Kernel = List[List[float]]


##############################################################################

# class bcolors:
#     HEADER = '\033[95m'
#     OKBLUE = '\033[94m'
#     OKCYAN = '\033[96m'
#     OKGREEN = '\033[92m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     ENDC = '\033[0m'
#     BOLD = '\033[1m'
#     UNDERLINE = '\033[4m'


###############################################################################


def separate_channels(image: ColoredImage) -> List[List[List[int]]]:
    """
    function that get List[List[List[int]]] (RGB Image) and return
    SingleChannelImage List[List[int]]
    :param image: the ColoredImage (RGB image) List[List[List[int]]]
    :return: List[List[List[int]]] list of 3 single channel image
    """
    number_of_channel = len(image[0][0])
    number_of_row = len(image)
    number_of_column = len(image[0])
    separate_list = []
    for color in range(number_of_channel):
        row_list = []
        for row in range(number_of_row):
            column_list = []
            for column in range(number_of_column):
                column_list.append(None)
            row_list.append(column_list)
        separate_list.append(row_list)
    for x, row in enumerate(image):
        for y, column in enumerate(row):
            for i, color in enumerate(column):
                separate_list[i][x][y] = color
    return separate_list


def combine_channels(channels: List[List[List[int]]]) -> ColoredImage:
    """
    function that get list of 3 separate color and combine them to one
    :param channels: list of 3 separate color (each SingleChannelImage)
    :return: List[List[List[int]]]
    """
    color_list = []  # channels[0][:]
    for x, row in enumerate(channels[0]):
        row_list = []
        for y, column in enumerate(row):
            column_list = []
            for i in range(len(channels)):
                column_list.append(channels[i][x][y])
            row_list.append(column_list)
        color_list.append(row_list)
    return color_list


def RGB2grayscale(colored_image: ColoredImage) -> SingleChannelImage:
    """
    function that get colored image(as 3D list) and return 2D list as gray
    scale image
    :param colored_image: 3D list as colored image
    :return: 2D list as gray scale image
    """
    gray_scale_list = []
    for row in colored_image:
        rows = []
        for column in row:
            red = column[0]
            green = column[1]
            blue = column[2]
            calculate = (red * 0.299) + (green * 0.587) + (blue * 0.114)
            rows.append(round(calculate))
        gray_scale_list.append(rows)
    return gray_scale_list


def blur_kernel(size: int) -> Kernel:
    """
    function that get size (int) and return list in size: "size"X"size"
    and the value of each cell is (1/size**2). the function to build the kernel
    to blur picture.
    :param size: the size of the kernel
    :return: List[List[float]] the blur kernel
    """
    list_kernel = []
    for row in range(size):
        row_list = []
        for column in range(size):
            row_list.append(1 / size ** 2)
        list_kernel.append(row_list)
    return list_kernel


def out_of_the_range(index: tuple, x_length: int, y_length: int) -> bool:
    """
    check if the index out of the range of the image
    :param index: index: tuple (int) (x,y) the index of specific cell
    :param image: 2D list present image
    :return: boolean (if the index out of the range return True)
    """
    x = index[0]
    y = index[1]
    if x >= 0 and x < x_length:
        if y >= 0 and y < y_length:
            return False
    return True


def index_and_kernel_to_avg_new2(index: tuple, image: SingleChannelImage,
                                 kernel: List[float]) -> int:
    """
    function that get index (x,y) from the image, image and kernel and return
    the average of the values of the cells that surround the specific cell
    :param index: tuple (int) (x,y) the index of specific cell
    :param image: the 2D list of the image
    :param kernel: the kernel that calculate the average
    :return: the average of the center cell
    """
    avg = 0
    x_length = len(image)
    y_length = len(image[0])
    index_x = index[0]
    index_y = index[1]
    value_center_index = image[index[0]][index[1]]

    size_of_kernel = int(1 / (kernel[0][0])) ** 0.5
    max_step = int((size_of_kernel - 1) // 2)
    row1 = int(index_x - max_step)
    lim = index_x + max_step + 1
    lim2 = int(index_y + max_step + 1)
    column1 = int(index_y - max_step)
    for row in range(row1, lim):
        for column in range(column1, lim2):
            if out_of_the_range((row, column), x_length, y_length):
                avg += kernel[0][0] * value_center_index
            else:
                avg += kernel[0][0] * image[row][column]
    return round(avg)


def value_of_cell_update(value: int):
    """
    check the value of the cell if the value not round, rount it and if
    the value under "0" round it to 0 and if value bigger that 255, decrease it
    to 255
    :param value: value of specific cells
    :return: int (the new value)
    """
    value = round(value)
    if value > 255:
        return 255
    elif value < 0:
        return 0
    return value


def apply_kernel(image: SingleChannelImage,
                 kernel: Kernel) -> SingleChannelImage:
    """
    function that get 2D list as single channel image and kernel, and return
    the 2D list after using with the kernel
    :param image: 2D list as single channel image
    :param kernel: 2D list (float)
    :return: new single channel image (2D list[list[int]])
    """
    image_after_filter = deepcopy(image)
    for x, row in enumerate(image):
        for y, column in enumerate(row):
            value = value_of_cell_update(
                index_and_kernel_to_avg_new2((x, y), image,
                                             kernel))
            image_after_filter[x][y] = value
    return image_after_filter


def bilinear_interpolation(image: SingleChannelImage, y: float,
                           x: float) -> int:
    """
    A function that receives a 2D list (image with a single color channel),
    and 2 numbers (float) and returns the relative value of the same pixel
    by the 2 numbers that represent X and Y
    :param image: image with a single color channel
    :param y: (float) value of the y in the index
    :param x: (float) value of the x in the index
    :return: (int) the value of the index in the original image
    """
    x_length = len(image)
    y_length = len(image[0])
    # Check if it's the edges
    if x == 0 and y == 0:
        return image[0][0]
    elif x == 0 and y == y_length - 1:
        return image[y_length - 1][0]
    elif y == 0 and x == x_length - 1:
        return image[0][x_length - 1]
    elif x == x_length - 1 and y == y_length - 1:
        return image[y_length - 1][x_length - 1]

    # If it is not the edges:
    if x != round(x):
        x_round_down = int(x)
        x_round_up = int(x + 1)
    else:
        x_round_down = int(x - 1)
        x_round_up = int(x)
    if y != round(y):
        y_round_down = int(y)
        y_round_up = int(y + 1)
    else:
        y_round_down = int(y - 1)
        y_round_up = int(y)

    # calculate the delta x and delta y
    delta_x = x - x_round_down
    delta_y = y - y_round_down

    # calculate the value of each cell
    a = image[y_round_down][x_round_down]
    b = image[y_round_up][x_round_down]
    c = image[y_round_down][x_round_up]
    d = image[y_round_up][x_round_up]

    # calculate the value of each corner
    a_value = a * (1 - delta_x) * (1 - delta_y)
    b_value = b * delta_y * (1 - delta_x)
    c_value = c * delta_x * (1 - delta_y)
    d_value = d * delta_x * delta_y

    # calculate the complete value
    value = a_value + b_value + c_value + d_value
    value = round(value)
    return value


def new_value_indexes(des_index, num_original_line, num_des_line):
    """
    function that return the index from the original image
    :param des_index: the new x\y value of the new image
    :param num_original_line: the number of the line in the original image
    :param num_des_line: the number of the line in the destination image
    :return: the x\y value of the original image
    """
    return (des_index * (num_original_line - 1)) / (num_des_line - 1)


def resize(image: SingleChannelImage, new_height: int,
           new_width: int) -> SingleChannelImage:
    """
    function that resize to SingleChannelImage.
    :param image: the original image
    :param new_height: the new height
    :param new_width: the new width
    :return: new image (SingleChannelImage) with the right size
    """
    new_picture = []
    num_original_line_x = len(image[0])
    num_original_line_y = len(image)
    for y in range(new_height):
        new_line = []
        for x in range(new_width):
            new_x = new_value_indexes(x, num_original_line_x, new_width)
            new_y = new_value_indexes(y, num_original_line_y, new_height)

            new_value = bilinear_interpolation(image, new_y, new_x)
            new_line.append(new_value)
        new_picture.append(new_line)
    return new_picture


def scale_down_colored_image(image: ColoredImage, max_size: int) -> Optional[
    ColoredImage]:
    """
    function that receive colored image and max_size and if the sizes of the
    image are bigger the function decrease the size
    :param image: 3D list- colored image
    :param max_size: int the max size (height and width)
    :return: new colored image with the right size
    """
    width = len(image[0])
    height = len(image)
    if width < max_size and height < max_size:
        return None
    if width > height:
        prop = width / max_size
        new_width = max_size
        new_height = round(height / prop)
    else:
        prop = height / max_size
        new_height = max_size
        new_width = round(width / prop)
    sep_list = separate_channels(image)
    new_image = []
    for channel in sep_list:
        channel = resize(channel, new_height, new_width)
        new_image.append(channel)
    new_image = combine_channels(new_image)
    return new_image


def rotate_90(image: Image, direction: str) -> Image:
    """
    function that receive image (colored or single channel) and rotate 90
    degrees dependent about the "direction" L=left R=right
    :param image: the image (colored or single channel)
    :param direction: the direction that the function need to rotate
    :return: rotated image
    """
    width = len(image[0])
    height = len(image)
    rotate_image = []
    # direction is Left
    if direction == "L":
        for x in range(width - 1, -1, -1):
            line = []
            for y in range(height):
                line.append(image[y][x])
            rotate_image.append(line)
        return rotate_image

    # direction is right:
    else:
        for x in range(width):
            line = []
            for y in range(height - 1, -1, -1):
                line.append(image[y][x])
            rotate_image.append(line)
        return rotate_image


def get_edges(image: SingleChannelImage, blur_size: int, block_size: int,
              c: int) -> SingleChannelImage:
    """
    function that return black-white image. the black lines present the
    edges of the object (like a dog or woman)
    :param image: the image (SingleChannelImage) that need to detect the edge
    :param blur_size: the size of the blur before the detection
    :param block_size: the size of the detection kernel
    :param c: number that check the difference between the average to the
    current value
    :return: 2D list that present black-white image
    """
    pic = apply_kernel(image, blur_kernel(blur_size))
    edge = []
    for y, row in enumerate(image):
        line = []
        for x, column in enumerate(row):
            avg = index_and_kernel_to_avg_new2((y, x), pic,
                                               blur_kernel(block_size))
            threshold = avg - c
            if threshold > column:
                line.append(0)
            else:
                line.append(255)
        edge.append(line)
    return edge


def quantize(image: SingleChannelImage, N: int) -> SingleChannelImage:
    """
    function that receive single channel image and return image with
    less variety of colors ("N" color)
    :param image: the original image
    :param N:the number of the color that the update image should return
    :return: new image with less variety of colors
    """
    qimg = []
    for y, row in enumerate(image):
        line = []
        for x, column in enumerate(row):
            cell_qimg = round(math.floor(column * N / 256) * 255 / (N - 1))
            line.append(cell_qimg)
        qimg.append(line)
    return qimg


def quantize_colored_image(image: ColoredImage, N: int) -> ColoredImage:
    """
    function that receive colored image and return colored image after
    quantization ->less variety of colors ("N" color)
    :param image: colored image
    :param N: the number of the color
    :return: quantized colored image
    """
    sep_image = separate_channels(image)
    sep_image_qimp = []
    for color in sep_image:
        sep_image_qimp.append(quantize(color, N))
    return combine_channels(sep_image_qimp)


def make_mask(image: SingleChannelImage):
    """function that receive edge image and return the image after update
    the values: 255-> 0->0"""
    new_heart = []
    for y, row in enumerate(image):
        line = []
        for x, column in enumerate(row):
            line.append(round(column / 255))
        new_heart.append(line)
    return new_heart


def add_mask_2D(image1: Image, image2: Image,
                mask: List[List[float]]) -> Image:
    """
    function that receive 2 images of 2D and mask and combine both of the
    images according to the "mask"
    :param image1: first image
    :param image2: second image
    :param mask: the mask (2D list) present shape that need to combine both
    of the images
    :return: combined image
    """
    new_image = []
    for y, row in enumerate(image1):
        line_new_image = []
        for x, column in enumerate(row):
            val = round(
                image1[y][x] * mask[y][x] + image2[y][x] * (1 - mask[y][x]))
            line_new_image.append(val)
        new_image.append(line_new_image)
    return new_image


def add_mask(image1: Image, image2: Image, mask: List[List[float]]) -> Image:
    """
    function that receive 2 images of 2\3D and mask and combine both of the
    images according to the "mask"
    :param image1: first image
    :param image2: second image
    :param mask: the mask (2D list) present shape that need to combine both
    of the images
    :return: combined image
    """
    if type(image1[0][0]) == list:
        qimg = []
        sep_list1 = separate_channels(image1)
        sep_list2 = separate_channels(image2)
        for i, color in enumerate(sep_list1):
            value = add_mask_2D(sep_list1[i], sep_list2[i], mask)
            qimg.append(value)
        return combine_channels(qimg)
    return add_mask_2D(image1, image2, mask)


def cartoonify(image: ColoredImage, blur_size: int, th_block_size: int,
               th_c: int, quant_num_shades: int) -> ColoredImage:
    """
    function that make image as cartoon
    :param image: 2\3 D image
    :param blur_size: the size of the blur before the detection
    :param th_block_size: the size of the detection kernel
    :param th_c: number that check the difference between the average to the
    current value
    :param quant_num_shades: the number of the color that will be after
    the quantize function
    :return: cartoon image
    """
    gray_scale_pic = RGB2grayscale(image)
    edge = get_edges(gray_scale_pic, blur_size, th_block_size, th_c)
    quant_image = quantize_colored_image(image, quant_num_shades)
    three_d_edge = combine_channels([edge, edge, edge])
    cartoonify_image = add_mask(quant_image, three_d_edge, make_mask(edge))
    return cartoonify_image


if __name__ == '__main__':
    ERROR_PARAM = "There is a problem with the amount of inputs, there should" \
                  " be 8 inputs"
    if len(sys.argv) != 8:
        print(ERROR_PARAM)
    else:
        image_source = sys.argv[1]
        cartoon_dest = sys.argv[2]
        max_im_size = int(sys.argv[3])
        blur_size = int(sys.argv[4])
        th_block_size = int(sys.argv[5])
        th_c = int(sys.argv[6])
        quant_num_shades = int(sys.argv[7])


        picture_list = load_image(image_source)
        picture_list = scale_down_colored_image(picture_list, max_im_size)
        cartoon_image = cartoonify(picture_list, blur_size, th_block_size, th_c
                                   , quant_num_shades)

        save_image(cartoon_image, cartoon_dest)
