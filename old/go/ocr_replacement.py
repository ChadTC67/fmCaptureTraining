import pytesseract
import cv2
import os
import sys

# Configure Tesseract path (update if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path, whitelist=None):
    """
    Extracts text from an image using pytesseract.

    Args:
        image_path (str): The path to the image file.
        whitelist (str, optional): Characters to whitelist for OCR. Defaults to None.

    Returns:
        str: The extracted text.
    """
    try:
        # Load the image using OpenCV
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Could not load image at {image_path}")
            return None

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply thresholding to improve OCR accuracy
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Configure tesseract
        config = ''
        if whitelist:
            config = f'-c tessedit_char_whitelist={whitelist}'

        # Perform OCR using pytesseract
        text = pytesseract.image_to_string(thresh, lang='eng', config=config)
        return text.strip()
    except Exception as e:
        print(f"Error during OCR: {e}")
        return None

def extract_item_text(image_path):
    """
    Extracts text from the item stats image.

    Args:
        image_path (str): The path to the item stats image.

    Returns:
        str: The extracted text.
    """
    return extract_text_from_image(image_path)

def extract_digits_from_image(image_path):
    """
    Extracts digits from the min/max images.

    Args:
        image_path (str): The path to the min/max image.

    Returns:
        str: The extracted digits.
    """
    return extract_text_from_image(image_path, whitelist='0123456789-%')

if __name__ == '__main__':
    # Get the function name and image path from command-line arguments
    if len(sys.argv) < 3:
        print("Usage: python ocr_replacement.py <function_name> <image_path>")
        sys.exit(1)

    function_name = sys.argv[1]
    image_path = sys.argv[2]

    if function_name == "extract_item_text":
        result = extract_item_text(image_path)
        print(result)
    elif function_name == "extract_digits_from_image":
        result = extract_digits_from_image(image_path)
        print(result)
    else:
        print(f"Error: Unknown function name {function_name}")
