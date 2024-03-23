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

def generate_planet_mask(width, height, x, y, points, array_width, array_height, uniform, point_width, point_height):
    planet_mask = [[(0, 0, 0) for _ in range(array_width)]
                   for _ in range(array_height)]

    if uniform:
        draw_ellipse(planet_mask, (x, y), point_width,
                     point_height, (255, 255, 255))

        return planet_mask

    for point in range(points):
        mod_x = random.randint(point_width // 5, point_width // 2)
        mod_y = random.randint(point_height // 5, point_height // 2)
        draw_ellipse(planet_mask, (x + mod_x, y + mod_y), point_width,
                     point_height, (255, 255, 255))

    return planet_mask

def generate_rgb_variation(rgb, variance):
    r, g, b = rgb
    vr, vg, vb = variance
    new_r = min(max(0, r + random.randint(-vr, vr)), 255)
    new_g = min(max(0, g + random.randint(-vg, vg)), 255)
    new_b = min(max(0, b + random.randint(-vb, vb)), 255)
    return new_r, new_g, new_b

def generate_rgb_variations(rgb, num_variations, variance):
    variations = []
    for _ in range(num_variations):
        variation = generate_rgb_variation(rgb, variance)
        variations.append(variation)
    return variations

def generate_planet_colours():
    base = (random.randint(30, 255),
            random.randint(30, 255),
            random.randint(30, 255))

    colours = [base] + \
        generate_rgb_variations(base, random.randint(0, 4), (35, 35, 35))

    return colours

def generate_planet_texture(x, y, width, height, array_width, array_height, colours):
    texture = [[colours[0] for _ in range(array_width)]
               for _ in range(array_height)]

    size_standard = min(array_width, array_height)

    for colour in colours[1:]:
        splotches = random.randint(size_standard // 10, size_standard)

        size = random.randint(4, max(size_standard // 5, 8))
        for splotch in range(splotches):
            size_mod = random.randint(0, size // 5)
            splotch_size = size + size_mod
            splotch_x = random.randint(
                math.ceil(splotch_size / 2), array_width - math.ceil(splotch_size / 2))
            splotch_y = random.randint(
                math.ceil(splotch_size / 2), array_height - math.ceil(splotch_size / 2))

            if splotch_x < x or splotch_x >= x + width or splotch_y < y or splotch_y >= y + height:
                continue

            draw_ellipse(texture, (splotch_x, splotch_y),
                         splotch_size, splotch_size, colour)

    return texture

def generate_planet(width=5, height=5, x=None, y=None, colours: list[tuple] = None, array_width=None, array_height=None, points=random.randint(1, 3), point_width=None, point_height=None, uniform=False):
    if array_width == None:
        array_width = width * 2
        array_height = height * 2

    if point_width == None:
        point_width = random.randint(math.ceil(min(width, height) / 3),
                                     min(width, height))
        point_height = random.randint(math.ceil(min(width, height) / 3),
                                      min(width, height))

    if x == None:
        x = random.randint(math.ceil(point_width / 2),
                           array_width - math.floor(point_width / 2))
        y = random.randint(math.ceil(point_height / 2),
                           array_height - math.floor(point_height / 2))

    if not colours:
        colours = generate_planet_colours()

    image = generate_planet_texture(
        x, y, width, height, array_width, array_height, colours)

    planet_mask = generate_planet_mask(
        width, height, x, y, points, array_width, array_height, uniform, point_width, point_height)
    image = apply_mask(image, planet_mask)
    image = image_from_array(image)
    image.save("output.png")


generate_planet(25, 25, array_width=192, array_height=108)
