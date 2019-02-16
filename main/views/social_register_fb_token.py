# ----------------------------
#  Andrea Silvestroni 2019
#  Residual Noise Extraction and Smartphone Linking
#
# ----------------------------

from main.models import Session, SocialToken

from django.http import HttpResponse
from django.views import generic


class RegisterFbTokenView(generic.UpdateView):
    """
    Links Facebook Graph API Token to the user's session
    """

    def put(self, request, *args, **kwargs):
        """
        Method accessed via ajax request from the social linking view, Graph API returns a token using PUT
        """

        session_id = request.session.get('session_id')
        token = request.GET.get('token', '')

        if len(token) != 0:
            try:
                session = Session.objects.get(id=session_id)
                tokens = SocialToken.objects.filter(session=session, type='facebook')
                if tokens.count() == 0:
                    SocialToken(session=session, type="facebook", key=token).save()
                else:
                    print('User owns a token already')
            except Session.DoesNotExist as e:
                print('Tried to store token for non existing session')
                return HttpResponse(None)
            
        return HttpResponse(session_id)
