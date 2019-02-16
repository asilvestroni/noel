# ----------------------------
#  Andrea Silvestroni 2019
#  Residual Noise Extraction and Smartphone Linking
#
# ----------------------------
import os

from django.core.validators import RegexValidator
from django.db import models


# from main.logic.common.funcs import get_session_progress


class Session(models.Model):
    """
    Model that represents a Session on the system. It is created when the user submits their photos through the index's
    form, and is used throughout the process to keep track of the steps that need to be completed.
    """
    # TODO: consider adding an email field for completion notification
    # TODO: consider using Django's file managing instead of direct path access

    id = models.CharField(max_length=64, validators=[RegexValidator(regex='^.{64}$')], primary_key=True)
    status = models.CharField(max_length=50)
    progress = models.FloatField(default=0)
    stage = models.CharField(max_length=20)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

        originals_dir = '{}/original'.format(self.session_dir)
        if not os.path.isdir(originals_dir):
            os.makedirs(originals_dir)
            os.makedirs(originals_dir + '/preps')
            os.makedirs(originals_dir + '/noises')

    @property
    def session_dir(self):
        """
        :return: Path to the session's main directory
        """
        return 'storage/{}'.format(self.id)

    def update_and_log_status(self, step: str = '', progress: float = 0):
        """
        Updates session status and logs it to console

        :param step: session stage step that has been reached
        :param progress: stage progress
        """
        from main.logic.update_session import next_session_status
        status = next_session_status(self, step=step, progress=progress)
        print('[{}]: {} +{}%'.format(self.id, status, progress))
