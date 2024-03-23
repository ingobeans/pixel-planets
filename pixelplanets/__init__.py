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
                     point_width, (255, 255, 255))

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

def generate_planet_colours(colour_variance, variations_amount=None):
    if variations_amount == None:
        variations_amount = random.randint(
            0, 4)
    base = (random.randint(30, 255),
            random.randint(30, 255),
            random.randint(30, 255))

    colours = [base] + \
        generate_rgb_variations(
            base, variations_amount, (colour_variance, colour_variance, colour_variance))

    return colours

def generate_planet_texture(x, y, width, height, array_width, array_height, colours):
    base = colours.pop(0)
    texture = [[base for _ in range(array_width)]
               for _ in range(array_height)]

    if len(colours) == 0:
        return texture

    size_standard = min(array_width, array_height)
    sizes = [random.randint(4, max(size_standard // 5, 8))
             for c in colours]

    if len(colours) > 1:
        # sort all colours by how large their splotches are, so that large splotches are always drawn behind small ones
        combined = list(zip(colours, sizes))
        combined_sorted = sorted(combined, key=lambda x: x[1], reverse=True)

        colours, sizes = zip(*combined_sorted)

    for index, colour in enumerate(colours):
        splotches = random.randint(size_standard // 10, size_standard)

        size = sizes[index]
        for splotch in range(splotches):
            size_mod = random.randint(0, size // 5)
            splotch_size = size + size_mod
            splotch_x = random.randint(
                math.ceil(splotch_size / 2), array_width - math.ceil(splotch_size / 2))
            splotch_y = random.randint(
                math.ceil(splotch_size / 2), array_height - math.ceil(splotch_size / 2))

            if splotch_x + splotch_size < x or splotch_x >= x + width or splotch_y + splotch_size < y or splotch_y >= y + height:
                continue

            draw_ellipse(texture, (splotch_x, splotch_y),
                         splotch_size, splotch_size, colour)

    return texture

def generate_planet(width=5, height=5, x=None, y=None, colours: list[tuple] = None, array_width=None, array_height=None, colour_variance=36, variations_amount=None, points=random.randint(1, 3), point_width=None, point_height=None, uniform=False):
    """width and height control the planets size. 

    x and y, its position within the array. 

    colours is an array of rgb tuples, which colours to use for details (first is base colour). 

    array_width and height are dimensions of the array itself containing the planet. 

    colour_variance is only used if colours isn't specified, if so, it determines how much the detail colours will vary from base colour. 

    variations_amount is only used if colours isn't specified, if so, it determines are how many detail colours to use.

    uniform controls if planet is just a single circle or if it has some more shape to it

    points, is used if planet isn't uniform. then thats how many different circles to combine for planet shape.

    point_width and height are used to directly specify size of those points."""
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
        colours = generate_planet_colours(colour_variance, variations_amount)

    image = generate_planet_texture(
        x, y, width, height, array_width, array_height, colours)

    planet_mask = generate_planet_mask(
        width, height, x, y, points, array_width, array_height, uniform, point_width, point_height)
    image = apply_mask(image, planet_mask)
    return image
