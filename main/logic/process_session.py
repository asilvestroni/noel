# ----------------------------
#  Andrea Silvestroni 2019
#  Residual Noise Extraction and Smartphone Linking
#
#  Task that contains all the steps needed to compute a session
# ----------------------------

import os
from typing import Callable

import main.logic.social.facebook as fb

from .common import status_extracted, generate_thumbnails
from .common.pics import pics_residual_noise, cluster_pattern_noise
from .social.clustering import clusterize
from .social.linking import link_types

from main.models import Picture, SocialToken, PictureCluster, Session

from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


# Session processing: defines the workflow for each session based on the given options
# TODO: find a better way to handle statuses and status changes
@shared_task
def process(ses_id: str, options: dict = {'skip': []}):
    """
    Processes a session. Accepts an options dictionary which accepts as keys:
        - skip: array; defines which steps should be skipped (check .env.example for details)
        - matlab_runtime: str; contains the path to the installed matlab runtime
    :param ses_id: Id of the session to process
    :param options: Options dictionary
    """
    skip = options['skip']

    if len(options) > 0:
        print('Processing session with options: ', options)

    ses = Session.objects.get(id=ses_id)
    try:
        # Acquire the tokens owned by the session
        tokens = SocialToken.objects.filter(session=ses)

        def handle_social_downloads():
            """
            Called to download from all of SNs the Session has access to
            """

            def fetch_pictures(token_type: str, handler: Callable):
                try:
                    token = tokens.get(type=token_type)
                    handler(ses, token)
                except SocialToken.DoesNotExist:
                    print('Could not fetch {} pictures'.format(token_type))

            # Add social download handlers here
            if len(tokens) > 0:
                fetch_pictures('facebook', fb.handle_downloads)
                ses.update_and_log_status('final')

        generate_thumbnails(ses)

        # Download all SNs pictures for the session
        if 'social_download' not in skip:
            ses.update_and_log_status()
            handle_social_downloads()

        # Creates the cluster where all original pictures will be contained
        original_cluster = PictureCluster.objects.get_or_create(session=ses, type='original',
                                                                label="original", original=True)[0]
        # Extract Residual Noise from original pictures
        if 'rn_original' not in skip:
            ses.update_and_log_status('original')

            pics_residual_noise(ses, 'original')

            # Get the actual pictures (all the valid ones that were extracted)
            original_pics = Picture.objects.filter(session=ses, type='original', status=status_extracted)

            if len(original_pics) < 10:
                raise Exception('Not enough original pictures (%d < 10)' % len(original_pics))

            # Associate all original pictures to the original cluster
            for pic in original_pics:
                pic.cluster = original_cluster
                pic.save()

        # Compute Pattern Noise for the original cluster
        if 'pn_original' not in skip:
            cluster_pattern_noise(original_cluster)

        # Extract Residual Noise from SN pictures
        if 'rn_social' not in skip:

            # Cycle through all the authorized SNs
            for token in tokens:
                ses.update_and_log_status(token.type)

                pics_residual_noise(ses, type=token.type)

            ses.update_and_log_status('final')

            for token in tokens:
                ses.update_and_log_status(token.type)

                # Cluster the pictures based on their Residual Noises
                clusterize(ses, cluster_type=token.type)

                # Get all the clusters obtained from the previous step
                clusters = PictureCluster.objects.filter(session=ses, type=token.type).prefetch_related('picture_set')

                # Compute Pattern Noise for the SN clusters
                if 'pn_social' not in skip:
                    for cluster in clusters:
                        ses.update_and_log_status(cluster.type, 50)
                        cluster_pattern_noise(cluster)

        # Link clusters between each other
        if 'linking' not in skip:
            # Original by social
            for token in tokens:
                link_types(ses, 'original', token.type)

            # Social by social
            # for token in tokens:
            #     other_tokens = tokens.exclude(id=token.id)
            #     for other in other_tokens:
            #         link_types(ses, token, other)

        ses.update_and_log_status('final')
    except Exception as e:
        # If any exception is raised while processing the session, catch it here and signal it
        import traceback
        ses.update_and_log_status('error occurred')
        logger.error(e)
        logger.error(traceback.format_exc())
