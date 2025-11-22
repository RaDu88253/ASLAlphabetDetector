#shell script to set up a Python virtual environment and install dependencies

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 could not be found. Please install Python 3 to proceed."
    exit 1
fi

# Create a virtual environment named 'venv'
python3 -m venv .venv
echo "Virtual environment '.venv' created."
# Activate the virtual environment
source .venv/bin/activate
echo "Virtual environment '.venv' activated."
# Upgrade pip to the latest version
pip install --upgrade pip
echo "pip upgraded to the latest version."
# Install dependencies from requirements.txt
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
    echo "Dependencies from requirements.txt installed."
else
    echo "requirements.txt file not found. Please create one to install dependencies."
fi
