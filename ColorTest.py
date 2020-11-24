import colorgram
import numpy as np
import pandas as pd
import tqdm
import time
from colr import color
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

fileName = 'gatesfence.png'


# Extract 6 colors from an image.
colors = colorgram.extract(fileName, 10) 

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
        return 100
    fiveColorProp = 0
    for x in range(5):
        fiveColorProp += colorList[x].proportion
    return fiveColorProp * 100 

#finding the standard deviation of the light values in hsl
def Contrast(colorList):
    lightList = []
    for x in colorList:
        if x.proportion > .01:
            lightList.append(x.hsl.l)
    dev = np.std(lightList)
    return min(dev, 100)

# Find the difference between the top proportion and 60, second to 30, and third to 10
def SixThreeOne(colorList):
    firstDist = abs(.60 - colorList[0].proportion)
    secDist = abs(.30 - colorList[1].proportion)
    thirdDist = abs(.10 - colorList[2].proportion)

    # best case total distance = 0, worst case total distance = 1
    return (1-(firstDist + secDist + thirdDist))*100

def RedGreen(colorList):
    redGreenCount = 0
    for x in colorList:
        if x.proportion > .05 and (x.hsl.h < 40 or
                                 (70 < x.hsl.h and x.hsl.h < 200) or
                                 (x.hsl.h > 240)):
            redGreenCount += 1
    if redGreenCount > 0:
        redGreenCount -= 1
    return (1 - redGreenCount/len(colorList)) * 100

class ImageData(object):
    left = 0;
    top = 0;
    width = 0;
    height = 0;
    img = lambda: None

    def __init__(self, left, top, width, height, img):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.img = img


# This function will handle the core OCR processing of the screenshot
def ocr_core(image):
    textData = pytesseract.image_to_data(image, output_type = 'data.frame') 
    textData.to_csv("data.csv")
    return textData  

def groupText(text, image):
    # go line by line, if the line has a word then store the top left location
    # keep going until there isnt a word left in the paragraph, then get the location of the last word
    # and width + height to get bottom right location, then crop out the box
    print('Grouping Text...')
    prevParNum = -1
    parList = []
    picName = 0
    currLine = 0
    maxWidth = 0
    tick = False
    l, t, w, h = 0, 0, 0, 0
    for idx, row in tqdm.tqdm(text.iterrows()):
        # textValue = text.iloc[idx]['text']
        # if type(textValue) == str:
        #     textValue.replace(" ","")
        # if not textValue:
        #     prevParNum = text.iloc[idx]['par_num']
        #     continue
        parNum = text.iloc[idx]['block_num']
        if parNum != prevParNum:
            prevParNum = parNum
            # checks if first time
            if not tick:
                tick = True
            else:
                
                w = max(w,maxWidth)
                im = image.crop((l, t, l + w, t + h))
                # parList.append(ImageData(l, t, w, h, im))
                parList.append(im)
                im.save(str(picName) + ".png")
                currLine = 0
                maxWidth = 0
                picName += 1
            l = text.iloc[idx]['left']
            t = text.iloc[idx]['top']
            w = text.iloc[idx]['width']
            h = text.iloc[idx]['height']
            continue
        if text.iloc[idx]['line_num'] > currLine:
            currLine = text.iloc[idx]['line_num']
            h += text.iloc[idx]['height']
            if maxWidth < w:
                maxWidth = w
            w = 0
        w += text.iloc[idx]['width']
        

    return parList
    
def fontSize(parList):
    return 0

def textTests(parList):
    print("Running Tests...")
    contrastList = []
    for x in tqdm.tqdm(range(len(parList))):
        colors = colorgram.extract(parList[x], 5)
        contrastList.append(Contrast(colors))
    return min(99.0, np.average(contrastList)*2)


        
print(ocr_core(fileName))

image = Image.open(fileName)

parList = groupText(ocr_core(image), image)

read = textTests(parList)
fiveColor = FiveColors(colors)
contr = Contrast(colors)
six = SixThreeOne(colors)
redGreen = RedGreen(colors)
finalScore = (read+fiveColor+contr+six+redGreen)/5
print(f"Text Readability: {read}")
print(f"Five color: {fiveColor}")
print(f"Contrast: {contr}")
print(f"60-30-10: {six}")
print(f"Red Green: {redGreen}")

print(f"Final Score: {finalScore}")









        


