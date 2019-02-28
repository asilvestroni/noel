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
        from main.templatetags.pic_filters import pic_thumb
        session = get_object_or_404(Session, pk=id)
        data = {
            'id':       session.id,
            'status':   session.status,
            'progress': session.progress,
            'pictures': {x.id: {'id': x.id, 'status': x.status, 'data': pic_thumb(x.thumb_path)} for x in
                         session.picture_set.all()},
            }

        return JsonResponse(data)
