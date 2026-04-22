import os
import sys
import shutil

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
source_db = os.path.join(base_dir, 'db.sqlite3')
tmp_db = '/tmp/db.sqlite3'

if not os.path.exists(tmp_db) and os.path.exists(source_db):
    shutil.copy2(source_db, tmp_db)

# Add the project root to the sys.path so Django can find the 'config' and 'hotel' packages
sys.path.append(base_dir)

from config.wsgi import app
