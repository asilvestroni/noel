# ----------------------------
#  Andrea Silvestroni 2019
#  Residual Noise Extraction and Smartphone Linking
#
# ----------------------------

from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('socials/', views.SocialsView.as_view()),
    path('socials/fb_token', views.RegisterFbTokenView.as_view()),
    path('sessions/<id>', views.SessionStatusView.as_view()),
    path('sessions/<id>/data', views.SessionDataView.as_view()),
    path('reset/<id>', views.ResetSessionStatusView.as_view()),
    # re_path('^.*$', RedirectView.as_view(url='/'))
    ]
