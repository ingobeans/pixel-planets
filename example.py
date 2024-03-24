from pixelplanets import *

image = generate_planet(25, 25, array_width=90, array_height=90, uniform=False)
image = image_from_array(image)
image.save("output.png")
