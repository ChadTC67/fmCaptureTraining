import time
import os
import mss
import json
import pytesseract
from pynput import mouse
from threading import Timer
import pickle # <-- Import pickle
import numpy as np # <-- Import numpy
# Import the functions from the other files
from SerializationRuneData import formatData, saveToJsonFile
from capture_functions import capture_images, OUTPUT_FOLDER, capture_item_grid, capture_min_max_grid, is_click_combine_region
from ocr_functions import extract_digits, extract_text
from extraction_functions import extract_reliquat_effets
from grid_calculation import matchRuneIdByPosition
from rune_data import runeNumbers, caracId, runeWeight

# Configure Tesseract path if needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Replace with your Tesseract path

# Define output folder for data
OUTPUT_DATA_FOLDER = "output_data"
# Trained model and scaler paths (using names from your training script)
MODEL_PATH = 'model.pkl'
SCALER_PATH = 'scaler.pkl'
os.makedirs(OUTPUT_DATA_FOLDER, exist_ok=True)

counter = 0
# Load the counter
try:
    with open("counter.txt", "r") as f:
        counter = int(f.read())
except FileNotFoundError:
    counter = 0

# Load Model and Scaler globally once (more efficient if script runs long)
model = None
scaler = None
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
    print(f"Successfully loaded model '{MODEL_PATH}' and scaler '{SCALER_PATH}'.")
except FileNotFoundError:
    print(f"Error: Model '{MODEL_PATH}' or scaler '{SCALER_PATH}' not found.")
    print("Please train the model first using your training script.")
    model = None # Ensure model is None if loading failed
except Exception as e:
    print(f"Error loading model/scaler: {e}")
    model = None

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
def delayed_capture(x, y):
    global counter  # Declare that we're using the global counter variable
    caracValues = []
    caracIds = []
    start_time = time.time()  # Start timing
    print(f"Mouse released at ({x}, {y})")
    sct = mss.mss()
    item_img = capture_item_grid(sct)
    
    # Check if the click is in the counter region
    combineClicked = is_click_combine_region(x, y)
    if combineClicked:
        min_img, max_img = capture_min_max_grid(sct)
        min_text = extract_digits(min_img)
        max_text = extract_digits(max_img)

        # Clean the extracted text
        min_text = [s.replace('%', '') for s in min_text]
        max_text = [s.replace('%', '') for s in max_text]

        # Convert to integers, setting to 0 if conversion fails
        min_text = [int(s) if s.isdigit() else 0 for s in min_text]
        max_text = [int(s) if s.isdigit() else 0 for s in max_text]
    else:
        min_text = None
        max_text = None
    

    reliquat_carac_text = extract_text(item_img)

    reliquat, caracs = extract_reliquat_effets(reliquat_carac_text)
    reliquat = float(reliquat) if reliquat else 0.0

    runeUsed = matchRuneIdByPosition(x, y, caracs)
    if runeUsed is None:
        print("No rune used detected.")
        return
    runeUsedWeight = runeWeight.get(runeUsed) 

    for carac in caracs:
        caracValue, caracId = carac
        caracIds.append(caracId)

        caracValues.append(caracValue)
    
    screenshotData = formatData(reliquat, caracValues, caracIds, runeUsed, runeUsedWeight, min_text, max_text)

    # Save data to JSON file in output_data folder
    outputName = os.path.join(OUTPUT_DATA_FOLDER, f"data_{counter:04d}.json")
    if screenshotData:
        saveToJsonFile(screenshotData, outputName,caracIds, min_text, max_text)
    
    if combineClicked:
        counter += 1
        print(f"Counter incremented to: {counter}")
        # Save counter to file
        with open("counter.txt", "w") as f:
            f.write(str(counter))

    # Print debugging information
    elapsed_time = time.time() - start_time
    print("Formatted Data:")
    if screenshotData:
        print(json.dumps(screenshotData, indent=4))
        # for value in screenshotData['data']:
        #     print(f"{value}")
        # print(f"Min values: {screenshotData['min']}")
        # print(f"Max values: {screenshotData['max']}")
    print(f"Processing time: {elapsed_time:.3f} seconds")

def on_click(x, y, button, pressed):
    if not pressed:  # Only trigger on mouse release, not press
        # Wait 200ms before capturing
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