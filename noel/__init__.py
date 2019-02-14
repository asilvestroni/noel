# ----------------------------
#  Andrea Silvestroni 2019
#  Residual Noise Extraction and Smartphone Linking
#
# ----------------------------

from .celery import app as celery_app

__all__ = ['celery_app']
