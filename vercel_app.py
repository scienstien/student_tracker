import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_tracker.settings')

application = get_wsgi_application()
application = WhiteNoise(application)
application.add_files('staticfiles', prefix='static/')

app = application 