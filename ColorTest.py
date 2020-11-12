import colorgram
import numpy
from colr import color

# Extract 6 colors from an image.
colors = colorgram.extract('test6.png', 100) 

# colorgram.extract returns Color objects, which let you access
# RGB, HSL, and what proportion of the image was that color.

# colorgram also sorts the colors from most prominent to least prominent

for x in colors:
    testColor = x
    rgb = testColor.rgb # e.g. (255, 151, 210)
    hsl = testColor.hsl # e.g. (230, 255, 203)
    proportion = testColor.proportion # e.g. 0.34

    print("\n")
    print(color("   ", back=(rgb[0], rgb[1], rgb[2])))
    print(rgb)
    print(hsl)
    print(proportion)
# RGB and HSL are named tuples, so values can be accessed as properties.
# These all work just as well:
red = rgb[0]
red = rgb.r
saturation = hsl[1]
saturation = hsl.s

# palettes can't be more than five colors
# the idea is that the top five colors must account for at least 80% of the colors in the picture.
def FiveColors(colorList): 
    if len(colorList) <= 5:
        return True
    fiveColorProp = 0
    for x in range(5):
        fiveColorProp += colorList[x].proportion
    if fiveColorProp > .8:
        return True
    return False

#finding the standard deviation of the light values in hsl
def Contrast(colorList):
    lightList = []
    for x in colorList:
        if x.proportion > .10:
            lightList.append(x.hsl.l)
    dev = numpy.std(lightList)
    return dev

# Find the difference between the top proportion and 60, second to 30, and third to 10
def SixThreeTen(colorList):
    firstDist = abs(.60 - colorList[0].proportion)
    secDist = abs(.30 - colorList[1].proportion)
    thirdDist = abs(.10 - colorList[2].proportion)
    return firstDist + secDist + thirdDist

print(f"Five color: {FiveColors(colors)}")
print(f"Contrast: {Contrast(colors)}")







        


