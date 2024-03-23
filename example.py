from pixelplanets import *

image = generate_planet(25, 25, array_width=192,
                        array_height=108, uniform=False)
image = image_from_array(image)
image.save("output.png")
