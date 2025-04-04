package utils

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"
	
	"github.com/sam/fm-data-capture/models"
)

// ExtractReliquatEffets extracts the reliquat value and effects from text
func ExtractReliquatEffets(text string) (float64, []models.CaracValue, error) {
	var reliquat float64 = 0
	var effets []models.CaracValue
	
	lines := strings.Split(text, "\n")
	for _, line := range lines {
		if strings.Contains(strings.ToLower(line), "sink") {
			reliquatRegex := regexp.MustCompile(`sink\s*:\s*(\d+(\.\d+)?)`)
			matches := reliquatRegex.FindStringSubmatch(line)
			if len(matches) > 1 {
				var err error
				reliquat, err = strconv.ParseFloat(matches[1], 64)
				if err != nil {
					return 0, nil, fmt.Errorf("failed to parse reliquat value: %v", err)
				}
			}
		} else if !strings.Contains(line, "Effects / Stats") && 
				 !strings.Contains(line, "COMBINE") && 
				 strings.TrimSpace(line) != "" {
			
			// Extract effects with potential '%' corrections
			effectRegex := regexp.MustCompile(`([O0-9]*)\s*(%?)\s*(\w.+)`)
			matches := effectRegex.FindStringSubmatch(line)
			
			if len(matches) > 3 {
				valueStr := strings.Replace(matches[1], "O", "0", -1) // Replace O with 0
				percentSign := matches[2]
				effectName := strings.TrimSpace(matches[3])
				
				// If the effect name contains a '%' in the name, add it back
				if percentSign != "" {
					effectName = "% " + effectName
				}
				
				// Match the effect name to caracId
				var caracID int
				found := false
				
				for characteristic, id := range models.CaracID {
					if strings.Contains(strings.ToLower(effectName), strings.ToLower(characteristic)) {
						caracID = id
						found = true
						break
					}
				}
				
				if found && valueStr != "" {
					value, err := strconv.Atoi(valueStr)
					if err == nil {
						effets = append(effets, models.CaracValue{
							Value: value,
							ID:    caracID,
						})
					}
				}
			}
		}
	}
	
	return reliquat, effets, nil
}
