# example code that generates a wallpaper suitable image using the planet generator

from pixelplanets import *
import ctypes

user32 = ctypes.windll.user32
width, height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

image = generate_planet(25, 25, array_width=width // 10,
                        array_height=height // 10, uniform=False, variations_amount=random.randint(1, 4))
# settings to ensure planet always has details and is roughly a good size

image = image_from_array(image)

for y in range(image.height):
    for x in range(image.width):
        pixel = image.getpixel((x, y))

        if pixel == (0, 0, 0):
            if random.randint(0, 1000) == 0:
                image.putpixel((x, y), (255, 255, 255))

image = image.resize((width // 10 * 10, height // 10 * 10), Image.NEAREST)
image.save("output.png")
