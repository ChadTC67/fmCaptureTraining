package utils

import (
	"fmt"
	"image"
	"image/color"
	"image/png"
	"os"
	"path/filepath"
	"time"

	"github.com/kbinani/screenshot"
)

const (
	// Output folder for saving captured images
	OutputFolder = "captured_grids"
)

// Region represents a rectangular region on the screen
type Region struct {
	Top    int
	Left   int
	Width  int
	Height int
}

var (
	// ItemStatsGridRegion defines the region for item stats
	ItemStatsGridRegion = Region{
		Top:    350,
		Left:   1020,
		Width:  820,
		Height: 1540,
	}

	// MinGridRegion defines the region for minimum values
	MinGridRegion = Region{
		Top:    620,
		Left:   1050,
		Width:  100,
		Height: 1240,
	}

	// MaxGridRegion defines the region for maximum values
	MaxGridRegion = Region{
		Top:    620,
		Left:   1191,
		Width:  110,
		Height: 1240,
	}
)

// InitializeOutputFolder creates the output folder if it doesn't exist
// and cleans it if it does
func InitializeOutputFolder() error {
	// Create the output directory if it doesn't exist
	if _, err := os.Stat(OutputFolder); os.IsNotExist(err) {
		err := os.MkdirAll(OutputFolder, 0755)
		if err != nil {
			return fmt.Errorf("failed to create output directory: %v", err)
		}
		return nil
	}

	// Clean the output directory
	files, err := os.ReadDir(OutputFolder)
	if err != nil {
		return fmt.Errorf("failed to read output directory: %v", err)
	}

	for _, file := range files {
		err := os.RemoveAll(filepath.Join(OutputFolder, file.Name()))
		if err != nil {
			return fmt.Errorf("failed to clean output directory: %v", err)
		}
	}

	return nil
}

// CaptureRegion captures a region of the screen and returns it as an image
func CaptureRegion(region Region) (*image.RGBA, error) {
	// Capture the primary display
	bounds := image.Rect(region.Left, region.Top, region.Left+region.Width, region.Top+region.Height)
	img, err := screenshot.CaptureRect(bounds)
	if err != nil {
		return nil, fmt.Errorf("failed to capture screen: %v", err)
	}

	return img, nil
}

func RemoveBorders(img *image.RGBA) *image.RGBA {
	// Define the colors to be replaced and the replacement color
	colorFF8080 := color.RGBA{R: 255, G: 128, B: 128, A: 255}   // #FF8080
	color90E052 := color.RGBA{R: 144, G: 224, B: 82, A: 255}    // #90E052
	replacementColor := color.RGBA{R: 41, G: 44, B: 76, A: 255} // #292C4C

	bounds := img.Bounds()
	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			c := img.At(x, y)
			if rgba, ok := c.(color.RGBA); ok {
				if rgba == colorFF8080 {
					img.SetRGBA(x, y, replacementColor)
				} else if rgba == color90E052 {
					img.SetRGBA(x, y, replacementColor)
				}
			}
		}
	}

	return img
}

// ConvertToGrayscale converts an RGBA image to grayscale
func ConvertToGrayscale(img *image.RGBA) *image.Gray {
	bounds := img.Bounds()
	grayImg := image.NewGray(bounds)

	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			r, g, b, _ := img.At(x, y).RGBA()
			// Standard grayscale formula
			gray := uint8((0.3*float64(r) + 0.59*float64(g) + 0.11*float64(b)) / 256.0)
			grayImg.SetGray(x, y, color.Gray{Y: gray})
		}
	}

	return grayImg
}

// ThresholdImage applies binary thresholding to a grayscale image
func ThresholdImage(img *image.Gray) *image.Gray {
	bounds := img.Bounds()
	threshImg := image.NewGray(bounds)

	// Simple thresholding at 128 (middle value)
	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			if img.GrayAt(x, y).Y > 128 {
				threshImg.SetGray(x, y, color.Gray{Y: 255}) // White
			} else {
				threshImg.SetGray(x, y, color.Gray{Y: 0}) // Black
			}
		}
	}

	return threshImg
}

// RectangleMask creates a white rectangle on the image
func RectangleMask(img *image.Gray, x1, y1, x2, y2 int) {
	for y := y1; y < y2; y++ {
		for x := x1; x < x2; x++ {
			if y >= 0 && y < img.Bounds().Max.Y && x >= 0 && x < img.Bounds().Max.X {
				img.SetGray(x, y, color.Gray{Y: 255}) // White
			}
		}
	}
}

// SaveImage saves an image to the specified path
func SaveImage(img image.Image, filename string) error {
	// Create output directory if it doesn't exist
	if _, err := os.Stat(OutputFolder); os.IsNotExist(err) {
		os.MkdirAll(OutputFolder, 0755)
	}

	path := filepath.Join(OutputFolder, filename)
	file, err := os.Create(path)
	if err != nil {
		return fmt.Errorf("failed to create file: %v", err)
	}
	defer file.Close()

	return png.Encode(file, img)
}

// CaptureItemGrid captures and processes the item stats grid
func CaptureItemGrid() (*image.Gray, error) {
	img, err := CaptureRegion(ItemStatsGridRegion)
	if err != nil {
		return nil, err
	}

	// Convert to grayscale
	gray := ConvertToGrayscale(img)

	// Cover the stats icons with white rectangle
	rectLeftPadding := 0
	rectTopPadding := 270
	rectWidth := 375
	rectHeight := gray.Bounds().Max.Y
	RectangleMask(gray, rectLeftPadding, rectTopPadding, rectWidth, rectHeight)

	// Save the processed image
	timestamp := time.Now().Format("20060102-150405")
	err = SaveImage(gray, fmt.Sprintf("item_%s.png", timestamp))
	if err != nil {
		return nil, err
	}

	return gray, nil
}

// CaptureMinMaxGrid captures and processes the min/max value grids
func CaptureMinMaxGrid() (*image.Gray, *image.Gray, error) {
	minImg, err := CaptureRegion(MinGridRegion)
	if err != nil {
		return nil, nil, err
	}

	maxImg, err := CaptureRegion(MaxGridRegion)
	if err != nil {
		return nil, nil, err
	}

	minFlat := RemoveBorders(minImg)
	maxFlat := RemoveBorders(maxImg)

	// Convert to grayscale
	minGray := ConvertToGrayscale(minFlat)
	maxGray := ConvertToGrayscale(maxFlat)

	// Apply thresholding
	minThresh := ThresholdImage(minGray)
	maxThresh := ThresholdImage(maxGray)

	// Save the processed images
	timestamp := time.Now().Format("20060102-150405")
	err = SaveImage(minThresh, fmt.Sprintf("min_%s.png", timestamp))
	if err != nil {
		return nil, nil, err
	}

	err = SaveImage(maxThresh, fmt.Sprintf("max_%s.png", timestamp))
	if err != nil {
		return nil, nil, err
	}

	return minThresh, maxThresh, nil
}

// CaptureImages captures all required images from the screen
func CaptureImages() (*image.Gray, *image.Gray, *image.Gray, error) {
	itemImg, err := CaptureItemGrid()
	if err != nil {
		return nil, nil, nil, err
	}

	minImg, maxImg, err := CaptureMinMaxGrid()
	if err != nil {
		return nil, nil, nil, err
	}

	return itemImg, minImg, maxImg, nil
}
