import os
import sys

# Add the project root to the sys.path so Django can find the 'config' and 'hotel' packages
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.wsgi import app
