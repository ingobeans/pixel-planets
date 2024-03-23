# Pixel Planets Generator

Generate customizable simple pixely planets.
![Autumn Planet](https://github.com/ingobeans/pixel-planets/blob/main/example_planets/autumn_hd.png)

## Installation

* Download pixel-planets and unzip
* In the pixel-planets folder, run `pip install --upgrade .`

## Usage

The generate_planet function is the main function to generate planets. It takes a whole load of arguments:

* width and height control the planets size. 
* x and y, its position within the array. 
* colours is an array of rgb tuples, which colours to use for details (first is base colour). 
* array_width and height are dimensions of the array itself containing the planet. 
* colour_variance is only used if colours isn't specified, if so, it determines how much the detail colours will vary from base colour. 
* variations_amount is only used if colours isn't specified, if so, it determines are how many detail colours to use.
* uniform controls if planet is just a single circle or if it has some more shape to it
* points, is used if planet isn't uniform. then thats how many different circles to combine for planet shape.
* point_width and height are used to directly specify size of those points.

Example usage (also found in example.py):
```py
from pixelplanets import *

image = generate_planet(25, 25, array_width=192,
                        array_height=108, uniform=False)
image = image_from_array(image)
image.save("output.png")
```