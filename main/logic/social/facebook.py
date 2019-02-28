# ----------------------------
#  Andrea Silvestroni 2019
#  Residual Noise Extraction and Smartphone Linking
#
#  Functions for Facebook interaction
# ----------------------------

import facebook
from os import makedirs
from django.db.models import QuerySet
from main.logic.common import timeit, download_pic, const
from main.models import Session, Picture, SocialToken


@timeit
def handle_downloads(ses: Session, token: SocialToken):
    """
        Handle downloads from Facebook, given a session and its tokens

        :param ses: Session to which pictures belong
        :param token: Facebook SocialToken
        """

    # Connects to Facebook's GraphAPI
    graph = facebook.GraphAPI(access_token=token.key)

    if len(Picture.objects.filter(session=ses, type='facebook')) == 0:
        try:
            # Send a custom request for pictures and make a list with their urls
            pics = list(map(lambda p: p['images'][0]['source'], graph.request(
                    'me/photos/uploaded?fields=images&limit={}'.format(const.fb_max_pictures)).get('data')))

            n_pics = len(pics)

            # Save pictures
            # TODO: switch to django's file managing
            pics_dir = '{}/{}'.format(ses.session_dir, 'facebook')
            makedirs(pics_dir, exist_ok=True)
            makedirs(pics_dir + '/preps', exist_ok=True)
            makedirs(pics_dir + '/noises', exist_ok=True)

            for pic in enumerate(pics):
                model = Picture.objects.create(session=ses, type='facebook')
                download_pic(model, pic[1])
                ses.update_and_log_status('facebook', 1 / n_pics)
        except Exception as e:
            print(e)
