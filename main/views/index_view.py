# ----------------------------
#  Andrea Silvestroni 2019
#  Residual Noise Extraction and Smartphone Linking
#
#  Website Index, handles the pictures upload form
# ----------------------------

from django.views.generic import TemplateView

from main.models import Session


class IndexView(TemplateView):
    """
    Index View, shows a widget for original pictures upload
    """
    template_name = 'pages/index.html'

    def get(self, request, *args, **kwargs):
        session_id = request.session.get('session_id')
        try:
            session = Session.objects.get(id=session_id)
            if session.picture_set.count() > 0:
                request.session.flush()
        except Session.DoesNotExist:
            pass

        return super().get(request, *args, **kwargs)

