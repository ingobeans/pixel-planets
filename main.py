from PIL import Image
import numpy as np

def draw_ellipse(array, center, width, height, fill_value=1):
    for y in range(array.shape[0]):
        for x in range(array.shape[1]):
            if ((x - center[0]) / width)**2 + ((y - center[1]) / height)**2 <= 1:
                array[y, x] = fill_value

array_width = 190
array_height = 108

array = np.zeros((array_height, array_width))

center = (10, 5)

width = 5
height = 5

draw_ellipse(array, (array_width // 2, array_height // 2), width, height)
draw_ellipse(array, (array_width // 2 + 2, array_height // 2 + 2), width, height)

image = Image.fromarray(np.uint8(array * 255), mode="L")
image.save("output.png")