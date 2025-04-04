import json
import os
from datetime import datetime

def validateData(min, max, reliquat, caracValues, caracIds):
    """
    Validates the data for rune serialization.
    
    Args:
        min: List of minimum values
        max: List of maximum values
        reliquat: Reliquat value
        caracValues: List of characteristic values
        caracIds: List of characteristic IDs
        
    Returns:
        str: Error message if data is invalid, None otherwise
    """
    # Check if min and max have the same length
    if len(min) != len(max):
        error_message = "Error: min and max arrays must have the same length"
        print(error_message)
        return error_message
    
    # Pad lists with None if they are shorter than 13
    required_length = 13
    
    while len(min) < required_length:
        min.append(None)
    while len(max) < required_length:
        max.append(None)
    while len(caracValues) < required_length:
        caracValues.append(None)
    while len(caracIds) < required_length:
        caracIds.append(None)
    
    # Handle reliquat if None or 0
    if reliquat is None or reliquat == 0:
        reliquat = 0
    
    # Check and handle empty values in min, max, and caracValues
    for i in range(len(min)):
        
        if min[i] == "" or min[i] is None:
            min[i] = None
        
        if max[i] == "" or max[i] is None:
            max[i] = None
            
        if caracValues[i] == "" or caracValues[i] is None:
            caracValues[i] = None
    
    return None

def formatData(reliquat, caracValues, caracIds, runeId, runeWeight, min=None, max=None):

    # validData = validateData(min, max, reliquat, caracValues, caracIds)

    # while len(caracValues) < 13:
    #     caracValues.append(None)

    # if validData is not None:
    #     return None
    
    # Format the data to be serialized
    data = [
        caracValues,
        runeId,
        runeWeight,
        reliquat
    ]
    return data

def saveToJsonFile(data, filename, caracIds, min=None, max=None):
    """
    Saves the formatted data to a JSON file.
    If the file already exists, the new data is appended as a new entry.
    
    Args:
        data: The data to save
        filename: The name of the JSON file (default: rune_data.json)
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
        
        # Check if file exists and load existing data
        existing_data = []
        jsonData = {
            "data": existing_data,
            "caracIds": caracIds,
        }
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            try:
                with open(filename, 'r') as file:
                    jsonData = json.load(file)
            except json.JSONDecodeError:
                # If the file is corrupted, we'll start fresh
                print(f"Warning: {filename} is corrupted, creating new file")
                jsonData = {
                    "min": min,
                    "max": max,
                    "data": existing_data
                }
        
        # Add the new entry and save
        jsonData["data"].append(data)
        if min is not None:
            jsonData["min"] = min
            jsonData["max"] = max
        
        with open(filename, 'w') as file:
            json.dump(jsonData, file, indent=2)
        
        print(f"Data saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving to JSON file: {str(e)}")
        return False