
import os
import sys
from pathlib import Path

# Menentukan folder utama proyek Django
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Menambahkan folder sistem_pakar ke Python Path
sys.path.insert(0, str(PROJECT_DIR))

# Mengatur konfigurasi Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
