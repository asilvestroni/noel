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
from main.models import Session, Picture


@timeit
def handle_downloads(ses: Session, tokens: QuerySet):
    """
        Handle downloads from Facebook, given a session and its tokens

        :param ses: Session to which pictures belong
        :param tokens: SN auth tokens associated with the session (avoids a query)
        """
    # TODO: handle missing token

    # Connects to Facebook's GraphAPI
    token = tokens.get(type='facebook')
    graph = facebook.GraphAPI(access_token=token.key)

    if len(Picture.objects.filter(session=ses, type='facebook')) == 0:
        try:
            # Send a custom request for pictures and make a list with their urls
            pics = list(map(lambda p: p['images'][0]['source'], graph.request('me/photos/uploaded?fields=images&limit={}'.format(const.fb_max_pictures)).get('data')))

            n_pics = len(pics)

            # Save pictures
            # TODO: switch to django's file managing
            pics_dir = '{}/{}'.format(ses.session_dir, 'facebook')
            makedirs(pics_dir, exist_ok=True)
            makedirs(pics_dir + '/preps', exist_ok=True)
            makedirs(pics_dir + '/noises', exist_ok=True)

            for pic in enumerate(pics):
                ses.update_and_log_status('Gathering Facebook Pictures: {}/{}'.format(pic[0] + 1, n_pics))
                model = Picture.objects.create(session=ses, type='facebook')
                download_pic(model, pic[1])
        except Exception as e:
            print(e)
