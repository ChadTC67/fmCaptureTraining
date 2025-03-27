def validateData(min, max, reliquat, caracValues, caracIds, runeId, runeWeight):
    """
    Validates the data for rune serialization.
    
    Args:
        min: List of minimum values
        max: List of maximum values
        reliquat: Reliquat value
        caracValues: List of characteristic values
        caracIds: List of characteristic IDs
        runeId: Rune ID
        runeWeight: Rune weight
        
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

def formatData(min, max, reliquat, caracValues, caracIds, runeId, runeWeight):

    validData = validateData(min, max, reliquat, caracValues, caracIds, runeId, runeWeight)

    if validData is not None:
        return None
    
    # Format the data to be serialized
    data = [
        [caracIds[0], min[0], max[0], caracValues[0]],
        [caracIds[1], min[1], max[1], caracValues[1]],
        [caracIds[2], min[2], max[2], caracValues[2]],
        [caracIds[3], min[3], max[3], caracValues[3]],
        [caracIds[4], min[4], max[4], caracValues[4]],
        [caracIds[5], min[5], max[5], caracValues[5]],
        [caracIds[6], min[6], max[6], caracValues[6]],
        [caracIds[7], min[7], max[7], caracValues[7]],
        [caracIds[8], min[8], max[8], caracValues[8]],
        [caracIds[9], min[9], max[9], caracValues[9]],
        [caracIds[10], min[10], max[10], caracValues[10]],
        [caracIds[11], min[11], max[11], caracValues[11]],
        [caracIds[12], min[12], max[12], caracValues[12]],
        runeId,
        runeWeight,
        reliquat
    ]
    # print("Data:", data)
    return data