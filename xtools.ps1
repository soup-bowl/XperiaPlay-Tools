if (Get-Command python3 -errorAction SilentlyContinue) {
    python3 -m xpt
} elseif (Get-Command python -errorAction SilentlyContinue) {
    python -m xpt
} else {
	"Error: Python is not installed."
	"Get Python from your package manager, or here - https://www.python.org/downloads/"
	"Please ensure when prompted, you add Python to PATH. Otherwise xtools will not be able to run."
	exit 1
}
