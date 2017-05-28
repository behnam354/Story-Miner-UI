import sys
activate_this = '/home/website/strand-demo-backend/StoryMinerUI/app/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

sys.path.insert(0, '/home/website/strand-demo-backend/StoryMinerUI')
from app import app as application
