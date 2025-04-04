package utils

import (
	"fmt"
	"strconv"
	
	"github.com/sam/fm-data-capture/models"
)

// RuneData represents the final formatted data structure
type RuneData struct {
	Row1       [3]interface{} `json:"row1"`
	Row2       [3]interface{} `json:"row2"`
	Row3       [3]interface{} `json:"row3"`
	Row4       [3]interface{} `json:"row4"`
	Row5       [3]interface{} `json:"row5"`
	Row6       [3]interface{} `json:"row6"`
	Row7       [3]interface{} `json:"row7"`
	Row8       [3]interface{} `json:"row8"`
	Row9       [3]interface{} `json:"row9"`
	Row10      [3]interface{} `json:"row10"`
	Row11      [3]interface{} `json:"row11"`
	Row12      [3]interface{} `json:"row12"`
	Row13      [3]interface{} `json:"row13"`
	CaracIds   []models.CaracValue `json:"caracIds"`
	RuneId     int     `json:"runeId"`
	RuneWeight float64 `json:"runeWeight"`
	Reliquat   float64 `json:"reliquat"`
}

// ValidateData validates the input data before serialization
func ValidateData(mins []string, maxs []string, reliquat float64, caracValues []models.CaracValue, 
                 caracIds []models.CaracValue, runeId int, runeWeight float64) ([]interface{}, []interface{}, float64, bool) {
	
	// Check if min and max have the same length
	if len(mins) != len(maxs) {
		fmt.Println("Error: min and max arrays must have the same length")
		return nil, nil, 0, false
	}
	
	// Ensure reliquat is not negative
	if reliquat < 0 {
		reliquat = 0
	}
	
	// Convert string values to integers or nil
	minValues := make([]interface{}, len(mins))
	maxValues := make([]interface{}, len(maxs))
	
	for i := range mins {
		// Handle mins
		if mins[i] == "-" || mins[i] == "" {
			minValues[i] = nil
		} else {
			val, err := strconv.Atoi(mins[i])
			if err != nil {
				minValues[i] = nil
			} else {
				minValues[i] = val
			}
		}
		
		// Handle maxs
		if maxs[i] == "-" || maxs[i] == "" {
			maxValues[i] = nil
		} else {
			val, err := strconv.Atoi(maxs[i])
			if err != nil {
				maxValues[i] = nil
			} else {
				maxValues[i] = val
			}
		}
	}
	
	return minValues, maxValues, reliquat, true
}

// FormatData formats the data into the final structure
func FormatData(mins []string, maxs []string, reliquat float64, caracValues []models.CaracValue, 
               caracIds []models.CaracValue, runeId int, runeWeight float64) (*RuneData, error) {
	
	minValues, maxValues, reliquat, valid := ValidateData(mins, maxs, reliquat, caracValues, caracIds, runeId, runeWeight)
	if !valid {
		return nil, fmt.Errorf("data validation failed")
	}
	
	// Ensure we have enough data to fill all rows
	for len(minValues) < 13 {
		minValues = append(minValues, nil)
	}
	for len(maxValues) < 13 {
		maxValues = append(maxValues, nil)
	}
	
	// Create caracValue array with same length
	caracValueArray := make([]interface{}, 13)
	for i := range caracValues {
		if i < len(caracValueArray) {
			caracValueArray[i] = caracValues[i].Value
		}
	}
	
	// Create the data structure
	data := &RuneData{
		Row1:       [3]interface{}{minValues[0], maxValues[0], caracValueArray[0]},
		Row2:       [3]interface{}{minValues[1], maxValues[1], caracValueArray[1]},
		Row3:       [3]interface{}{minValues[2], maxValues[2], caracValueArray[2]},
		Row4:       [3]interface{}{minValues[3], maxValues[3], caracValueArray[3]},
		Row5:       [3]interface{}{minValues[4], maxValues[4], caracValueArray[4]},
		Row6:       [3]interface{}{minValues[5], maxValues[5], caracValueArray[5]},
		Row7:       [3]interface{}{minValues[6], maxValues[6], caracValueArray[6]},
		Row8:       [3]interface{}{minValues[7], maxValues[7], caracValueArray[7]},
		Row9:       [3]interface{}{minValues[8], maxValues[8], caracValueArray[8]},
		Row10:      [3]interface{}{minValues[9], maxValues[9], caracValueArray[9]},
		Row11:      [3]interface{}{minValues[10], maxValues[10], caracValueArray[10]},
		Row12:      [3]interface{}{minValues[11], maxValues[11], caracValueArray[11]},
		Row13:      [3]interface{}{minValues[12], maxValues[12], caracValueArray[12]},
		CaracIds:   caracIds,
		RuneId:     runeId,
		RuneWeight: runeWeight,
		Reliquat:   reliquat,
	}
	
	return data, nil
}
