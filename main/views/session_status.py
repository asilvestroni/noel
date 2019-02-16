# ----------------------------
#  Andrea Silvestroni 2019
#  Residual Noise Extraction and Smartphone Linking
#
# ----------------------------

import os

from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404

from main.logic.common import const
from main.models import Session, Picture, SocialToken, PictureCluster
from main.logic.process_session import process


class SessionStatusView(View):
    """
    Shows details about the current status of a session
    """

    def get(self, request, id):
        ses = None

        # Obtain session ID from url query
        ses = get_object_or_404(Session, pk=id)
        tokens = SocialToken.objects.filter(session=ses)
        # This page should not be available if no tokens were given, abort the session
        if tokens.count() == 0:
            ses.stage = const.session_statuses['error']
            ses.save()

        # Trigger session processing if this is the first visit
        if ses.stage == const.session_statuses['wait']:
            skip = os.environ.get('SESSION_SKIP')
            options = dict(skip=skip.split(' ') if skip else [])
            process.delay(ses.id, options)

        # Fill up the context dictionary with data needed for the template
        pics = Picture.objects.filter(session=ses).order_by('id')
        clusters = PictureCluster.objects.filter(session=ses)
        groups = []

        for cluster in clusters:
            cluster_dict = {
                'label':    cluster.label,
                'type':     cluster.type,
                'pics':     [],
                'original': cluster.original,
                }

            for pic in pics.filter(cluster=cluster):
                cluster_dict['pics'].append(pic)

            # groups[cluster.type].append(cluster_dict)
            groups.append(cluster_dict)

        context = {
            'session':  ses,
            'pics':     pics,
            'groups':   groups,
            }

        return render(None, 'pages/session_status.html',
                      context=context)
