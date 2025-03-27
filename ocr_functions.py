import pytesseract
import numpy as np

def extract_text(image):
    text = pytesseract.image_to_string(image, lang='eng')
    return text

def check_for_hyphen(image, x1, y1, x2, y2):
    """
    Check if all pixels in the specified grid are white (255),
    which would indicate the presence of a hyphen.
    """
    # Extract the region of interest
    roi = image[y1:y2, x1:x2]
    
    # Check if all pixels are white (255 for white in grayscale)
    is_hyphen = np.all(roi == 255)
    
    return is_hyphen

def check_all_hyphens(image, base_x1=35, base_y1=37, base_x2=44, base_y2=40, y_increment=98, max_hyphens=12):
    """
    Check for hyphens at multiple positions by incrementing Y coordinates.
    Returns a list of booleans indicating hyphen presence at each position.
    """
    hyphen_count = 0
    
    for i in range(max_hyphens):
        # Calculate the Y coordinates for this iteration
        current_y1 = base_y1 + (i * y_increment)
        current_y2 = base_y2 + (i * y_increment)
        
        # Check if we're still within the image boundaries
        if current_y2 <= image.shape[0]:
            hyphen_detected = check_for_hyphen(image, base_x1, current_y1, base_x2, current_y2)
            hyphen_count += hyphen_detected
    
    return hyphen_count

def extract_digits(image):
    custom_oem_psm_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789%'
    text = pytesseract.image_to_string(image, config=custom_oem_psm_config)
    
    # Check for hyphens at all potential positions
    hyphen_count = check_all_hyphens(image)

    # Split min_text and max_text on newlines to get individual values
    text = text.split("\n")
    # remove empty strings from the lists
    text = list(filter(None, text))
    # for each exo add '-' to the front of the array
    for i in range(hyphen_count):
        text.insert(i, "-")
    
    return text
