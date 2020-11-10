import colorgram

# Extract 6 colors from an image.
colors = colorgram.extract('test.jpg', 6)

# colorgram.extract returns Color objects, which let you access
# RGB, HSL, and what proportion of the image was that color.

for x in colors:

    first_color = x
    rgb = first_color.rgb # e.g. (255, 151, 210)
    hsl = first_color.hsl # e.g. (230, 255, 203)
    proportion  = first_color.proportion # e.g. 0.34

    print(rgb)
    print(hsl)
    print(proportion)
# RGB and HSL are named tuples, so values can be accessed as properties.
# These all work just as well:
red = rgb[0]
red = rgb.r
saturation = hsl[1]
saturation = hsl.s