import time
import mss
import cv2
import numpy as np
import pytesseract
import os
import re

# Configure Tesseract path if needed
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Define the region of the screen where the grid is located
GRID_REGION = {
    "top": 400,  # Adjust based on your screen position
    "left": 1250,  # Adjust based on your screen position
    "width": 575,  # Width of the grid area
    "height": 1280  # Height of the grid area
}

# Folder to save captured images
OUTPUT_FOLDER = "captured_grids"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Function to capture screen and process image
def capture_grid():
    with mss.mss() as sct:
        screenshot = sct.grab(GRID_REGION)
        
        # Convert to an OpenCV image
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # Optional: Preprocess the image (grayscale, thresholding, etc.)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        
        # Cover the problematic column
        cv2.rectangle(thresh, (200, 320), (220 + 45, thresh.shape[0]), (255, 255, 255), -1)

        # Save the processed image
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        image_path = os.path.join(OUTPUT_FOLDER, f"grid_{timestamp}.png")
        cv2.imwrite(image_path, thresh)

        return thresh

# Function to extract text from the processed image
def extract_text(image):
    text = pytesseract.image_to_string(image, lang='fra')
    return text

# Function to extract reliquat and Effets/Carac
def extract_reliquat_and_effets(text):
    reliquat = None
    effets = []

    lines = text.split('\n')
    for line in lines:
        if "reliquat" in line:
            reliquat_match = re.search(r'reliquat\s*:\s*(\d+)', line)
            if reliquat_match:
                reliquat = reliquat_match.group(1)
        elif "Effets / Carac." in line:
            continue  # Skip the header line
        elif line.strip():  # Non-empty lines after the header
            # Extract effects, assuming they are in the format "number Effect Name"
            effect_match = re.search(r'(\d+)\s+(.+)', line)
            if effect_match:
                effets.append(f"{effect_match.group(1)} {effect_match.group(2)}")
    
    return reliquat, effets

# Main loop to capture and extract data after every click
if __name__ == "__main__":
    while True:
        print("Capturing grid...")
        grid_image = capture_grid()
        text = extract_text(grid_image)

        reliquat, effets = extract_reliquat_and_effets(text)

        print("Reliquat:", reliquat)
        print("Effets / Carac.:")
        for effet in effets:
            print(f"  - {effet}")

        # Wait for the next action (e.g., after a click)
        time.sleep(2)  # Adjust based on your rune application frequency