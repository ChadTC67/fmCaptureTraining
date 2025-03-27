import time
import os
import pytesseract
from pynput import mouse
from threading import Timer
# Import the functions from the other files
from SerializationRuneData import formatData
from capture_functions import capture_images, OUTPUT_FOLDER
from ocr_functions import extract_digits, extract_text
from extraction_functions import extract_reliquat_effets
from grid_calculation import  matchRuneIdByPosition # Import the grid calculation function
from rune_data import runeNames, runeNumbers, caracId, runeWeight

# Configure Tesseract path if needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Replace with your Tesseract path

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

# Function to perform capture after a slight delay
def delayed_capture(x,y):
    start_time = time.time()  # Start timing
    print(f"Mouse released at ({x}, {y})")
    grid_item_image, min_image, max_image = capture_images()

    reliquat_carac_text = extract_text(grid_item_image)
    min_text = extract_digits(min_image)
    max_text = extract_digits(max_image)

    # Clean the extracted text
    min_text = [s.replace('%', '') for s in min_text]
    max_text = [s.replace('%', '') for s in max_text]

    # Convert to integers, setting to 0 if conversion fails
    min_text = [int(s) if s.isdigit() else 0 for s in min_text]
    max_text = [int(s) if s.isdigit() else 0 for s in max_text]

    reliquat, caracs = extract_reliquat_effets(reliquat_carac_text)
    reliquat = float(reliquat) if reliquat else 0.0

    runeUsed = matchRuneIdByPosition(x, y, caracs)
    if runeUsed is None:
        print("No rune used detected.")
        return
    runeUsedWeight = runeWeight.get(runeUsed) 

    caracValues = []
    caracIds = []
    for carac in caracs:
        caracValue, caracId = carac
        caracIds.append(caracId)

        caracValues.append(caracValue)
    
    screenshotData = formatData(min_text, max_text, reliquat, caracValues, caracIds, runeUsed, runeUsedWeight)
    # # Uncomment for debugging:
    print("Formatted Data:")
    if screenshotData:
        for value in screenshotData:
            print(f"{value}")
    # if runeUsed is not None:
    #     print(f"Rune used: {runeUsed}")
    # else:
    #     print("No rune used detected.")
    # print("Raw min text:", min_text)
    # print("Raw max text:", max_text)
    # print("Min/Max Stats:")
    # for i in range(len(mins)):
    #     if i < len(mins) and i < len(maxs):
    #         print(f"  - Min: {mins[i]}, Max: {maxs[i]}")
    # print("Reliquat:", reliquat)
    # Calculate and print total processing time
    elapsed_time = time.time() - start_time
    print(f"Processing time: {elapsed_time:.3f} seconds")

def on_click(x, y, button, pressed):
    if not pressed:  # Only trigger on mouse release, not press

        # Wait 300ms (0.25 seconds) before capturing
        Timer(0.20, delayed_capture, args=(x, y)).start()

# Set up the mouse listener
if __name__ == "__main__":
    print("Starting capture on click release. Press Ctrl+C to exit.")
    
    # Start the mouse listener
    with mouse.Listener(on_click=on_click) as listener:
        try:
            listener.join()  # Keep the script running
        except KeyboardInterrupt:
            print("\nCapture script terminated.")