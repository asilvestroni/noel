# ----------------------------
#  Andrea Silvestroni 2019
#  Residual Noise Extraction and Smartphone Linking
#
# ----------------------------
import os

from django.shortcuts import redirect
from django.views.generic import TemplateView

from main.models import Session


class SocialsView(TemplateView):
    """
    List of social network linking buttons, each one connected to a different linking view
    """
    template_name = 'pages/social_linking.html'

    # Prepares the context dictionary before rendering the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fb_app_id'] = os.environ['FB_API_KEY']
        return context

    def get(self, request, *args, **kwargs):
        session_id = request.session.get('session_id')
        if session_id:
            session = Session.objects.get(id=session_id)
            if session.picture_set.count() >= 10:
                return super().get(request, *args, **kwargs)

        return redirect('/')
