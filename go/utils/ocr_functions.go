package utils

import (
	"fmt"
	"image"
	"os/exec"
	"strings"
	"sync"
)

// ocrResult stores the result of an OCR operation
type ocrResult struct {
	text string
	err  error
}

// performOCR performs OCR using the Python script
func performOCR(imagePath string, ocrType string, resultChan chan<- ocrResult) {
	cmd := exec.Command("python", "ocr_replacement.py", ocrType, imagePath)
	output, err := cmd.CombinedOutput()
	if err != nil {
		resultChan <- ocrResult{text: "", err: fmt.Errorf("failed to execute Python script: %v, output: %s", err, string(output))}
		return
	}
	resultChan <- ocrResult{text: strings.TrimSpace(string(output)), err: nil}
}

// ExtractText extracts text from an image using the Python OCR script
func ExtractText(img image.Image) (string, error) {
	// Save the image to a temporary file
	tmpFile, err := saveToTempFile(img)
	if err != nil {
		return "", fmt.Errorf("failed to save temp image: %v", err)
	}
	defer tmpFile.cleanup()

	// Perform OCR
	resultChan := make(chan ocrResult)
	go performOCR(tmpFile.path, "extract_item_text", resultChan)
	result := <-resultChan
	return result.text, result.err
}

// ExtractDigits extracts numerical values from an image using the Python OCR script
func ExtractDigits(img *image.Gray) ([]string, error) {
	// Save the image to a temporary file
	tmpFile, err := saveToTempFile(img)
	if err != nil {
		return nil, fmt.Errorf("failed to save temp image: %v", err)
	}
	defer tmpFile.cleanup()

	// Perform OCR
	resultChan := make(chan ocrResult)
	go performOCR(tmpFile.path, "extract_digits_from_image", resultChan)
	result := <-resultChan
	// Split the output into lines
	lines := strings.Split(result.text, "\n")

	// Filter out empty lines
	var finalResult []string
	for _, line := range lines {
		trimmedLine := strings.TrimSpace(line)
		if trimmedLine != "" {
			finalResult = append(finalResult, trimmedLine)
		}
	}

	return finalResult, result.err
}

func CaptureAndExtract() (string, []string, []string, error) {
	var (
		itemImg   *image.Gray
		minImg    *image.Gray
		maxImg    *image.Gray
		itemText  string
		minDigits []string
		maxDigits []string
		err       error
		wg        sync.WaitGroup
		itemErr   error
		minErr    error
		maxErr    error
	)

	// Capture images
	itemImg, minImg, maxImg, err = CaptureImages()
	if err != nil {
		return "", nil, nil, fmt.Errorf("error capturing images: %v", err)
	}

	// Create channels to receive OCR results
	itemChan := make(chan ocrResult)
	minChan := make(chan ocrResult)
	maxChan := make(chan ocrResult)

	// Launch OCR goroutines
	wg.Add(3)

	go func() {
		defer wg.Done()
		itemTextResult, itemErr := ExtractText(itemImg)
		itemChan <- ocrResult{text: itemTextResult, err: itemErr}
	}()

	go func() {
		defer wg.Done()
		minDigitsResult, minErr := ExtractDigits(minImg)
		minChan <- ocrResult{text: strings.Join(minDigitsResult, "\n"), err: minErr}
	}()

	go func() {
		defer wg.Done()
		maxDigitsResult, maxErr := ExtractDigits(maxImg)
		maxChan <- ocrResult{text: strings.Join(maxDigitsResult, "\n"), err: maxErr}
	}()

	// Wait for OCR goroutines to complete
	wg.Wait()

	// Retrieve OCR results from channels
	itemResult := <-itemChan
	itemText = itemResult.text
	itemErr = itemResult.err

	minResult := <-minChan
	minDigits = strings.Split(minResult.text, "\n")
	minErr = minResult.err

	maxResult := <-maxChan
	maxDigits = strings.Split(maxResult.text, "\n")
	maxErr = maxResult.err

	// Handle errors
	if itemErr != nil {
		err = fmt.Errorf("error extracting item text: %v", itemErr)
	}
	if minErr != nil {
		err = fmt.Errorf("error extracting min digits: %v", minErr)
	}
	if maxErr != nil {
		err = fmt.Errorf("error extracting max digits: %v", maxErr)
	}

	return itemText, minDigits, maxDigits, err
}

// CheckForHyphen checks if a region of the image contains a hyphen
func CheckForHyphen(img *image.Gray, x1 int, y1 int, x2 int, y2 int) bool {
	// Count white pixels in the region
	whitePixels := 0
	totalPixels := 0

	for y := y1; y < y2; y++ {
		for x := x1; x < x2; x++ {
			if y >= 0 && y < img.Bounds().Max.Y && x >= 0 && x < img.Bounds().Max.X {
				totalPixels++
				if img.GrayAt(x, y).Y == 255 { // White pixel
					whitePixels++
				}
			}
		}
	}

	// If all pixels are white, it's likely a hyphen
	// You might need to adjust this threshold based on your specific case
	return totalPixels > 0 && float64(whitePixels)/float64(totalPixels) > 0.9
}

// CheckAllHyphens checks for hyphens at multiple positions
func CheckAllHyphens(img *image.Gray) int {
	baseX1 := 35
	baseY1 := 37
	baseX2 := 44
	baseY2 := 40
	yIncrement := 98
	maxHyphens := 12

	hyphenCount := 0

	for i := 0; i < maxHyphens; i++ {
		currentY1 := baseY1 + (i * yIncrement)
		currentY2 := baseY2 + (i * yIncrement)

		// Check if we're still within image boundaries
		if currentY2 <= img.Bounds().Max.Y {
			if CheckForHyphen(img, baseX1, currentY1, baseX2, currentY2) {
				hyphenCount++
			}
		}
	}

	return hyphenCount
}
