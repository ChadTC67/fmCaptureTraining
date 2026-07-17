import time
from pathlib import Path

import cv2
import numpy as np

ITEM_STATS_GRID_REGION = {
    "top": 350,
    "left": 1020,
    "width": 820,
    "height": 1540,
}

COMBINE_BUTTON_REGION = {
    "top": 450,
    "left": 1520,
    "width": 190,
    "height": 50,
}

RUNES_PASSED_GRID_REGION = {
    "top": 600,
    "left": 420,
    "width": 60,
    "height": 1249,
}

OUTPUT_FOLDER = Path("captured_grids")

BACKGROUND_RGB = np.array([58, 61, 88], dtype=np.uint8)  # #3A3D58
BACKGROUND_HSV = cv2.cvtColor(np.uint8([[BACKGROUND_RGB]]), cv2.COLOR_RGB2HSV)[0][0]

hue_range = 10
lower_bound = np.array([BACKGROUND_HSV[0] - hue_range, 30, 30], dtype=np.uint8)
upper_bound = np.array([BACKGROUND_HSV[0] + hue_range, 255, 255], dtype=np.uint8)


def find_last_rune_row(rune_mask):
    """Finds the last row containing a rune in the mask."""
    for y in range(rune_mask.shape[0] - 1, 0, -1):
        if np.any(rune_mask[y, :] > 0):  # Check if row contains a rune
            return y
    return None


def crop_last_rune(rune_log, last_rune_y, rune_height=60):
    """Crops the last rune from the rune log image."""
    start_y = max(0, last_rune_y - rune_height + 1)
    return rune_log[start_y:last_rune_y + 8, :]


def capture_item_grid(sct):
    stats_screenshot = sct.grab(ITEM_STATS_GRID_REGION)

    img_item = np.array(stats_screenshot)
    img_item = cv2.cvtColor(img_item, cv2.COLOR_BGRA2BGR)

    img_item = cv2.cvtColor(img_item, cv2.COLOR_BGR2GRAY)

    # Cover the stats icons
    rect_left_padding = 0
    rect_top_padding = 270
    rect_width = 375
    rect_height = img_item.shape[0]
    img_item_stats_reliquat = cv2.rectangle(
        img_item,
        (rect_left_padding, rect_top_padding),
        (rect_width, rect_height),
        (255, 255, 255),
        -1,
    )

    OUTPUT_FOLDER.mkdir(exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    item_path = OUTPUT_FOLDER / f"item_{timestamp}.png"

    cv2.imwrite(str(item_path), img_item_stats_reliquat)

    return img_item_stats_reliquat


def capture_rune_grid(sct):
    runes_passed_screenshot = sct.grab(RUNES_PASSED_GRID_REGION)
    
    img_rune_passed = np.array(runes_passed_screenshot)
    img_rune_passed = cv2.cvtColor(img_rune_passed, cv2.COLOR_BGRA2BGR)

    # Convert image to HSV for better background detection
    hsv_log = cv2.cvtColor(img_rune_passed, cv2.COLOR_BGR2HSV)

    # Create a mask to remove background
    mask = cv2.inRange(hsv_log, lower_bound, upper_bound)
    rune_mask = cv2.bitwise_not(mask)  # Invert mask to keep non-background pixels

    last_rune_y = find_last_rune_row(rune_mask)
    if last_rune_y is None:
        print("No rune detected")
        return None

    return crop_last_rune(img_rune_passed, last_rune_y)


def apply_clahe(img):
    """Apply CLAHE to enhance contrast."""
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    return clahe.apply(img)


def increase_brightness(img, value=50):
    """Increase brightness by adding a constant value."""
    img = cv2.convertScaleAbs(img, alpha=1, beta=value)
    return img


def capture_min_max_grid(sct):
    """Captures the min/max values grid region from the screen and enhances the images."""
    
    MIN_GRID_REGION = {
        "top": 620,
        "left": 1050,
        "width": 100,
        "height": 1240,
    }

    MAX_GRID_REGION = {
        "top": 620,
        "left": 1191,
        "width": 110,
        "height": 1240,
    }
    
    min_screenshot = sct.grab(MIN_GRID_REGION)
    max_screenshot = sct.grab(MAX_GRID_REGION)
    
    # Convert to an OpenCV image
    img_min = np.array(min_screenshot)
    img_min = cv2.cvtColor(img_min, cv2.COLOR_BGRA2BGR)

    img_max = np.array(max_screenshot)
    img_max = cv2.cvtColor(img_max, cv2.COLOR_BGRA2BGR)

    # Define the colors to be replaced and the replacement color
    color_ff8080 = np.array([128, 128, 255], dtype=np.uint8)  # BGR format for #FF8080
    color_90e052 = np.array([82, 224, 144], dtype=np.uint8)  # BGR format for #90E052
    replacement_color = np.array([76, 44, 41], dtype=np.uint8)  # BGR format for #292C4C

    # Create masks for the colors to be replaced
    mask_min_ff8080 = np.all(img_min == color_ff8080, axis=-1)
    mask_min_90e052 = np.all(img_min == color_90e052, axis=-1)
    mask_max_ff8080 = np.all(img_max == color_ff8080, axis=-1)
    mask_max_90e052 = np.all(img_max == color_90e052, axis=-1)

    # Replace the colors
    img_min[mask_min_ff8080] = replacement_color
    img_min[mask_min_90e052] = replacement_color
    img_max[mask_max_ff8080] = replacement_color
    img_max[mask_max_90e052] = replacement_color

    # Convert to grayscale
    img_min = cv2.cvtColor(img_min, cv2.COLOR_BGR2GRAY)
    img_max = cv2.cvtColor(img_max, cv2.COLOR_BGR2GRAY)

    # Apply brightness increase
    img_min = increase_brightness(img_min, value=50)
    img_max = increase_brightness(img_max, value=50)

    img_min = cv2.threshold(img_min, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    img_max = cv2.threshold(img_max, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    OUTPUT_FOLDER.mkdir(exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    min_path = OUTPUT_FOLDER / f"min_{timestamp}.png"
    max_path = OUTPUT_FOLDER / f"max_{timestamp}.png"
    
    cv2.imwrite(str(min_path), img_min)
    cv2.imwrite(str(max_path), img_max)
    
    return img_min, img_max


def is_click_combine_region(x, y):
    """Check if a click is within the counter increment region."""
    return (COMBINE_BUTTON_REGION["left"] <= x <= COMBINE_BUTTON_REGION["left"] + COMBINE_BUTTON_REGION["width"] and
            COMBINE_BUTTON_REGION["top"] <= y <= COMBINE_BUTTON_REGION["top"] + COMBINE_BUTTON_REGION["height"])


def capture_images(sct):
    item_img = capture_item_grid(sct)
    min_img, max_img = capture_min_max_grid(sct)
    return item_img, min_img, max_img
