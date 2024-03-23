from PIL import Image
import random
import math

def draw_ellipse(array, center, width, height, fill_value=1):
    for y in range(len(array)):
        for x in range(len(array[0])):
            if ((x - center[0]) / width)**2 + ((y - center[1]) / height)**2 <= 1:
                array[y][x] = fill_value

def apply_mask(image, mask):
    result = [[None] * len(image[0]) for _ in range(len(image))]  #

    for i in range(len(image)):
        for j in range(len(image[0])):
            if mask[i][j] == (255, 255, 255):
                result[i][j] = image[i][j]
            else:
                result[i][j] = (0, 0, 0)

    return result

def image_from_array(array):
    height = len(array)
    width = len(array[0])

    image = Image.new("RGB", (width, height))

    for y in range(height):
        for x in range(width):
            pixel_value = array[y][x]
            image.putpixel((x, y), pixel_value)

    return image

def generate_planet_mask(width, height, points, array_width, array_height):
    planet_mask = [[(0, 0, 0) for _ in range(array_width)]
                   for _ in range(array_height)]

    point_width = random.randint(math.ceil(min(width, height) / 3),
                                 min(width, height))

    point_height = random.randint(math.ceil(min(width, height) / 3),
                                  min(width, height))

    x = random.randint(math.ceil(point_width / 2),
                       array_width - math.floor(point_width / 2))

    y = random.randint(math.ceil(point_height / 2),
                       array_height - math.floor(point_height / 2))

    for point in range(points):
        mod_x = random.randint(point_width // 5, point_width // 2)
        mod_y = random.randint(point_height // 5, point_height // 2)
        draw_ellipse(planet_mask, (x + mod_x, y + mod_y), point_width,
                     point_height, (255, 255, 255))

    return planet_mask

def generate_planet(width=5, height=5, colour=(248, 128, 0), points=random.randint(1, 3), array_width=None, array_height=None):
    if array_width == None:
        array_width = width * 2
        array_height = height * 2

    image = [[colour for _ in range(array_width)]
             for _ in range(array_height)]

    planet_mask = generate_planet_mask(
        width, height, points, array_width, array_height)

    image = apply_mask(image, planet_mask)
    image = image_from_array(image)
    image.save("output.png")


generate_planet(25, 25, array_width=192, array_height=108)
