import re
from rune_data import caracId


CHARACTERISTICS_BY_LENGTH = sorted(caracId.items(), key=lambda item: len(item[0]), reverse=True)


def extract_reliquat_effets(text):
    reliquat = None
    effets = []

    lines = text.split('\n')
    for line in lines:
        if "sink" in line:
            reliquat_match = re.search(r'sink\s*:\s*(\d+(\.\d+)?)', line)
            if reliquat_match:
                reliquat = reliquat_match.group(1)
        elif "Effects / Stats" in line:
            continue  # Skip the header line
        elif "COMBINE" in line:
            continue  # Skip the header line
        elif line.strip():  # Non-empty lines after the header
            # Extract effects with potential '%' corrections
            effect_match = re.search(r'([O0-9]*)\s*(%?)\s*(\w.+)', line)
            if effect_match:
                value = effect_match.group(1).replace('O', '0')  # Replace O with 0
                percent_sign = effect_match.group(2)  # Capture the '%' if present
                effect_name = effect_match.group(3).strip()
                
                # If the effect name contains a '%' in the name, add it back
                if percent_sign:
                    effect_name = f"% {effect_name}"
                
                # Match the effect name to caracId
                carac_id = None
                for characteristic, c_id in CHARACTERISTICS_BY_LENGTH:
                    if characteristic.lower() in effect_name.lower():
                        carac_id = c_id
                        break
                
                if carac_id and value:
                    try:
                        numeric_value = int(value) if value else 0
                        effets.append((numeric_value, carac_id))
                    except ValueError:
                        # Skip effects with invalid numeric values
                        pass
    return reliquat, effets

def extract_min_max(min_text, max_text):
    """
    Extracts min and max values from the given text.

    Args:
        min_text (str): The text containing min values.
        max_text (str): The text containing max values.

    Returns:
        tuple: Two lists, one for min values and one for max values.
    """
    min_values = []
    max_values = []

    min_lines = min_text.split('\n')
    max_lines = max_text.split('\n')

    for min_line, max_line in zip(min_lines, max_lines):
        # Use regex to find numbers in each line
        min_match = re.search(r'(\d+)', min_line)
        max_match = re.search(r'(\d+)', max_line)
        
        if min_match and max_match:
            min_values.append(int(min_match.group(1)))
            max_values.append(int(max_match.group(1)))

    return min_values, max_values
