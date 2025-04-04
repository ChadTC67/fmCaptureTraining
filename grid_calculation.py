import re
from capture_functions import COMBINE_BUTTON_REGION
from rune_data import runeNumbers, caracId, runeIds


def calculate_grid_item(x, y):
    """
    Calculates the grid item clicked based on the coordinates.

    Args:
        x (int): The x-coordinate of the click.
        y (int): The y-coordinate of the click.

    Returns:
        tuple: A tuple (row, column) representing the grid item clicked, or None if the click is outside the grid.
    """
    grid_start_x = 2072
    grid_start_y = 620
    box_width = 73
    box_height = 73
    padding_x = 24  # Padding for X-axis
    padding_y = 25  # Padding for Y-axis
    num_rows = 13
    num_cols = 3

    # Check if the click is within the grid boundaries
    if not (grid_start_x <= x <= grid_start_x + (box_width + padding_x) * num_cols - padding_x):
        if x < grid_start_x:
            print(f"Click x-coordinate {x} is left of the grid boundaries.")
        else:
            print(f"Click x-coordinate {x} is right of the grid boundaries.")
        return None
    if not (grid_start_y <= y <= grid_start_y + (box_height + padding_y) * num_rows - padding_y):
        if y < grid_start_y:
            print(f"Click y-coordinate {y} is above the grid boundaries.")
        else:
            print(f"Click y-coordinate {y} is below the grid boundaries.")
        return None

    # Calculate the row and column
    col = (x - grid_start_x) // (box_width + padding_x)
    row = (y - grid_start_y) // (box_height + padding_y)

    # Calculate the exact x and y coordinates of the top-left corner of the cell
    cell_start_x = grid_start_x + col * (box_width + padding_x)
    cell_start_y = grid_start_y + row * (box_height + padding_y)

    # Check if the click is within the cell's box
    if not (cell_start_x <= x <= cell_start_x + box_width and
            cell_start_y <= y <= cell_start_y + box_height+1):
        print("Clicked between grid items.")
        return None

    # Check if the calculated row and column are within the grid dimensions
    if 0 <= row < num_rows and 0 <= col < num_cols:
        return (row, col)
    else:
        print(f"Calculated row {row} or column {col} is outside the grid dimensions.")
        return None
    



def matchRuneIdByPosition(x, y, caracs):
    """
    Matches the rune used based on the carac name at the given row.

    Args:
        row (int): The row index of the carac.
        col (int): The column index.
        caracs (list): A list of carac names.

    Returns:
        int: A rune ID if a match is found, or None if no match is found.
    """
    
    if (COMBINE_BUTTON_REGION["left"] <= x <= COMBINE_BUTTON_REGION["left"] + COMBINE_BUTTON_REGION["width"] and
            COMBINE_BUTTON_REGION["top"] <= y <= COMBINE_BUTTON_REGION["top"] + COMBINE_BUTTON_REGION["height"]):
        return 38

    grid_item = calculate_grid_item(x, y)
    if grid_item is None:
        print("Clicked outside the grid.")
        return None
    
    print(f"Clicked on grid item: {grid_item}")
    row, col = grid_item

    if row <= len(caracs):
        currentCaracValue, currentCaracId = caracs[row]
        for caracId, runeId in runeIds.items():
            if currentCaracId == caracId:
                return runeId[col]
        print(f"No rune found for carac {currentCaracId}.")

    return None

