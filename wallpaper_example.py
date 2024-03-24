# example code that generates a wallpaper suitable image using the planet generator

from pixelplanets import *
import ctypes

user32 = ctypes.windll.user32
width, height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# downscale resolution
width, height = width // 10, height // 10

min_x = width // 3
max_x = width - width // 3

min_y = height // 3
max_y = height - height // 3

# forces stars to generate within roughly center of screen

x = random.randint(min_x, max_x)
y = random.randint(min_y, max_y)

image = generate_planet(25, 25, array_width=width, array_height=height, uniform=False, variations_amount=random.randint(1, 4), x=x, y=y)
# settings to ensure planet always has details and is roughly a good size

image = image_from_array(image)

# loop to replace roughly every thousands black pixel with white
# (stars)
for y in range(image.height):
    for x in range(image.width):
        pixel = image.getpixel((x, y))

        if pixel == (0, 0, 0):
            if random.randint(0, 1000) == 0:
                image.putpixel((x, y), (255, 255, 255))

image = image.resize((width * 10, height * 10), Image.NEAREST)
image.save("output.png")
