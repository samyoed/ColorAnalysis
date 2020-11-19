import pytesseract
import numpy as np


try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

def ocr_core(filename):
    
    # This function will handle the core OCR processing of images.
    
    text = pytesseract.image_to_data(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

print(ocr_core('ocrTest2.png'))