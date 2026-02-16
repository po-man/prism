import sys
from pathlib import Path

# Add the project root to the Python path.
# This allows tests to import modules from the 'app' directory as 'app.xxx'.
# The project root is assumed to be the parent directory of the 'tests' directory.
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))