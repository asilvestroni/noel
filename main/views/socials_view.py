# ----------------------------
#  Andrea Silvestroni 2019
#  Residual Noise Extraction and Smartphone Linking
#
# ----------------------------
import os

from django.views.generic import TemplateView


class SocialsView(TemplateView):
    """
    List of social network linking buttons, each one connected to a different linking view
    """
    template_name = 'pages/social_linking.html'

    # Prepares the context dictionary before rendering the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fb_app_id'] = os.environ['FB_API_KEY']
        context['ses_id'] = self.request.session.session_key
        return context
