# ----------------------------
#  Andrea Silvestroni 2019
#  Residual Noise Extraction and Smartphone Linking
#
# ----------------------------

from django.db import models
from django.db.models import Model, ForeignKey, CharField

from . import Session


class SocialToken(Model):
    """
    Model representing a Social Network authorization for a Session. Contains the API key provided by the Social,
    in order to allow access to its endpoints
    """
    session = ForeignKey(Session, on_delete=models.CASCADE)
    type = CharField(max_length=20)
    key = CharField(max_length=300)
