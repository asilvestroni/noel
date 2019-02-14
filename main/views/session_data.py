# ----------------------------
#  Andrea Silvestroni 2019
#  Residual Noise Extraction and Smartphone Linking
#
# ----------------------------
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View

from main.models import Session


class SessionDataView(View):
    """
    Data endpoint for a particular session
    """

    def get(self, request, id):
        session = get_object_or_404(Session, pk=id)
        data = {
            'id':       session.id,
            'status':   session.status,
            'progress': session.progress
            }

        return JsonResponse(data)
