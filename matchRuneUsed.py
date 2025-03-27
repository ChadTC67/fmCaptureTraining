import time
import cv2
import numpy as np
import os

OUTPUT_FOLDER = "captured_runes"

def match_rune_with_templates(last_rune, template_dir="rune_templates"):
    """Matches the cropped rune with known rune templates."""
    rune_templates = {file: cv2.imread(os.path.join(template_dir, file), cv2.IMREAD_UNCHANGED) 
                       for file in os.listdir(template_dir) if file.endswith(".png")}

    best_match = None
    best_score = -1

    for name, template in rune_templates.items():
        if template is None:
            continue

        # Convert template to same color space as last_rune (BGR)
        template = cv2.cvtColor(template, cv2.COLOR_BGRA2BGR)

        template = cv2.resize(template, (last_rune.shape[1], last_rune.shape[0]))
        result = cv2.matchTemplate(last_rune, template, cv2.TM_CCOEFF_NORMED)
        score = np.max(result)

        if score > best_score:
            best_score = score
            best_match = name

    return best_match, best_score

def matchRuneUsed(last_rune):
    
    if last_rune is None:
        print("Error: No rune log image provided.")
        return

    best_match, best_score = match_rune_with_templates(last_rune)

    # Display the best-matching rune name
    if best_match:
        rune_name = best_match.replace(".png", "").replace("_", " ").title()
        print(f"Last rune used: {rune_name} (Confidence: {best_score:.2f})")
    else:
        print("No matching rune found.")

