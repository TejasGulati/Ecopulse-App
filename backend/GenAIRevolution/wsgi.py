import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'backend'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GenAIRevolution.settings')

application = get_wsgi_application()


# Add this block for Render deployment
if os.environ.get('RENDER'):
    from django.core.management.commands.runserver import Command as runserver
    runserver.default_port = os.environ.get('PORT', 8000)