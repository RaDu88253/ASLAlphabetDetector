# Check if Python 3 is installed
if (-not (Get-Command python3 -ErrorAction SilentlyContinue)) {
    Write-Host "Python could not be found. Please install Python 3 to proceed."
    exit 1
}

# Create a virtual environment named 'venv'
python3 -m venv .venv
Write-Host "Virtual environment '.venv' created."

# Activate the virtual environment
$activateScript = ".\.venv\Scripts\Activate.ps1"

if (-not (Test-Path $activateScript)) {
    Write-Host "Activation script not found: $activateScript"
    exit 1
}

# Dot-source the activation script
. $activateScript
Write-Host "Virtual environment '.venv' activated."

# Upgrade pip
python.exe -m pip install --upgrade pip
Write-Host "pip upgraded to the latest version."

# Install dependencies from requirements.txt if the file exists
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
    Write-Host "Dependencies from requirements.txt installed."
} else {
    Write-Host "requirements.txt file not found. Please create one to install dependencies."
}
