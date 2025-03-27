# FM Data Capture Go Version

This is a Go implementation of the FM Data Capture tool, which captures and processes in-game rune data from Dofus.

## Prerequisites

1. Go 1.18 or higher
2. Tesseract OCR installed and available in your PATH
3. The following Go packages (automatically installed via go.mod):
   - github.com/go-vgo/robotgo
   - github.com/kbinani/screenshot 
   - github.com/otiai10/gosseract/v2
   - github.com/robotn/gohook

## Installation

1. Install Tesseract OCR:
   - Windows: Download and install from https://github.com/UB-Mannheim/tesseract/wiki
   - macOS: `brew install tesseract`
   - Linux: `sudo apt-get install tesseract-ocr`

2. Install required C libraries for robotgo:
   - Windows: `gcc` and related build tools
   - macOS: Xcode Command Line Tools
   - Linux: `sudo apt-get install gcc libc6-dev libx11-dev xorg-dev libxtst-dev libpng++-dev xcb libxcb-xkb-dev x11-xkb-utils libx11-xcb-dev libxkbcommon-dev libxkbcommon-x11-dev libxinerama-dev`

3. Clone the repository:
   ```bash
   git clone https://github.com/your-username/fm-data-capture.git
   cd fm-data-capture/go
   ```

4. Install dependencies:
   ```bash
   go mod download
   ```

## Usage

1. Run the application:
   ```bash
   go run main.go
   ```

2. The application will start capturing mouse click events. Each time you release a mouse click, it will:
   - Capture the item stats grid
   - Capture the min/max grids
   - Process the images with OCR
   - Extract relevant values
   - Match the clicked position to determine the rune used
   - Format and display the data

3. To exit the application, press Ctrl+C or ESC.

## Output

The application will:
1. Save captured images to the `captured_grids` folder
2. Display formatted data in the console
3. Log activities to `fm-data-capture.log`

## Troubleshooting

- If OCR results are inaccurate, make sure Tesseract is properly installed and available in your PATH
- Adjust the screen coordinates in `utils/capture_functions.go` if they don't match your screen layout
- Check the log file for detailed error information
