package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"time"

	hook "github.com/robotn/gohook"
	"github.com/sam/fm-data-capture/models"
	"github.com/sam/fm-data-capture/utils"
)

// Initialize logger
var logger *log.Logger

func init() {
	// Create log file
	logFile, err := os.OpenFile("fm-data-capture.log", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		fmt.Printf("Failed to open log file: %v\n", err)
		os.Exit(1)
	}

	logger = log.New(logFile, "", log.LstdFlags)
	logger.Println("Application starting...")

	// Initialize output folder
	if err := utils.InitializeOutputFolder(); err != nil {
		logger.Printf("Failed to initialize output folder: %v\n", err)
		fmt.Printf("Failed to initialize output folder: %v\n", err)
		os.Exit(1)
	}
}

// delayedCapture performs the screen capture after a short delay
func delayedCapture(x, y int) {
	start := time.Now()
	fmt.Printf("Mouse released at (%d, %d)\n", x, y)
	logger.Printf("Mouse released at (%d, %d)\n", x, y)

	// Wait for 300ms before capturing
	time.Sleep(300 * time.Millisecond)

	// Capture images
	itemImg, minImg, maxImg, err := utils.CaptureImages()
	if err != nil {
		logger.Printf("Error capturing images: %v\n", err)
		fmt.Printf("Error capturing images: %v\n", err)
		return
	}

	// Extract text using OCR
	reliquatCaracText, err := utils.ExtractText(itemImg)
	if err != nil {
		logger.Printf("Error extracting text from item image: %v\n", err)
		fmt.Printf("Error extracting text from item image: %v\n", err)
		return
	}

	minText, err := utils.ExtractDigits(minImg)
	if err != nil {
		logger.Printf("Error extracting min values: %v\n", err)
		fmt.Printf("Error extracting min values: %v\n", err)
		return
	}

	maxText, err := utils.ExtractDigits(maxImg)
	if err != nil {
		logger.Printf("Error extracting max values: %v\n", err)
		fmt.Printf("Error extracting max values: %v\n", err)
		return
	}

	// Extract reliquat and characteristics
	reliquat, caracs, err := utils.ExtractReliquatEffets(reliquatCaracText)
	if err != nil {
		logger.Printf("Error extracting reliquat and effects: %v\n", err)
		fmt.Printf("Error extracting reliquat and effects: %v\n", err)
		return
	}

	// Match rune ID based on position
	runeID := utils.MatchRuneIdByPosition(x, y, caracs)
	runeWeight := models.RuneWeight[runeID]

	// Format the data
	screenshotData, err := utils.FormatData(minText, maxText, reliquat, caracs, caracs, runeID, runeWeight)
	if err != nil {
		logger.Printf("Error formatting data: %v\n", err)
		fmt.Printf("Error formatting data: %v\n", err)
		return
	}

	// Print the formatted data for debugging
	fmt.Println("Formatted Data:")
	jsonData, _ := json.MarshalIndent(screenshotData, "", "  ")
	fmt.Println(string(jsonData))

	if runeID != 0 {
		fmt.Printf("Rune used: %d\n", runeID)
	} else {
		fmt.Println("No rune used detected.")
	}

	fmt.Printf("Processing time: %.3f seconds\n", time.Since(start).Seconds())
	logger.Printf("Processing time: %.3f seconds\n", time.Since(start).Seconds())
}

func main() {
	fmt.Println("Starting capture on click release. Press Ctrl+C to exit.")

	// Use hook.Add instead of Register
	hook.Register(hook.MouseUp, []string{}, func(e hook.Event) {
		fmt.Printf("Mouse clicked: %v at (%d, %d)\n", e.Button, e.X, e.Y)
		delayedCapture(int(e.X), int(e.Y))
	})

	// Handle ESC key press
	hook.Register(hook.KeyDown, []string{"ctrl", "c"}, func(e hook.Event) {
		fmt.Println("Ctrl+C pressed, exiting...")
		hook.End()
		os.Exit(0)
	})

	// Start listening for events
	fmt.Println("Listening for events...")
	s := hook.Start()
	<-hook.Process(s)
}
