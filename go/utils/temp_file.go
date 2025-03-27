package utils

import (
	"fmt"
	"image"
	"image/png"
	"os"
	"path/filepath"
)

// tempFile represents a temporary file with cleanup functionality
type tempFile struct {
	path string
	file *os.File
}

// cleanup removes the temporary file
func (t *tempFile) cleanup() {
	if t.file != nil {
		t.file.Close()
	}
	os.Remove(t.path)
}

// saveToTempFile saves an image to a temporary file and returns its path
func saveToTempFile(img image.Image) (*tempFile, error) {
	// Create a temporary file
	tempDir := os.TempDir()
	tmpFile, err := os.CreateTemp(tempDir, "ocr-*.png")
	if err != nil {
		return nil, fmt.Errorf("failed to create temp file: %v", err)
	}

	// Save the image to the temporary file
	err = png.Encode(tmpFile, img)
	if err != nil {
		tmpFile.Close()
		os.Remove(tmpFile.Name())
		return nil, fmt.Errorf("failed to encode image: %v", err)
	}

	// Close the file to ensure it's fully written
	tmpFile.Close()

	return &tempFile{
		path: filepath.ToSlash(tmpFile.Name()),
		file: nil,
	}, nil
}
