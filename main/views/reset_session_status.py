# ----------------------------
#  Andrea Silvestroni 2019
#  Residual Noise Extraction and Smartphone Linking
#
# ----------------------------

import os
from django.views.generic import View
from django.shortcuts import redirect

from main.logic.common import const
from main.models import Session, PictureCluster, Picture


# TODO: remove this view once deployed
class ResetSessionStatusView(View):
    """
    Helper View, used to reset session status during debug
    """

    def get(self, *args, **kwargs):
        """
        Resets the session corresponding to the given session ID and redirects to its status page
        """
        try:
            # Reset session
            ses = Session.objects.get(id=kwargs.get('id', ''))
            ses.progress = 0
            ses.stage = const.session_statuses['wait']
            ses.save()

            # Reset extracting Pictures status
            pics = Picture.objects.filter(session=ses, status="extracting")
            for pic in pics:
                pic.status = None
                pic.save()

            # Delete session clusters
            PictureCluster.objects.filter(session=ses).delete()
            try:
                os.remove('storage/%s/%s/clustering_matrix.npy' % (ses.id, 'facebook'))
            except OSError:
                pass

            return redirect('/sessions/' + ses.id)

        except Session.DoesNotExist as e:
            return redirect('/')
