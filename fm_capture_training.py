import json
import os
import time
from pathlib import Path
from threading import Timer

import mss
import pytesseract
from pynput import mouse

from capture_functions import (
    OUTPUT_FOLDER,
    capture_item_grid,
    capture_min_max_grid,
    is_click_combine_region,
)
from ocr_functions import extract_digits, extract_text
from extraction_functions import extract_reliquat_effets
from grid_calculation import matchRuneIdByPosition
from rune_data import runeWeight
from serialization_rune_data import format_data, save_to_json_file

OUTPUT_DATA_FOLDER = Path("output_data")
COUNTER_PATH = Path("counter.txt")
CAPTURE_DELAY_SECONDS = 0.20


def configure_tesseract() -> None:
    """Use a custom Tesseract binary when TESSERACT_CMD is set."""
    tesseract_cmd = os.environ.get("TESSERACT_CMD")
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd


def load_counter() -> int:
    try:
        return int(COUNTER_PATH.read_text().strip())
    except (FileNotFoundError, ValueError):
        return 0


def save_counter(value: int) -> None:
    COUNTER_PATH.write_text(str(value))


counter = load_counter()

def delayed_capture(x, y):
    global counter
    carac_values = []
    carac_ids = []
    start_time = time.time()
    print(f"Mouse released at ({x}, {y})")
    sct = mss.mss()
    item_img = capture_item_grid(sct)
    
    # Check if the click is in the counter region
    combine_clicked = is_click_combine_region(x, y)
    if combine_clicked:
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

    rune_used = matchRuneIdByPosition(x, y, caracs)
    if rune_used is None:
        print("No rune used detected.")
        return
    rune_used_weight = runeWeight.get(rune_used)

    for carac in caracs:
        carac_value, carac_id = carac
        carac_ids.append(carac_id)

        carac_values.append(carac_value)
    
    screenshot_data = format_data(reliquat, carac_values, carac_ids, rune_used, rune_used_weight, min_text, max_text)

    # Save data to JSON file in output_data folder
    output_name = OUTPUT_DATA_FOLDER / f"data_{counter:04d}.json"
    if screenshot_data:
        save_to_json_file(screenshot_data, output_name, carac_ids, min_text, max_text)
    
    if combine_clicked:
        counter += 1
        print(f"Counter incremented to: {counter}")
        save_counter(counter)

    # Print debugging information
    elapsed_time = time.time() - start_time
    print("Formatted Data:")
    if screenshot_data:
        print(json.dumps(screenshot_data, indent=4))
    print(f"Processing time: {elapsed_time:.3f} seconds")


def on_click(x, y, button, pressed):
    if not pressed:
        Timer(CAPTURE_DELAY_SECONDS, delayed_capture, args=(x, y)).start()


if __name__ == "__main__":
    configure_tesseract()
    OUTPUT_DATA_FOLDER.mkdir(exist_ok=True)
    Path(OUTPUT_FOLDER).mkdir(exist_ok=True)

    print("Starting capture on click release. Press Ctrl+C to exit.")
    with mouse.Listener(on_click=on_click) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            print("\nCapture script terminated.")
