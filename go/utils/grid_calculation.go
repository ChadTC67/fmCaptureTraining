package utils

import (
	"fmt"
	
	"github.com/sam/fm-data-capture/models"
)

// GridItem represents a position in the grid
type GridItem struct {
	Row int
	Col int
}

// CalculateGridItem calculates which grid item was clicked based on coordinates
func CalculateGridItem(x, y int) *GridItem {
	gridStartX := 2072
	gridStartY := 620
	boxWidth := 73
	boxHeight := 73
	paddingX := 24
	paddingY := 25
	numRows := 13
	numCols := 3
	
	// Check if click is within grid boundaries
	if !(gridStartX <= x && x <= gridStartX+(boxWidth+paddingX)*numCols-paddingX) {
		if x < gridStartX {
			fmt.Printf("Click x-coordinate %d is left of the grid boundaries.\n", x)
		} else {
			fmt.Printf("Click x-coordinate %d is right of the grid boundaries.\n", x)
		}
		return nil
	}
	
	if !(gridStartY <= y && y <= gridStartY+(boxHeight+paddingY)*numRows-paddingY) {
		if y < gridStartY {
			fmt.Printf("Click y-coordinate %d is above the grid boundaries.\n", y)
		} else {
			fmt.Printf("Click y-coordinate %d is below the grid boundaries.\n", y)
		}
		return nil
	}
	
	// Calculate the row and column
	col := (x - gridStartX) / (boxWidth + paddingX)
	row := (y - gridStartY) / (boxHeight + paddingY)
	
	// Calculate exact coordinates of the top-left corner of the cell
	cellStartX := gridStartX + col*(boxWidth+paddingX)
	cellStartY := gridStartY + row*(boxHeight+paddingY)
	
	// Check if click is within the cell's box
	if !(cellStartX <= x && x <= cellStartX+boxWidth &&
		cellStartY <= y && y <= cellStartY+boxHeight+1) {
		fmt.Println("Clicked between grid items.")
		return nil
	}
	
	// Check if calculated row and column are within grid dimensions
	if 0 <= row && row < numRows && 0 <= col && col < numCols {
		return &GridItem{Row: row, Col: col}
	}
	
	fmt.Printf("Calculated row %d or column %d is outside the grid dimensions.\n", row, col)
	return nil
}

// MatchRuneIdByPosition matches a rune ID based on the clicked position and available characteristics
func MatchRuneIdByPosition(x, y int, caracs []models.CaracValue) int {
	gridItem := CalculateGridItem(x, y)
	if gridItem == nil {
		fmt.Println("Clicked outside the grid.")
		return 0 // Using 0 as "not found" indicator
	}
	
	if gridItem.Row < len(caracs) {
		currentCaracValue := caracs[gridItem.Row]
		for caracID, runeIDs := range models.RuneIDs {
			if currentCaracValue.ID == caracID && gridItem.Col < len(runeIDs) {
				return runeIDs[gridItem.Col]
			}
		}
		fmt.Printf("No rune found for carac %d.\n", currentCaracValue.ID)
	}
	
	return 0
}
