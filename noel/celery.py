import os
import dotenv
from celery import Celery

dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'), override=True)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noel.settings')
app = Celery('noel', backend=os.environ.get('REDIS_URL'), broker=os.environ.get('REDIS_URL'))
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()