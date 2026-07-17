import json
from pathlib import Path


def validate_data(min_values, max_values, reliquat, carac_values, carac_ids):
    """
    Validates the data for rune serialization.

    Args:
        min_values: List of minimum values
        max_values: List of maximum values
        reliquat: Reliquat value
        carac_values: List of characteristic values
        carac_ids: List of characteristic IDs

    Returns:
        str: Error message if data is invalid, None otherwise
    """
    if len(min_values) != len(max_values):
        error_message = "Error: min and max arrays must have the same length"
        print(error_message)
        return error_message

    required_length = 13

    while len(min_values) < required_length:
        min_values.append(None)
    while len(max_values) < required_length:
        max_values.append(None)
    while len(carac_values) < required_length:
        carac_values.append(None)
    while len(carac_ids) < required_length:
        carac_ids.append(None)

    for index in range(len(min_values)):
        if min_values[index] == "":
            min_values[index] = None
        if max_values[index] == "":
            max_values[index] = None
        if carac_values[index] == "":
            carac_values[index] = None

    return None


def format_data(reliquat, carac_values, carac_ids, rune_id, rune_weight, min_values=None, max_values=None):
    return [
        carac_values,
        rune_id,
        rune_weight,
        reliquat,
    ]


def save_to_json_file(data, filename, carac_ids, min_values=None, max_values=None):
    """
    Saves the formatted data to a JSON file.
    If the file already exists, the new data is appended as a new entry.

    Args:
        data: The data to save
        filename: The name of the JSON file

    Returns:
        bool: True if successful, False otherwise
    """
    path = Path(filename)

    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        json_data = {
            "data": [],
            "caracIds": carac_ids,
        }

        if path.exists() and path.stat().st_size > 0:
            try:
                with path.open("r") as file:
                    json_data = json.load(file)
            except json.JSONDecodeError:
                print(f"Warning: {path} is corrupted, creating new file")
                json_data = {
                    "data": [],
                    "caracIds": carac_ids,
                }

        json_data["data"].append(data)
        json_data["caracIds"] = carac_ids

        if min_values is not None:
            json_data["min"] = min_values
            json_data["max"] = max_values

        with path.open("w") as file:
            json.dump(json_data, file, indent=2)

        print(f"Data saved to {path}")
        return True
    except Exception as e:
        print(f"Error saving to JSON file: {str(e)}")
        return False


# Backwards-compatible aliases for older local scripts.
validateData = validate_data
formatData = format_data
saveToJsonFile = save_to_json_file
