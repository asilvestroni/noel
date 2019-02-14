# ----------------------------
#  Andrea Silvestroni 2019
#  Residual Noise Extraction and Smartphone Linking
#
#  Linking between different picture types (different SN, social and original, ...)
# ----------------------------

import numpy as np
from scipy.stats import pearsonr

from ..common import timeit
from main.models import PictureCluster, Session


@timeit
def link_types(ses: Session, source_type: str, dest_type: str):
    """
    Finds the original cluster in dest_type by using the pattern noise of the one in source_type
    :param ses: The session the clusters belong to
    :param source_type: Type of pictures the source cluster contains (original, facebook, ...)
    :param dest_type: Type of pictures the destination cluster contains (original, facebook, ...)
    """

    # Fetch the clusters
    src_cluster = PictureCluster.objects.filter(session=ses, type=source_type, original=True).first()
    dst_clusters = list(PictureCluster.objects.filter(session=ses, type=dest_type))

    # Fetch the pattern noises
    src_pn = np.load(src_cluster.pattern_noise_path)
    dst_pns = [np.load(cluster.pattern_noise_path) for cluster in dst_clusters]

    # Compute correlations between pattern noises
    corrs = [pearsonr(src_pn.flatten(), y.flatten())[0] for y in dst_pns]

    # Get the most similar destination cluster
    dest_original = dst_clusters[np.argmax(corrs)]

    # Mark it as original
    dest_original.original = True
    dest_original.save()

