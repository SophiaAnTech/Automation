#################
### version 1 ###
#################

# in the extracted text, iced mocha's price is incorrect

import pytesseract
from PIL import Image
import os

# os.environ['PATH'] = '/opt/homebrew/Cellar:' + os.environ['PATH'] #this line will get permission error

# Instead of modifying PATH, directly specify the tesseract command path
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/Cellar/tesseract/5.5.2/bin/tesseract'

# Extract text from single image
def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

# Usage
image_path = '/Users/ax/Downloads/receipt.png'
extracted_text = extract_text_from_image(image_path)
print(extracted_text)

# # Save to file
# with open('extracted_text.txt', 'w', encoding='utf-8') as f:
#     f.write(extracted_text)





#################
### version 2 ###
#################

# use opencv and tessseract improve the accuracy of the extraction, but still not as good as AI.
!pip install opencv-python
import pytesseract
from PIL import Image
import cv2
import numpy as np
import os

# Specify tesseract command path for Homebrew installations
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

# Enhanced text extraction with preprocessing
def extract_text_from_image(image_path):
    # Read image with OpenCV
    img = cv2.imread(image_path)
    
    # Preprocessing to improve OCR accuracy
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to get black and white image
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # Optional: Apply additional preprocessing if needed
    # Remove noise
    kernel = np.ones((1, 1), np.uint8)
    img_cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    # Convert the OpenCV image back to PIL format for pytesseract
    img_pil = Image.fromarray(img_cleaned)
    
    # Use additional tesseract configuration to improve number recognition
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789.ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz '
    
    # Extract text
    text = pytesseract.image_to_string(img_pil, config=custom_config)
    return text

# Usage
image_path = '/Users/ax/Downloads/receipt.png'
extracted_text = extract_text_from_image(image_path)
print(extracted_text)

# # Save to file
# with open('extracted_text.txt', 'w', encoding='utf-8') as f:
#     f.write(extracted_text)
