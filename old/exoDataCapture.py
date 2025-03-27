import time
import mss
import cv2
import numpy as np
import pytesseract
import os
import re


# Define the region of the screen where the grid is located
GRID_REGION = {
    "top": 350,  # Adjust based on your screen position
    "left": 1020,  # Adjust based on your screen position
    "width": 820,  # Width of the grid area
    "height": 1520  # Height of the grid area
}

# Folder to save captured images
OUTPUT_FOLDER = "captured_grids"
# Empty the output folder on start
if os.path.exists(OUTPUT_FOLDER):
    for filename in os.listdir(OUTPUT_FOLDER):
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                import shutil
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')
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
        # _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        
        # Cover the stats icons
        rectLeftPadding = 325
        rectTopPadding = 270
        rectWidth = 375
        rectHeight = gray.shape[0] # Image height
        imgStatsReliquat = cv2.rectangle(gray, (rectLeftPadding, rectTopPadding), (rectWidth, rectHeight), (255, 255, 255), -1)

        # Save the processed image
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        image_path = os.path.join(OUTPUT_FOLDER, f"grid_{timestamp}.png")
        cv2.imwrite(image_path, imgStatsReliquat)

        return imgStatsReliquat

# Function to extract text from the processed image
def extract_text(image):
    text = pytesseract.image_to_string(image, lang='fra')
    return text

# Function to extract reliquat, Effets/Carac, and Min/Max stats
def extract_reliquat_effets_min_max(text):
    reliquat = None
    effets = []
    min_max_stats = []

    lines = text.split('\n')
    for line in lines:
        if "reliquat" in line:
            reliquat_match = re.search(r'reliquat\s*:\s*(\d+(\.\d+)?)', line)
            if reliquat_match:
                reliquat = reliquat_match.group(1)
        elif "Effets / Carac." in line:
            continue  # Skip the header line
        elif line.strip():  # Non-empty lines after the header
            # Extract effects with potential '%' corrections
            effect_match = re.search(r'(\d+)\s*(%?)\s+(.+)', line)
            if effect_match:
                value = effect_match.group(1)
                percent_sign = effect_match.group(2)  # Capture the '%' if present
                effect_name = effect_match.group(3)
                effets.append(f"{value}{percent_sign} {effect_name}")
            else:
                # Try to extract min/max stats
                min_max_match = re.search(r'(\d+)\s+(\d+)', line)
                if min_max_match:
                    min_val = min_max_match.group(1)
                    max_val = min_max_match.group(2)
                    min_max_stats.append(f"Min: {min_val}, Max: {max_val}")

    return reliquat, effets, min_max_stats

# Main loop to capture and extract data after every click
if __name__ == "__main__":
    while True:
        print("Capturing grid...")
        grid_image = capture_grid()
        text = extract_text(grid_image)

        reliquat, effets, min_max_stats = extract_reliquat_effets_min_max(text)

        print("Reliquat:", reliquat)
        print("Effets / Carac.:")
        for effet in effets:
            print(f"  - {effet}")
        print("Min/Max Stats:")
        for stat in min_max_stats:
            print(f"  - {stat}")

        # Wait for the next action (e.g., after a click)
        time.sleep(2)  # Adjust based on your rune application frequency