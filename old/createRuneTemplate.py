import cv2
import re
import os
import pytesseract
from PIL import Image

# Load the image
# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Create path to the image in the same directory
image_path = os.path.join(script_dir, "min_20250324-150718.png")
image = cv2.imread(image_path)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding to improve OCR accuracy
gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Perform OCR
custom_oem_psm_config = r'--oem 3 --psm 6'  # Use default OCR engine with semi-structured layout
text = pytesseract.image_to_string(gray, config=custom_oem_psm_config)

# Print extracted text
print("Extracted text:\n", text)

# Extract numerical values from the text
numbers = re.findall(r'\d+%?|\d+\.\d+', text)  # Match integers, percentages, and decimal numbers
print("Extracted numbers:", numbers)