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

from config.wsgi import app as _application

def app(environ, start_response):
    # Vercel rewrite maps everything to /api/index.py, causing Django to 404.
    # We retrieve the actual requested URL path from the environment and restore it.
    request_uri = environ.get('REQUEST_URI', '')
    if request_uri:
        environ['PATH_INFO'] = request_uri.split('?')[0]
    elif environ.get('PATH_INFO', '').startswith('/api/index.py'):
        environ['PATH_INFO'] = environ['PATH_INFO'].replace('/api/index.py', '', 1) or '/'
        
    environ['SCRIPT_NAME'] = ''
        
    return _application(environ, start_response)
