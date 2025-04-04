@echo off
echo Setting up dependencies for FM Data Capture...

REM Check if go.mod exists, if not initialize it
if not exist go.mod (
    echo Initializing go module...
    go mod init github.com/sam/fm-data-capture
)

echo Downloading dependencies...
go get github.com/go-vgo/robotgo
go get github.com/robotn/gohook
go get github.com/kbinani/screenshot
go get golang.org/x/image/draw

echo Tidying go.mod...
go mod tidy

echo Verifying dependencies...
go mod verify

echo Setup complete! You can now build and run the application.
pause
